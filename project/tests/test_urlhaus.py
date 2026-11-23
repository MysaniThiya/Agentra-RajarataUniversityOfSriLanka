from unittest.mock import patch, Mock

from agents.threat_intelligence.sources.urlhaus import check_urlhaus


@patch("agents.threat_intelligence.sources.urlhaus.httpx.post")
def test_urlhaus_no_match(mock_post):
    mock_response = Mock()

    mock_response.json.return_value = {
        "query_status": "no_results"
    }

    mock_post.return_value = mock_response

    result = check_urlhaus("https://example.com")

    assert result["source"] == "URLhaus"
    assert result["status"] == "completed"
    assert result["matched"] is False


@patch("agents.threat_intelligence.sources.urlhaus.httpx.post")
def test_urlhaus_match(mock_post):
    mock_response = Mock()

    mock_response.json.return_value = {
        "query_status": "ok",
        "url": "https://example.com",
        "threat": "malware_download",
        "url_status": "online",
        "tags": ["test"],
        "date_added": "2026-11-23"
    }

    mock_post.return_value = mock_response

    result = check_urlhaus("https://example.com")

    assert result["source"] == "URLhaus"
    assert result["status"] == "completed"
    assert result["matched"] is True