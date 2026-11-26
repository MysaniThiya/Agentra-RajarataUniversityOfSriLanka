
from schemas.agent_result import AgentResult
from agents.risk_assessment.risk_assessment_agent import assess_risk


# Helper function to create mock agent results
def create_agent_result(agent, status, classification, indicators=None):
    return AgentResult(
        agent=agent,
        status=status,
        classification=classification,
        risk_score=None,
        indicators=indicators or [],
        explanation=f"Mock result from {agent}",
        evidence=[]
    )


# Test 1: Empty input
def test_empty_agent_results():
    result = assess_risk([])

    assert result.classification == "unknown"
    assert result.risk_level == "unknown"
    assert result.risk_score is None


# Test 2: Malicious result
def test_malicious_result():
    results = [
        create_agent_result(
            "Threat Intelligence Agent",
            "completed",
            "malicious",
            ["URL found in URLhaus."]
        )
    ]

    result = assess_risk(results)

    assert result.classification == "malicious"
    assert result.risk_level == "high"
    assert "URL found in URLhaus." in result.indicators


# Test 3: Suspicious result
def test_suspicious_result():
    results = [
        create_agent_result(
            "Email Analysis Agent",
            "completed",
            "suspicious",
            ["Urgent account verification request."]
        )
    ]

    result = assess_risk(results)

    assert result.classification == "suspicious"
    assert result.risk_level == "medium"


# Test 4: All agents report safe
def test_all_agents_safe():
    results = [
        create_agent_result("Email Analysis Agent", "completed", "safe"),
        create_agent_result("URL Analysis Agent", "completed", "safe"),
        create_agent_result("Threat Intelligence Agent", "completed", "safe")
    ]

    result = assess_risk(results)

    assert result.classification == "safe"
    assert result.risk_level == "low"


# Test 5: All agents report unknown
def test_all_agents_unknown():
    results = [
        create_agent_result("Threat Intelligence Agent", "completed", "unknown")
    ]

    result = assess_risk(results)

    assert result.classification == "unknown"
    assert result.risk_level == "unknown"


# Test 6: All agents unavailable
def test_all_agents_unavailable():
    results = [
        create_agent_result("Email Analysis Agent", "unavailable", "unknown"),
        create_agent_result("URL Analysis Agent", "unavailable", "unknown")
    ]

    result = assess_risk(results)

    assert result.classification == "unknown"
    assert result.risk_level == "unknown"


# Test 7: Conflicting results
def test_conflicting_safe_and_malicious_results():
    results = [
        create_agent_result("Email Analysis Agent", "completed", "safe"),
        create_agent_result("Threat Intelligence Agent", "completed", "malicious")
    ]

    result = assess_risk(results)

    assert result.classification == "malicious"
    assert result.risk_level == "high"
    assert "Conflicting findings were reported" in result.explanation
    assert "Email Analysis Agent reported 'safe'" in result.explanation
    assert "Threat Intelligence Agent reported 'malicious'" in result.explanation
