
from agents.threat_intelligence.url_validator import validate_url


def test_valid_https_url():
    result = validate_url("https://example.com")

    assert result["valid"] is True


def test_valid_http_url():
    result = validate_url("http://google.com")

    assert result["valid"] is True


def test_empty_url():
    result = validate_url("")

    assert result["valid"] is False


def test_localhost_url():
    result = validate_url("http://localhost")

    assert result["valid"] is False


def test_private_ip_address():
    result = validate_url("http://127.0.0.1")

    assert result["valid"] is False


def test_unsupported_protocol():
    result = validate_url("ftp://example.com")

    assert result["valid"] is False
