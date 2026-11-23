
from schemas.agent_result import AgentResult

from agents.threat_intelligence.sources.urlhaus import check_urlhaus
from agents.threat_intelligence.sources.threatfox import check_threatfox


def analyze_threat_intelligence(url: str) -> AgentResult:
    """
    Main Threat Intelligence Agent.

    Checks the submitted URL against URLhaus and ThreatFox,
    then combines their results into one AgentResult.
    """

    # 1. Check whether a URL was provided
    if not isinstance(url, str) or not url.strip():
        return AgentResult(
            agent="Threat Intelligence Agent",
            status="error",
            classification="unknown",
            risk_score=None,
            indicators=["URL was not provided"],
            explanation="Cannot perform threat intelligence lookup without a URL.",
            evidence=[]
        )

    # 2. Query both threat intelligence sources
    urlhaus_result = check_urlhaus(url)
    threatfox_result = check_threatfox(url)

    # Store both results together for processing
    source_results = [
        urlhaus_result,
        threatfox_result
    ]

    # 3. Prepare the combined result
    indicators = []
    evidence = []

    matched_sources = []
    completed_sources = []

    for result in source_results:

        source = result.get("source", "Unknown source")
        status = result.get("status")
        matched = result.get("matched")

        # Track sources that successfully responded
        if status == "completed":
            completed_sources.append(source)

        # Record positive matches
        if matched is True:
            matched_sources.append(source)

            indicators.append(
                f"{source}: Submitted URL matched a known threat indicator."
            )

            # Preserve details returned by the source
            if source == "URLhaus":
                evidence.append(
                    f"URLhaus details: {result}"
                )

            elif source == "ThreatFox":
                evidence.append(
                    f"ThreatFox details: {result.get('results', [])}"
                )

        # Record successful searches with no matches
        elif matched is False:
            indicators.append(
                f"{source}: No matching indicator was found."
            )

        # Record unavailable or failed sources
        else:
            indicators.append(
                f"{source}: {result.get('message', 'Lookup was unsuccessful.')}"
            )

    # 4. Determine the overall status
    if completed_sources:
        overall_status = "completed"

    elif any(result.get("status") == "error" for result in source_results):
        overall_status = "error"

    else:
        overall_status = "unavailable"

    # 5. Determine the overall classification
    if matched_sources:
        classification = "malicious"
        explanation = (
            "The submitted URL matched a threat indicator in: "
            + ", ".join(matched_sources)
            + "."
        )

    else:
        classification = "unknown"

        failed_sources = [
            result["source"]
            for result in source_results
            if result.get("status") != "completed"
        ]

        if failed_sources:
            explanation = (
                "The threat intelligence lookup was partially completed. "
                "Some sources were unavailable or returned errors: "
                + ", ".join(failed_sources)
                + ". No matching indicator was found in the sources "
                "that responded successfully. This does not prove that "
                "the URL is safe."
            )
        else:
            explanation = (
                "No matching threat indicator was found in the "
                "sources that responded successfully. This does not "
                "prove that the URL is safe."
            )

    # 6. Return the combined result using the shared schema
    return AgentResult(
        agent="Threat Intelligence Agent",
        status=overall_status,
        classification=classification,
        risk_score=None,
        indicators=indicators,
        explanation=explanation,
        evidence=evidence
    )
