from agents.threat_intelligence.url_validator import validate_url


test_urls = [
    "https://example.com",
    "http://google.com",
    "",
    "ftp://example.com",
    "http://localhost",
    "http://127.0.0.1",
    "not-a-valid-url"
]

for url in test_urls:
    result = validate_url(url)

    print("\nURL:", url)
    print("Result:", result)