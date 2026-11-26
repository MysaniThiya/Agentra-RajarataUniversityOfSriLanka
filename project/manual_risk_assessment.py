
from agents.risk_assessment.risk_assessment_agent import assess_risk
from schemas.agent_result import AgentResult


def create_agent_result(agent, status, classification):
    return AgentResult(
        agent=agent,
        status=status,
        classification=classification,
        explanation=f"{agent} reported {classification}."
    )


def run_test_case(name, email, url, threat_intel):

    results = [
        create_agent_result(
            "Email Analysis Agent",
            email[0],
            email[1]
        ),
        create_agent_result(
            "URL Analysis Agent",
            url[0],
            url[1]
        ),
        create_agent_result(
            "Threat Intelligence Agent",
            threat_intel[0],
            threat_intel[1]
        )
    ]

    result = assess_risk(results)

    print("\n" + "=" * 55)
    print(f"TEST CASE: {name}")
    print("=" * 55)

    print(result.model_dump_json(indent=4))


# Test case 1: All agents safe
run_test_case(
    "All Agents Safe",
    ("completed", "safe"),
    ("completed", "safe"),
    ("completed", "safe")
)


# Test case 2: Email suspicious
run_test_case(
    "Suspicious Email",
    ("completed", "suspicious"),
    ("completed", "safe"),
    ("completed", "safe")
)


# Test case 3: URL malicious
run_test_case(
    "Malicious URL",
    ("completed", "safe"),
    ("completed", "malicious"),
    ("completed", "safe")
)


# Test case 4: Confirmed threat intelligence match
run_test_case(
    "Confirmed Threat Match",
    ("completed", "safe"),
    ("completed", "safe"),
    ("completed", "malicious")
)


# Test case 5: Threat intelligence unknown
run_test_case(
    "Threat Intelligence Unknown",
    ("completed", "safe"),
    ("completed", "safe"),
    ("completed", "unknown")
)


# Test case 6: One agent unavailable
run_test_case(
    "Email Agent Unavailable",
    ("unavailable", "unknown"),
    ("completed", "safe"),
    ("completed", "safe")
)


# Test case 7: Conflicting findings
run_test_case(
    "Conflicting Findings",
    ("completed", "safe"),
    ("completed", "malicious"),
    ("completed", "safe")
)


# Test case 8: All agents unavailable
run_test_case(
    "All Agents Unavailable",
    ("unavailable", "unknown"),
    ("unavailable", "unknown"),
    ("unavailable", "unknown")
)
