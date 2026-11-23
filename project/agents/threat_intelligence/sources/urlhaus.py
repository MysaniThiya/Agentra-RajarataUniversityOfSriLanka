import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

from agents.threat_intelligence.url_validator import validate_url

# Find and load the .env file in the project folder
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")


# URLhaus API endpoint
URLHAUS_API = "https://urlhaus-api.abuse.ch/v1/url/"


def check_urlhaus(url: str) -> dict:
    """
    Check whether a URL is listed in the URLhaus database.
    """
    # Validate the URL before contacting URLhaus
    validation_result = validate_url(url)

    if not validation_result["valid"]:
        return {
            "source": "URLhaus",
            "status": "error",
            "matched": None,
            "message": validation_result["message"]
        }

    # 1. Get the API key from the .env file
    auth_key = os.getenv("ABUSE_CH_AUTH_KEY")

    if not auth_key:
        return {
            "source": "URLhaus",
            "status": "unavailable",
            "matched": None,
            "message": "URLhaus Auth-Key is missing."
        }

    # 2. Send the URL to the URLhaus API
    try:
        response = httpx.post(
            URLHAUS_API,
            headers={
                "Auth-Key": auth_key
            },
            data={
                "url": url
            },
            timeout=15.0
        )

        # Raise an error if the API returns an unsuccessful HTTP status
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary
        result = response.json()

        query_status = result.get("query_status")

        # 3. Check whether URLhaus found the URL
        if query_status == "ok":
            return {
                "source": "URLhaus",
                "status": "completed",
                "matched": True,
                "url": result.get("url"),
                "threat": result.get("threat"),
                "url_status": result.get("url_status"),
                "tags": result.get("tags", []),
                "date_added": result.get("date_added")
            }

        elif query_status == "no_results":
            return {
                "source": "URLhaus",
                "status": "completed",
                "matched": False,
                "message": "No matching URL was found in URLhaus."
            }

        # 4. Handle unexpected API responses
        return {
            "source": "URLhaus",
            "status": "error",
            "matched": None,
            "message": f"Unexpected API response: {query_status}"
        }

    # 5. Handle connection and API errors
    except httpx.TimeoutException:
        return {
            "source": "URLhaus",
            "status": "unavailable",
            "matched": None,
            "message": "URLhaus API request timed out."
        }

    except httpx.HTTPStatusError as error:
        return {
            "source": "URLhaus",
            "status": "error",
            "matched": None,
            "message": f"HTTP error: {error.response.status_code}"
        }

    except (httpx.RequestError, ValueError) as error:
        return {
            "source": "URLhaus",
            "status": "error",
            "matched": None,
            "message": f"Request failed: {type(error).__name__}"
        }