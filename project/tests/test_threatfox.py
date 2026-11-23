from unittest.mock import patch, Mock

from agents.threat_intelligence.sources.threatfox import check_threatfox


@patch("agents.threat_intelligence.sources.threatfox.httpx.post")
def test_threatfox_no_match(mock_post):
    mock_response = Mock()

    mock_response.json.return_value = {
        "query_status": "no_result"
    }

    mock_post.return_value = mock_response

    result = check_threatfox("https://example.com")

    assert result["source"] == "ThreatFox"
    assert result["status"] == "completed"
    assert result["matched"] is False


@patch("agents.threat_intelligence.sources.threatfox.httpx.post")
def test_threatfox_match(mock_post):
    mock_response = Mock()

    mock_response.json.return_value = {
        "query_status": "ok",
        "data": [
            {
                "ioc": "https://example.com",
                "threat_type": "payload_delivery",
                "malware": "TestMalware"
            }
        ]
    }

    mock_post.return_value = mock_response

    result = check_threatfox("https://example.com")

    assert result["source"] == "ThreatFox"
    assert result["status"] == "completed"
    assert result["matched"] is True