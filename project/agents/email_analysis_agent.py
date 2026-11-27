
import re
from pathlib import Path
from email.utils import parseaddr

import joblib

from schemas.agent_result import AgentResult


# 1. LOAD TRAINED MODEL AND TF-IDF VECTORIZER

PROJECT_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = PROJECT_DIR / "models" / "email_analysis_model"

MODEL_PATH = MODEL_DIR / "logistic_regression_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"

model = None
vectorizer = None
MODEL_LOAD_ERROR = None

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("Email Analysis Agent initialized successfully!")

except Exception as error:
    MODEL_LOAD_ERROR = str(error)


# 2. CLASSIFICATION MAPPINGS

CLASSIFICATION_MAPPING = {
    0: "safe",
    1: "malicious",
    2: "suspicious"
}

LABEL_NAMES = {
    0: "Ham (Legitimate)",
    1: "Phishing",
    2: "Spam"
}


# 3. EMAIL BODY ANALYSIS

def analyze_email_content(email_text):

    indicators = []
    evidence = []

    patterns = {
        "Urgent language": [
            r"\bimmediately\b",
            r"\burgent\b",
            r"\bact now\b",
            r"\bwithin 24 hours\b",
            r"\bas soon as possible\b",
            r"\bwithout delay\b"
        ],

        "Account suspension warning": [
            r"\baccount\b.{0,60}\b(suspend|suspended|blocked|disabled|locked)\b",
            r"\b(suspend|suspended|blocked|disabled|locked)\b.{0,60}\baccount\b"
        ],

        "Credential request": [
            r"\b(password|login credentials|passcode|OTP)\b",
            r"\bverify\b.{0,60}\b(account|password|identity|credentials)\b"
        ],

        "Suspicious link instruction": [
            r"\b(click|follow|visit|open)\b.{0,60}\b(link|URL|website|below)\b"
        ],

        "Financial information request": [
            r"\b(bank details|credit card|card number|bank account details)\b"
        ]
    }

    sentences = re.split(r"(?<=[.!?])\s+", email_text)

    for indicator, expressions in patterns.items():

        for expression in expressions:

            for sentence in sentences:

                if re.search(expression, sentence, re.IGNORECASE):

                    indicators.append(indicator)
                    evidence.append(sentence.strip())
                    break

            if indicator in indicators:
                break

    return {
        "indicators": list(dict.fromkeys(indicators)),
        "evidence": list(dict.fromkeys(evidence))
    }


# 4. EMAIL SUBJECT ANALYSIS

def analyze_email_subject(subject):

    indicators = []
    evidence = []

    subject_patterns = {
        "Urgent subject line": [
            r"\burgent\b",
            r"\bimmediately\b",
            r"\bact now\b",
            r"\bimportant action required\b"
        ],

        "Account warning in subject": [
            r"\baccount\b.{0,50}\b(suspend|suspended|blocked|locked|verify)\b"
        ],

        "Sensitive information request": [
            r"\b(password|credentials|OTP|verify your identity)\b"
        ],

        "Unusual financial notification": [
            r"\b(payment|bank|invoice|refund|transaction)\b"
        ]
    }

    for indicator, expressions in subject_patterns.items():

        for expression in expressions:

            if re.search(expression, subject, re.IGNORECASE):

                indicators.append(indicator)
                evidence.append(subject.strip())
                break

    return {
        "indicators": list(dict.fromkeys(indicators)),
        "evidence": list(dict.fromkeys(evidence))
    }


# 5. EMAIL SENDER ANALYSIS

def analyze_email_sender(sender):

    indicators = []
    evidence = []

    sender = sender.strip()

    # Ignore sender analysis when no sender is provided.
    if not sender:
        return {
            "indicators": [],
            "evidence": []
        }

    # Extract address from formats such as:
    # Security Team <security@example.com>
    address = parseaddr(sender)[1]

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(email_pattern, address):

        indicators.append(
            "Invalid or malformed sender address"
        )

        evidence.append(
            f"Sender address: {sender}"
        )

    else:

        local_part, domain = address.rsplit("@", 1)

        if domain.count(".") > 3:

            indicators.append(
                "Unusually complex sender domain"
            )

            evidence.append(
                f"Sender domain: {domain}"
            )

    return {
        "indicators": list(dict.fromkeys(indicators)),
        "evidence": list(dict.fromkeys(evidence))
    }


# 6. COMPLETE EMAIL ANALYSIS

def analyze_email(email_data):

    try:

        # Accept either a complete email dictionary
        # or plain email body text.

        if isinstance(email_data, str):

            email_data = {
                "sender": "",
                "subject": "",
                "body": email_data
            }

        if not isinstance(email_data, dict):
            raise ValueError(
                "Email input must be a dictionary or string."
            )

        sender = str(email_data.get("sender") or "").strip()
        subject = str(email_data.get("subject") or "").strip()
        body = str(email_data.get("body") or "").strip()

        if not body:
            raise ValueError("Email body cannot be empty.")

        # Check whether the trained model loaded.

        if model is None or vectorizer is None:

            return AgentResult(
                agent="Email Analysis Agent",
                status="unavailable",
                classification="unknown",
                risk_score=None,
                indicators=[],
                explanation=(
                    f"Email model could not be loaded: "
                    f"{MODEL_LOAD_ERROR}"
                ),
                evidence=[]
            )

        
        email_tfidf = vectorizer.transform([body])

        prediction = int(model.predict(email_tfidf)[0])

        probabilities = model.predict_proba(email_tfidf)[0]

        if prediction not in CLASSIFICATION_MAPPING:
            raise ValueError(
                f"Unexpected email model class: {prediction}"
            )

        class_positions = {
            int(label): index
            for index, label in enumerate(model.classes_)
        }

        if prediction not in class_positions:
            raise ValueError(
                "Predicted class was not found in model classes."
            )

        predicted_probability = float(
            probabilities[class_positions[prediction]]
        )

        classification = CLASSIFICATION_MAPPING[prediction]


        body_result = analyze_email_content(body)


        subject_result = analyze_email_subject(subject)


        sender_result = analyze_email_sender(sender)


        indicators = (
            body_result["indicators"]
            + subject_result["indicators"]
            + sender_result["indicators"]
        )

        evidence = (
            body_result["evidence"]
            + subject_result["evidence"]
            + sender_result["evidence"]
        )

        indicators = list(dict.fromkeys(indicators))
        evidence = list(dict.fromkeys(evidence))

        # Add ML prediction information to evidence.

        evidence.append(
            f"Machine learning prediction: {LABEL_NAMES[prediction]}"
        )

        evidence.append(
            f"Predicted class probability: "
            f"{predicted_probability * 100:.2f}%"
        )


        explanation = (
            f"The machine learning model classified the email as "
            f"{LABEL_NAMES[prediction]} with "
            f"{predicted_probability * 100:.2f}% probability. "
            f"Email content analysis detected "
            f"{len(indicators)} suspicious indicators."
        )


        return AgentResult(
            agent="Email Analysis Agent",
            status="completed",
            classification=classification,
            risk_score=None,
            indicators=indicators,
            explanation=explanation,
            evidence=evidence
        )

    except Exception as error:

        return AgentResult(
            agent="Email Analysis Agent",
            status="error",
            classification="unknown",
            risk_score=None,
            indicators=[],
            explanation=f"Email analysis failed: {str(error)}",
            evidence=[]
        )
