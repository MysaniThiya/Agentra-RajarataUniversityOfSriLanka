
from schemas.agent_result import AgentResult
from schemas.risk_assessment_result import RiskAssessmentResult


AGENT_WEIGHTS = {
    "Email Analysis Agent": 25,
    "URL Analysis Agent": 30,
    "Threat Intelligence Agent": 45,
}

CLASSIFICATION_SCORES = {
    "safe": 0,
    "suspicious": 35,
    "malicious": 100,
}


def input_was_not_provided(result: AgentResult) -> bool:
    """Identify agents that were unavailable only because input was missing."""
    explanation = result.explanation.lower()

    missing_input_messages = {
        "Email Analysis Agent": "no email content was provided",
        "URL Analysis Agent": "no url was provided",
        "Threat Intelligence Agent": "no url was provided",
    }

    expected_message = missing_input_messages.get(result.agent)

    return (
        result.status == "unavailable"
        and expected_message is not None
        and expected_message in explanation
    )


def assess_risk(agent_results: list[AgentResult]) -> RiskAssessmentResult:

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

    # Ignore agents that were not needed because their input was not provided.
    required_results = [
        result for result in agent_results
        if not input_was_not_provided(result)
    ]

    completed_results = [
        result for result in required_results
        if result.status == "completed"
    ]

    # A partially completed threat intelligence lookup is not fully complete.
    threat_intelligence_partial = any(
        result.agent == "Threat Intelligence Agent"
        and result.status == "completed"
        and "partially completed" in result.explanation.lower()
        for result in completed_results
    )

    all_required_completed = (
        bool(required_results)
        and all(result.status == "completed" for result in required_results)
        and not threat_intelligence_partial
    )

    # A completed malicious Threat Intelligence match is a confirmed match.
    threat_match = any(
        result.agent == "Threat Intelligence Agent"
        and result.status == "completed"
        and result.classification == "malicious"
        for result in completed_results
    )

    # Calculate the weighted average using available known classifications.
    weighted_total = 0
    available_weight = 0

    for result in completed_results:
        weight = AGENT_WEIGHTS.get(result.agent, 0)
        severity = CLASSIFICATION_SCORES.get(result.classification)

        if weight > 0 and severity is not None:
            weighted_total += weight * severity
            available_weight += weight

    risk_score = (
        round(weighted_total / available_weight)
        if available_weight > 0
        else None
    )

    # Collect indicators without duplicates.
    indicators = list(dict.fromkeys(
        indicator
        for result in completed_results
        for indicator in result.indicators
    ))

    # Separate the email and URL findings from threat intelligence.
    content_results = [
        result for result in completed_results
        if result.agent in {
            "Email Analysis Agent",
            "URL Analysis Agent"
        }
    ]

    has_suspicious = any(
        result.classification == "suspicious"
        for result in completed_results
    )

    has_malicious = any(
        result.classification == "malicious"
        for result in completed_results
    )

    content_results_safe = (
        bool(content_results)
        and all(result.classification == "safe" for result in content_results)
    )

    # Decide the overall classification.
    if threat_match:
        classification = "malicious"
        risk_level = "high"
        risk_score = max(risk_score or 0, 85)

    elif has_malicious:
        classification = "malicious"
        risk_level = "high"

    elif has_suspicious:
        classification = "suspicious"
        risk_level = "medium"
        risk_score = max(risk_score or 0, 20)

    elif all_required_completed and content_results_safe:
        classification = "safe"
        risk_level = "low"
        risk_score = risk_score if risk_score is not None else 0

    else:
        classification = "unknown"
        risk_level = "unknown"
        risk_score = None

    # Build the explanation.
    explanations = [
        f"{result.agent} reported '{result.classification}'."
        for result in completed_results
    ]

    if threat_match:
        explanations.append(
            "Threat Intelligence confirmed a match with a known threat indicator."
        )
    elif any(
        result.agent == "Threat Intelligence Agent"
        and result.status == "completed"
        and result.classification == "unknown"
        for result in completed_results
    ):
        explanations.append(
            "No matching threat indicator was found in the responding "
            "threat intelligence sources. This does not prove that the URL is safe."
        )

    if threat_intelligence_partial:
        explanations.append(
            "The threat intelligence lookup was only partially completed."
        )

    if not all_required_completed:
        explanations.append(
            "The assessment is incomplete because one or more required "
            "analysis agents did not complete successfully."
        )

    has_safe = any(
        result.classification == "safe"
        for result in completed_results
    )

    if has_safe and has_malicious:
        explanations.append(
            "Conflicting findings were reported by the analysis agents."
        )

    explanation = " ".join(explanations) or (
        "There was not enough completed analysis to determine the risk."
    )

    # Select recommendations.
    if classification == "malicious":
        recommendations = [
            "Do not click the link or open attachments.",
            "Do not enter passwords or other sensitive information.",
            "Report the message to your security team.",
            "Treat the URL as potentially malicious and block or quarantine it "
            "according to your organization's security policy."
        ]

    elif classification == "suspicious":
        recommendations = [
            "Avoid clicking links until they are verified.",
            "Do not share passwords or other sensitive information.",
            "Verify the message using an official communication channel."
        ]

    elif classification == "safe":
        recommendations = [
            "No suspicious signals were detected by the completed analysis agents.",
            "No matching threat indicator was found in the responding threat "
            "intelligence sources, but this does not guarantee safety.",
            "Continue following normal security practices."
        ]

    else:
        recommendations = [
            "Do not assume the message or URL is safe.",
            "Retry unavailable or failed analysis agents.",
            "Avoid interacting with suspicious links until the assessment is complete."
        ]

    return RiskAssessmentResult(
        classification=classification,
        risk_score=risk_score,
        risk_level=risk_level,
        indicators=indicators,
        explanation=explanation,
        recommendations=recommendations
    )
