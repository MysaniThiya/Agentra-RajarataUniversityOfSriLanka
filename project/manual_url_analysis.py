
from agents.url_analysis_agent import analyze_url

test_urls = [
    "https://www.google.com",
    "http://example.com/login",
    "http://192.168.1.1/verify-account"
]

for url in test_urls:
    print("\n" + "=" * 60)
    print("Testing URL:", url)

    result = analyze_url(url)

    print("Agent:", result.agent)
    print("Status:", result.status)
    print("Classification:", result.classification)
    print("Risk Score:", result.risk_score)
    print("Indicators:", result.indicators)
    print("Explanation:", result.explanation)
    print("Evidence:", result.evidence)
