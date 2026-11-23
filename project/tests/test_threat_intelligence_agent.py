from unittest.mock import patch

from agents.threat_intelligence_agent import analyze_threat_intelligence


def test_both_sources_no_match():

    urlhaus_result = {
        "source": "URLhaus",
        "status": "completed",
        "matched": False,
        "message": "No matching URL was found in URLhaus."
    }

    threatfox_result = {
        "source": "ThreatFox",
        "status": "completed",
        "matched": False,
        "message": "No matching indicator was found in ThreatFox."
    }

    with patch(
        "agents.threat_intelligence_agent.check_urlhaus",
        return_value=urlhaus_result
    ), patch(
        "agents.threat_intelligence_agent.check_threatfox",
        return_value=threatfox_result
    ):

        result = analyze_threat_intelligence("https://example.com")

    assert result.status == "completed"
    assert result.classification == "unknown"
    assert len(result.indicators) == 2
    assert "does not prove" in result.explanation


def test_one_source_matches():

    urlhaus_result = {
        "source": "URLhaus",
        "status": "completed",
        "matched": True,
        "url": "https://example.com",
        "threat": "malware_download",
        "url_status": "online",
        "tags": ["test"],
        "date_added": "2026-11-23"
    }

    threatfox_result = {
        "source": "ThreatFox",
        "status": "completed",
        "matched": False,
        "message": "No matching indicator was found in ThreatFox."
    }

    with patch(
        "agents.threat_intelligence_agent.check_urlhaus",
        return_value=urlhaus_result
    ), patch(
        "agents.threat_intelligence_agent.check_threatfox",
        return_value=threatfox_result
    ):

        result = analyze_threat_intelligence("https://example.com")

    assert result.status == "completed"
    assert result.classification == "malicious"
    assert len(result.evidence) > 0
    assert "URLhaus" in result.explanation


def test_partial_source_failure():

    urlhaus_result = {
        "source": "URLhaus",
        "status": "completed",
        "matched": False,
        "message": "No matching URL was found in URLhaus."
    }

    threatfox_result = {
        "source": "ThreatFox",
        "status": "unavailable",
        "matched": None,
        "message": "ThreatFox API request timed out."
    }

    with patch(
        "agents.threat_intelligence_agent.check_urlhaus",
        return_value=urlhaus_result
    ), patch(
        "agents.threat_intelligence_agent.check_threatfox",
        return_value=threatfox_result
    ):

        result = analyze_threat_intelligence("https://example.com")

    assert result.status == "completed"
    assert result.classification == "unknown"
    assert "partially completed" in result.explanation
    assert "ThreatFox" in result.explanation


def test_missing_url():

    result = analyze_threat_intelligence("")

    assert result.status == "error"
    assert result.classification == "unknown"
    assert result.risk_score is None