
import ipaddress
from urllib.parse import urlsplit


def validate_url(url: str) -> dict:
    """
    Validate a URL before sending it to threat intelligence sources.
    """

    # 1. Check whether input is provided
    if not isinstance(url, str) or not url.strip():
        return {
            "valid": False,
            "message": "URL is empty or invalid."
        }

    url = url.strip()

    try:
        # 2. Extract URL components
        parsed_url = urlsplit(url)

        # 3. Allow only HTTP and HTTPS
        if parsed_url.scheme.lower() not in ("http", "https"):
            return {
                "valid": False,
                "message": "Only HTTP and HTTPS URLs are supported."
            }

        # 4. Check hostname
        hostname = parsed_url.hostname

        if not hostname:
            return {
                "valid": False,
                "message": "URL does not contain a valid hostname."
            }

        # 5. Reject URLs containing username/password
        if parsed_url.username or parsed_url.password:
            return {
                "valid": False,
                "message": "URLs containing credentials are not allowed."
            }

        # 6. Reject localhost
        if hostname.lower() == "localhost" or hostname.lower().endswith(".localhost"):
            return {
                "valid": False,
                "message": "Localhost URLs are not allowed."
            }

        # 7. Check whether hostname is an IP address
        try:
            ip = ipaddress.ip_address(hostname)

            if not ip.is_global:
                return {
                    "valid": False,
                    "message": "Private or non-public IP addresses are not allowed."
                }

        except ValueError:
            # It is a domain name, not an IP address.
            pass

        # 8. Check for a valid port
        try:
            port = parsed_url.port
        except ValueError:
            return {
                "valid": False,
                "message": "URL contains an invalid port."
            }

        return {
            "valid": True,
            "message": "URL format is valid.",
            "url": url,
            "hostname": hostname,
            "port": port
        }

    except ValueError:
        return {
            "valid": False,
            "message": "Unable to parse the URL."
        }
