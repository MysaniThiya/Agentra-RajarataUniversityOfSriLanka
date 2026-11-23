from agents.threat_intelligence.sources.urlhaus import check_urlhaus

test_urls = [
    "https://example.com",
    "http://localhost",
    "http://127.0.0.1",
    "not-a-valid-url"
]

for url in test_urls:

    print("\nURL:", url)

    result = check_urlhaus(url)

    print("URLhaus Result:", result)