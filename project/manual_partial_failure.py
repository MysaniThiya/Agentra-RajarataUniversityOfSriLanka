
from unittest.mock import patch

from agents.threat_intelligence_agent import analyze_threat_intelligence


# Simulated successful URLhaus response
urlhaus_success = {
    "source": "URLhaus",
    "status": "completed",
    "matched": False,
    "message": "No matching URL was found in URLhaus."
}

# Simulated failed ThreatFox response
threatfox_failure = {
    "source": "ThreatFox",
    "status": "unavailable",
    "matched": None,
    "message": "ThreatFox API request timed out."
}


# Replace the real API functions with simulated responses
with patch(
    "agents.threat_intelligence_agent.check_urlhaus",
    return_value=urlhaus_success
), patch(
    "agents.threat_intelligence_agent.check_threatfox",
    return_value=threatfox_failure
):

    result = analyze_threat_intelligence("https://example.com")

    print("\n========== PARTIAL FAILURE TEST ==========")
    print(result.model_dump())
    print("==========================================")
