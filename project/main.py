
from fastapi import FastAPI

# Create the PhishGuard AI application
app = FastAPI(
    title="PhishGuard AI",
    description="Multi-Agent AI System for Phishing Detection and Cyber Threat Investigation",
    version="1.0.0"
)


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
