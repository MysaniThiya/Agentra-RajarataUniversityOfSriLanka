# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator
from typing import Optional

from orchestration.graph import phishguard_graph


# Create the PhishGuard AI application
app = FastAPI(
    title="PhishGuard AI",
    description="Multi-Agent AI System for Phishing Detection and Cyber Threat Investigation",
    version="1.0.0"
)

# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request schema
class AnalysisRequest(BaseModel):
    email_content: Optional[str] = None
    submitted_url: Optional[str] = None

    @model_validator(mode="after")
    def validate_input(self):
        if not self.email_content and not self.submitted_url:
            raise ValueError(
                "Please provide email content, a URL, or both."
            )
        return self


# Welcome endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to PhishGuard AI",
        "status": "Backend is running successfully"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "PhishGuard AI"
    }


# Main analysis endpoint
@app.post("/analyze")
def analyze(request: AnalysisRequest):

    try:
        input_data = request.model_dump(exclude_none=True)

        result = phishguard_graph.invoke(input_data)

        return {
            "message": "Analysis completed successfully",
            "results": {
                "email": result.get("email_result"),
                "url": result.get("url_result"),
                "threat_intelligence": result.get(
                    "threat_intelligence_result"
                ),
                "risk_assessment": result.get(
                    "risk_assessment_result"
                )
            }
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Analysis failed. Please try again."
        ) from error