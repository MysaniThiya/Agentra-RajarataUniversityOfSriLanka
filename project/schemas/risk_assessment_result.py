from typing import Literal
from pydantic import BaseModel, Field


class RiskAssessmentResult(BaseModel):

    classification: Literal[
        "safe",
        "suspicious",
        "malicious",
        "unknown"
    ]

    risk_score: int | None = Field(
        default=None,
        ge=0,
        le=100
    )

    risk_level: Literal[
        "low",
        "medium",
        "high",
        "unknown"
    ]

    indicators: list[str] = Field(default_factory=list)

    explanation: str

    recommendations: list[str] = Field(default_factory=list)