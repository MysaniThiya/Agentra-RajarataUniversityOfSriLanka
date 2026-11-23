
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

from agents.threat_intelligence.url_validator import validate_url


# Find and load the .env file in the project folder
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")


# ThreatFox API endpoint
THREATFOX_API = "https://threatfox-api.abuse.ch/api/v1/"


def check_threatfox(url: str) -> dict:
    """
    Check whether a URL is listed in the ThreatFox database.
    """

    # 1. Validate the URL before contacting ThreatFox
    validation_result = validate_url(url)

    if not validation_result["valid"]:
        return {
            "source": "ThreatFox",
            "status": "error",
            "matched": None,
            "message": validation_result["message"]
        }

    # 2. Get the API key from the .env file
    auth_key = os.getenv("ABUSE_CH_AUTH_KEY")

    if not auth_key:
        return {
            "source": "ThreatFox",
            "status": "unavailable",
            "matched": None,
            "message": "ThreatFox Auth-Key is missing."
        }

    # 3. Search for the URL in ThreatFox
    try:
        response = httpx.post(
            THREATFOX_API,
            headers={
                "Auth-Key": auth_key
            },
            json={
                "query": "search_ioc",
                "search_term": url,
                "exact_match": True
            },
            timeout=15.0
        )

        response.raise_for_status()

        result = response.json()
        query_status = result.get("query_status")

        # 4. Check the API response
        if query_status == "ok":
            return {
                "source": "ThreatFox",
                "status": "completed",
                "matched": True,
                "results": result.get("data", [])
            }

        elif query_status == "no_result":
            return {
                "source": "ThreatFox",
                "status": "completed",
                "matched": False,
                "message": "No matching indicator was found in ThreatFox."
            }

        return {
            "source": "ThreatFox",
            "status": "error",
            "matched": None,
            "message": f"Unexpected API response: {query_status}"
        }

    # 5. Handle API and connection errors
    except httpx.TimeoutException:
        return {
            "source": "ThreatFox",
            "status": "unavailable",
            "matched": None,
            "message": "ThreatFox API request timed out."
        }

    except httpx.HTTPStatusError as error:
        return {
            "source": "ThreatFox",
            "status": "error",
            "matched": None,
            "message": f"HTTP error: {error.response.status_code}"
        }

    except (httpx.RequestError, ValueError) as error:
        return {
            "source": "ThreatFox",
            "status": "error",
            "matched": None,
            "message": f"Request failed: {type(error).__name__}"
        }
