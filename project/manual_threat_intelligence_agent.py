from agents.threat_intelligence_agent import analyze_threat_intelligence


test_url = "https://example.com"

result = analyze_threat_intelligence(test_url)

print("\n========== THREAT INTELLIGENCE AGENT RESULT ==========")
print(result.model_dump())
print("======================================================")