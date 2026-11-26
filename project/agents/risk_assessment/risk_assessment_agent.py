
from schemas.agent_result import AgentResult
from schemas.risk_assessment_result import RiskAssessmentResult


# Each agent's contribution to the final risk score
AGENT_WEIGHTS = {
    "Email Analysis Agent": 25,
    "URL Analysis Agent": 30,
    "Threat Intelligence Agent": 45,
}

# Convert classifications into numerical scores
CLASSIFICATION_SCORES = {
    "safe": 0,
    "suspicious": 35,
    "malicious": 100,
}


def assess_risk(agent_results: list[AgentResult]) -> RiskAssessmentResult:

    # Step 1: Handle empty input
    if not agent_results:
        return RiskAssessmentResult(
            classification="unknown",
            risk_score=None,
            risk_level="unknown",
            explanation="No agent results were provided for risk assessment.",
            recommendations=[
                "Run the analysis agents before making a security decision."
            ]
        )

    # Step 2: Keep only successfully completed results
    completed_results = [
        result for result in agent_results
        if result.status == "completed"
    ]

    # Step 3: Check for a confirmed Threat Intelligence match
    threat_match = any(
        result.agent == "Threat Intelligence Agent"
        and result.status == "completed"
        and result.classification == "malicious"
        for result in completed_results
    )

    # Step 4: Calculate weighted score using available agents only
    weighted_total = 0
    available_weight = 0

    for result in completed_results:

        weight = AGENT_WEIGHTS.get(result.agent, 0)
        severity = CLASSIFICATION_SCORES.get(result.classification)

        # Ignore unknown classifications and unrecognized agents
        if weight > 0 and severity is not None:
            weighted_total += weight * severity
            available_weight += weight

    # Calculate the proportional weighted average
    if available_weight > 0:
        risk_score = round(weighted_total / available_weight)
    else:
        risk_score = None

    # Step 5: Collect indicators without duplicates
    indicators = list(dict.fromkeys(
        indicator
        for result in completed_results
        for indicator in result.indicators
    ))

    # Step 6: Check whether all three agents completed
    completed_agent_names = {
        result.agent for result in completed_results
    }

    all_agents_completed = all(
        agent in completed_agent_names
        for agent in AGENT_WEIGHTS
    )

    all_agents_safe = (
        all_agents_completed
        and all(
            result.classification == "safe"
            for result in completed_results
            if result.agent in AGENT_WEIGHTS
        )
    )

    # Step 7: Decide the final classification
    if threat_match:
        classification = "malicious"
        risk_level = "high"
        risk_score = max(risk_score or 0, 85)

    elif risk_score is None:
        classification = "unknown"
        risk_level = "unknown"

    elif risk_score >= 50:
        classification = "malicious"
        risk_level = "high"

    elif risk_score >= 20:
        classification = "suspicious"
        risk_level = "medium"

    elif all_agents_safe:
        classification = "safe"
        risk_level = "low"

    else:
        # A score of zero from incomplete analysis is not enough
        # to conclude that the input is safe.
        classification = "unknown"
        risk_level = "unknown"
        risk_score = None

    # Step 8: Explain the combined findings
    explanations = [
        f"{result.agent} reported '{result.classification}'."
        for result in completed_results
    ]

    # Check for conflicting findings
    has_safe = any(
        result.classification == "safe"
        for result in completed_results
    )

    has_malicious = any(
        result.classification == "malicious"
        for result in completed_results
    )

    if has_safe and has_malicious:
        explanations.append(
            "Conflicting findings were reported by the analysis agents."
        )

    # Explain incomplete assessment
    if not all_agents_completed:
        explanations.append(
            "The assessment is incomplete because one or more agents "
            "did not provide a completed result."
        )

    explanation = " ".join(explanations)

    # Step 9: Select recommendations
    if classification == "malicious":
        recommendations = [
            "Do not click the link or open attachments.",
            "Do not enter passwords or other sensitive information.",
            "Report the message to your security team.",
            "Block the confirmed malicious URL where appropriate."
        ]

    elif classification == "suspicious":
        recommendations = [
            "Avoid clicking links until they are verified.",
            "Do not share sensitive information.",
            "Verify the message using an official communication channel."
        ]

    elif classification == "safe":
        recommendations = [
            "No suspicious indicators were reported by the completed agents.",
            "Continue following normal security practices."
        ]

    else:
        recommendations = [
            "Do not assume the message is safe.",
            "Retry unavailable agents or investigate manually.",
            "Avoid interacting with suspicious links until the assessment is complete."
        ]

    # Step 10: Return the final structured result
    return RiskAssessmentResult(
        classification=classification,
        risk_score=risk_score,
        risk_level=risk_level,
        indicators=indicators,
        explanation=explanation,
        recommendations=recommendations
    )
