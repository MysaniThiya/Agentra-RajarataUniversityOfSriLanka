
from schemas.agent_result import AgentResult


# Scenario 1: All three agents report safe
all_safe = [
    AgentResult(
        agent="Email Analysis Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No suspicious email content detected.",
        evidence=[]
    ),
    AgentResult(
        agent="URL Analysis Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No suspicious URL characteristics detected.",
        evidence=[]
    ),
    AgentResult(
        agent="Threat Intelligence Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No matching threat record was found.",
        evidence=["URLhaus returned no_results."]
    )
]


# Scenario 2: Two agents report suspicious findings
two_suspicious = [
    AgentResult(
        agent="Email Analysis Agent",
        status="completed",
        classification="suspicious",
        indicators=["Urgent account verification request."],
        explanation="The email uses urgent language.",
        evidence=["The recipient is asked to verify their account."]
    ),
    AgentResult(
        agent="URL Analysis Agent",
        status="completed",
        classification="suspicious",
        indicators=["Possible domain impersonation."],
        explanation="The domain resembles a legitimate service.",
        evidence=["The domain name contains a brand-like variation."]
    ),
    AgentResult(
        agent="Threat Intelligence Agent",
        status="completed",
        classification="unknown",
        indicators=[],
        explanation="No matching threat record was found.",
        evidence=["No URLhaus or ThreatFox match."]
    )
]


# Scenario 3: Confirmed malicious threat intelligence match
confirmed_threat_match = [
    AgentResult(
        agent="Email Analysis Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No suspicious email content detected.",
        evidence=[]
    ),
    AgentResult(
        agent="URL Analysis Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No suspicious URL characteristics detected.",
        evidence=[]
    ),
    AgentResult(
        agent="Threat Intelligence Agent",
        status="completed",
        classification="malicious",
        indicators=["URL found in URLhaus."],
        explanation="A confirmed malicious URL match was found.",
        evidence=["Confirmed exact URL match in URLhaus."]
    )
]


# Scenario 4: Email reports malicious, other agents report safe
email_malicious = [
    AgentResult(
        agent="Email Analysis Agent",
        status="completed",
        classification="malicious",
        indicators=["Credential theft attempt detected."],
        explanation="The email contains strong phishing indicators.",
        evidence=["The message requests account credentials."]
    ),
    AgentResult(
        agent="URL Analysis Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No suspicious URL characteristics detected.",
        evidence=[]
    ),
    AgentResult(
        agent="Threat Intelligence Agent",
        status="completed",
        classification="unknown",
        indicators=[],
        explanation="No matching threat record was found.",
        evidence=["No matching database record."]
    )
]


# Scenario 5: One agent unavailable
one_agent_unavailable = [
    AgentResult(
        agent="Email Analysis Agent",
        status="completed",
        classification="safe",
        indicators=[],
        explanation="No suspicious email content detected.",
        evidence=[]
    ),
    AgentResult(
        agent="URL Analysis Agent",
        status="unavailable",
        classification="unknown",
        indicators=[],
        explanation="URL analysis service is unavailable.",
        evidence=[]
    ),
    AgentResult(
        agent="Threat Intelligence Agent",
        status="completed",
        classification="unknown",
        indicators=[],
        explanation="No matching threat record was found.",
        evidence=[]
    )
]


# Scenario 6: All agents unavailable
all_unavailable = [
    AgentResult(
        agent="Email Analysis Agent",
        status="unavailable",
        classification="unknown",
        indicators=[],
        explanation="Email analysis service is unavailable.",
        evidence=[]
    ),
    AgentResult(
        agent="URL Analysis Agent",
        status="unavailable",
        classification="unknown",
        indicators=[],
        explanation="URL analysis service is unavailable.",
        evidence=[]
    ),
    AgentResult(
        agent="Threat Intelligence Agent",
        status="unavailable",
        classification="unknown",
        indicators=[],
        explanation="Threat intelligence services are unavailable.",
        evidence=[]
    )
]
