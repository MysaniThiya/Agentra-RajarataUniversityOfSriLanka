
from typing import Literal
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    agent: str

    status: Literal["completed", "unavailable", "error"]

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

    indicators: list[str] = Field(default_factory=list)

    explanation: str

    evidence: list[str] = Field(default_factory=list)
