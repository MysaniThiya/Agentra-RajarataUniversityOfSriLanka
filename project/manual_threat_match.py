
from unittest.mock import patch

from agents.threat_intelligence_agent import analyze_threat_intelligence


# Simulate URLhaus finding a malicious URL
urlhaus_match = {
    "source": "URLhaus",
    "status": "completed",
    "matched": True,
    "url": "https://example.com",
    "threat": "malware_download",
    "url_status": "online",
    "tags": ["test"],
    "date_added": "2026-11-23"
}

# Simulate ThreatFox finding no matching indicator
threatfox_no_match = {
    "source": "ThreatFox",
    "status": "completed",
    "matched": False,
    "message": "No matching indicator was found in ThreatFox."
}


with patch(
    "agents.threat_intelligence_agent.check_urlhaus",
    return_value=urlhaus_match
), patch(
    "agents.threat_intelligence_agent.check_threatfox",
    return_value=threatfox_no_match
):

    result = analyze_threat_intelligence("https://example.com")

    print("\n========== THREAT MATCH TEST ==========")
    print(result.model_dump())
    print("=======================================")
