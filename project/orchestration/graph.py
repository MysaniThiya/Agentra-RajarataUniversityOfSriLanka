
from langgraph.graph import StateGraph, START, END

from orchestration.state import PhishGuardState
from agents.threat_intelligence_agent import analyze_threat_intelligence
from schemas.agent_result import AgentResult
from agents.risk_assessment.risk_assessment_agent import assess_risk


# 1. Threat Intelligence Agent
def threat_intelligence_node(state: PhishGuardState):
    url = state.get("submitted_url", "")

    if not url:
        return {
            "threat_intelligence_result": {
                "agent": "Threat Intelligence Agent",
                "status": "unavailable",
                "classification": "unknown",
                "risk_score": None,
                "indicators": [],
                "explanation": "No URL was provided.",
                "evidence": []
            }
        }

    try:
        result = analyze_threat_intelligence(url)
        return {
            "threat_intelligence_result": result.model_dump()
        }

    except Exception as error:
        return {
            "threat_intelligence_result": {
                "agent": "Threat Intelligence Agent",
                "status": "error",
                "classification": "unknown",
                "risk_score": None,
                "indicators": [],
                "explanation": "Threat intelligence analysis failed.",
                "evidence": []
            },
            "errors": [str(error)]
        }


# 2. Temporary Email Agent
def email_agent_node(state: PhishGuardState):
    return {
        "email_result": {
            "agent": "Email Agent",
            "status": "unavailable",
            "classification": "unknown",
            "risk_score": None,
            "indicators": [],
            "explanation": "Email Agent integration is pending.",
            "evidence": []
        }
    }


# 3. Temporary URL Agent
def url_agent_node(state: PhishGuardState):
    return {
        "url_result": {
            "agent": "URL Agent",
            "status": "unavailable",
            "classification": "unknown",
            "risk_score": None,
            "indicators": [],
            "explanation": "URL Agent integration is pending.",
            "evidence": []
        }
    }


# 4. Risk Assessment Agent
def risk_assessment_node(state: PhishGuardState):

    # Collect results from the three analysis agents
    raw_results = [
        state.get("email_result", {}),
        state.get("url_result", {}),
        state.get("threat_intelligence_result", {})
    ]

    # Convert valid agent results into AgentResult objects
    agent_results = []

    for result in raw_results:
        if result:
            agent_results.append(
                AgentResult.model_validate(result)
            )

    # Perform combined risk assessment
    risk_result = assess_risk(agent_results)

    return {
        "risk_assessment_result": risk_result.model_dump()
    }


# 5. Build LangGraph Workflow
builder = StateGraph(PhishGuardState)

builder.add_node("email_agent", email_agent_node)
builder.add_node("url_agent", url_agent_node)
builder.add_node("threat_intelligence", threat_intelligence_node)
builder.add_node("risk_assessment", risk_assessment_node)


# Start all three analysis agents in parallel
builder.add_edge(START, "email_agent")
builder.add_edge(START, "url_agent")
builder.add_edge(START, "threat_intelligence")

builder.add_edge(
    ["email_agent", "url_agent", "threat_intelligence"],
    "risk_assessment"
)

builder.add_edge("risk_assessment", END)


# 6. Compile Graph
phishguard_graph = builder.compile()
