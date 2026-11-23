
from typing import TypedDict, Any


class PhishGuardState(TypedDict, total=False):
    """
    Shared state for the PhishGuard AI LangGraph workflow.
    """

    # User input
    email_content: str
    submitted_url: str

    # Individual agent results
    email_result: dict[str, Any]
    url_result: dict[str, Any]
    threat_intelligence_result: dict[str, Any]

    # Combined risk assessment
    risk_assessment_result: dict[str, Any]

    # Final system response
    final_result: dict[str, Any]

    # Errors and unavailable services
    errors: list[str]
