# Agentra-RajarataUniversityOfSriLanka
Innodata AI Catalyst '26 – University Track Project
# PhishGuard AI

### Intelligent Phishing Detection & Investigation

PhishGuard AI is an AI-powered phishing detection system that analyzes  emails and URLs using machine learning, threat intelligence, and a multi-agent architecture.

Developed for Innodata AI Catalyst '26 – University Track: Multi-Agent AI for Global Problems.

## Project Overview

PhishGuard AI uses specialized AI agents to detect potential phishing threats, assess security risks, and provide investigation findings and recommendations.

The system helps users identify suspicious activities and make informed security decisions.


### Intelligent Phishing Detection & Investigation

PhishGuard AI is an AI-powered phishing detection system that analyzes  emails and URLs using machine learning, threat intelligence, and a multi-agent architecture.

Developed for Innodata AI Catalyst '26 – University Track: Multi-Agent AI for Global Problems.

## Project Overview

PhishGuard AI uses specialized AI agents to detect potential phishing threats, assess security risks, and provide investigation findings and recommendations.

The system helps users identify suspicious activities and make informed security decisions.

## Key Features

- Email Analysis: Detects suspicious emails using machine learning.
- URL Analysis: Identifies potentially malicious URLs.
- Threat Intelligence: Checks URLs using URLhaus and ThreatFox.
- Multi-Agent Architecture: Uses specialized agents for threat analysis.
- Risk Assessment: Calculates risk scores and classifies threats.
- Investigation Findings: Displays evidence and analysis results.
- Security Recommendations: Suggests actions based on detected risks.
- Interactive Dashboard: Provides a simple interface to analyze emails and URLs.

Multi-Agent Architecture
- PhishGuard AI consists of four specialized agents coordinated through LangGraph.
Agent	Responsibility
- Email Analysis Agent	Analyzes email content and identifies suspicious or malicious characteristics.
- URL Analysis Agent	Examines URL features and predicts potential malicious activity.
Threat Intelligence Agent	Checks URLs against external threat intelligence databases.
- Risk Assessment Agent	Aggregates agent results and determines the overall risk classification.

  How It Works
1. The user submits an email or URL through the web application.
2. The backend receives the submitted information through the FastAPI API.
3. The relevant analysis agents process the available input.
4. The Threat Intelligence Agent checks submitted URLs against external threat intelligence sources.
5. The Risk Assessment Agent evaluates the available agent findings.
6. The system generates an overall classification, risk score, explanation, indicators, and recommendations.
7. The frontend displays the investigation results.

Risk Classifications :Safe, Suspicious, Malicious, Unknown
Technology Stack
Frontend
- React.js
- TypeScript
- Vite
- Tailwind CSS
Backend
- Python 3.11
- FastAPI
- LangGraph
- Pydantic
Artificial Intelligence & Machine Learning
- Scikit-learn
- Logistic Regression
- TF-IDF Vectorization
- XGBoost
- Machine Learning-based classification
Threat Intelligence
- URLhaus
- ThreatFox
Development Tools
- Visual Studio Code
- Git
- GitHub
- Postman / FastAPI Swagger UI

Project Structure
Agentra-RajarataUniversityOfSriLanka/
│
├── project/
│   ├── agents/
│   │   ├── email_analysis_agent.py
│   │   ├── url_analysis_agent.py
│   │   ├── threat_intelligence_agent.py
│   │   └── risk_assessment/
│   │       └── risk_assessment_agent.py
│   │
│   ├── orchestration/
│   │   ├── graph.py
│   │   └── state.py
│   │
│   ├── schemas/
│   │   ├── agent_result.py
│   │   └── risk_assessment_result.py
│   │
│   ├── models/
│   │
│   ├── Frontend/
│   │   ├── src/
│   │   ├── public/
│   │   └── package.json
│   │
│   ├── main.py
│   └── requirements.txt
│
├── docs/
│   └── Proposal.docx
│
└── README.md


Installation and Setup
Follow these steps to run PhishGuard AI locally.
Prerequisites
Make sure you have installed:
- Python 3.11
- Node.js and npm
- Git
- Visual Studio Code (recommended)
1. Clone the Repository
git clone https://github.com/MysaniThiya/Agentra-RajarataUniversity

Navigate to the project directory:
cd Agentra-RajarataUniversityOfSriLanka/project

2. Set Up the Backend
Create a Python virtual environment:
python -m venv .venv

Activate the virtual environment on Windows PowerShell:
.\.venv\Scripts\Activate.ps1

Install the required dependencies:
pip install -r requirements.txt

3. Configure Environment Variables
Create a .env file in the backend project directory.

Add the API credentials required by the threat intelligence integrations, following the variable names and configuration in the project source code.

Important: Never commit API keys, passwords, or other sensitive credentials to GitHub.
4. Start the Backend Server
From the project directory, run:
uvicorn main:app --reload
The backend API will be available at:
http://127.0.0.1:8000

Access the interactive API documentation:

http://127.0.0.1:8000/docs
5. Set Up the Frontend
Open a second terminal and navigate to the frontend directory:
cd Frontend
Install frontend dependencies:
npm install
Start the development server:
npm run dev
The frontend will be available at:

http://localhost:5173

Important: Keep both the backend and frontend servers running while using the application.
API Usage
Analyze Email or URL
Endpoint:
POST /analyze
Example request – Email analysis:
{
  "email_content": "Your account will be suspended. Please verify your credentials immediately."
}
Example request – URL analysis:
{
  "submitted_url": "https://example.com"
}
Example response structure:
{
  "message": "Analysis completed successfully",
  "results": {
    "email": {},
    "url": {},
    "threat_intelligence": {},
    "risk_assessment": {}
  }
}
The response includes the results from the available analysis agents and the overall risk assessment.
Security Considerations
- Do not submit real passwords, banking credentials, or other sensitive personal information for testing.
- Do not open suspicious URLs.
- Keep API keys and environment variables private.
- A missing threat intelligence match does not guarantee that a URL is safe.
- Risk classifications depend on the available analysis results and the performance of the underlying models.
Development Team
Project: PhishGuard AI
Competition: Innodata AI Catalyst '26
Track: University Track – Multi-Agent AI for Global Problems
Institution: Rajarata University of Sri Lanka

Team: Agentra

Developed collaboratively by a team of four members.
Project Goal
Our goal is to make phishing detection more accessible and understandable by combining machine learning, multi-agent collaboration, and threat intelligence into a unified investigation platform.







