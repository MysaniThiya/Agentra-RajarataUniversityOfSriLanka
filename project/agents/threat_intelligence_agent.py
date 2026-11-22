
from schemas.agent_result import AgentResult


def analyze_threat_intelligence(url: str) -> AgentResult:
    """
    Initial Threat Intelligence Agent.
    External threat-intelligence API integration
    will be added in the next development stage.
    """

    if not url or not url.strip():
        return AgentResult(
            agent="Threat Intelligence Agent",
            status="error",
            classification="unknown",
            risk_score=None,
            indicators=["URL was not provided"],
            explanation="Cannot perform threat intelligence lookup without a URL.",
            evidence=[]
        )

    return AgentResult(
        agent="Threat Intelligence Agent",
        status="unavailable",
        classification="unknown",
        risk_score=None,
        indicators=["External threat intelligence lookup is not connected yet"],
        explanation=(
            "The agent received the URL, but no external threat "
            "intelligence source has been connected."
        ),
        evidence=[]
    )
