
from pathlib import Path
import ipaddress
from urllib.parse import urlparse

import pandas as pd
import joblib

from schemas.agent_result import AgentResult


# ==========================================
# STEP 1: Locate and load the trained model
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_DIR / "models" / "URL_Analysis_XGBoost.pkl"
)

loaded_model = joblib.load(MODEL_PATH)


# ==========================================
# STEP 2: Extract URL features
# ==========================================

def extract_url_features(url):

    url = str(url).strip()

    parsed = urlparse(
        url if "://" in url else "//" + url
    )

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    features = {}

    features["url_length"] = len(url)
    features["hostname_length"] = len(hostname)
    features["path_length"] = len(path)
    features["query_length"] = len(query)

    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_underscores"] = url.count("_")
    features["num_slashes"] = url.count("/")
    features["num_questionmarks"] = url.count("?")
    features["num_equal"] = url.count("=")
    features["num_at"] = url.count("@")
    features["num_ampersands"] = url.count("&")
    features["num_percent"] = url.count("%")

    features["num_digits"] = sum(
        c.isdigit() for c in url
    )

    features["num_letters"] = sum(
        c.isalpha() for c in url
    )

    features["digit_ratio"] = (
        features["num_digits"] / max(len(url), 1)
    )

    features["https"] = int(
        url.lower().startswith("https://")
    )

    features["http"] = int(
        url.lower().startswith("http://")
    )

    features["has_ip"] = 0

    try:
        ipaddress.ip_address(hostname)
        features["has_ip"] = 1
    except ValueError:
        pass

    features["num_subdomains"] = max(
        hostname.count(".") - 1, 0
    )

    suspicious_words = [
        "login", "verify", "account", "secure",
        "update", "banking", "password", "confirm",
        "free", "bonus", "wallet", "signin",
        "paypal", "malware", "download"
    ]

    features["suspicious_word_count"] = sum(
        word in url.lower()
        for word in suspicious_words
    )

    features["has_www"] = int(
        "www." in hostname.lower()
    )

    features["has_shortening_service"] = int(
        any(domain in hostname.lower() for domain in [
            "bit.ly", "tinyurl.com", "t.co",
            "goo.gl", "ow.ly", "is.gd"
        ])
    )

    features["special_char_count"] = sum(
        not c.isalnum() for c in url
    )

    return features


# ==========================================
# STEP 3: Generate the URL Analysis Result
# ==========================================

def analyze_url(url):

    url = str(url).strip()

    # Handle empty URL
    if not url:

        return AgentResult(
            agent="URL Analysis Agent",
            status="unavailable",
            classification="unknown",
            risk_score=None,
            indicators=[],
            explanation="Empty URL. Analysis could not be completed.",
            evidence=[]
        )

    try:

        # Extract URL features
        features = pd.DataFrame([
            extract_url_features(url)
        ])

        # Match the model's original training feature order
        features = features[
            loaded_model.feature_names_in_
        ]

        # Get prediction probabilities
        probabilities = loaded_model.predict_proba(
            features
        )[0]

        # Identify probability positions using class labels
        class_positions = {
            int(label): index
            for index, label in enumerate(
                loaded_model.classes_
            )
        }

        if 0 not in class_positions or 1 not in class_positions:
            raise ValueError(
                "Unexpected model class labels."
            )

        legitimate_probability = float(
            probabilities[class_positions[0]]
        )

        malicious_probability = float(
            probabilities[class_positions[1]]
        )

        # Classification
        if malicious_probability >= 0.70:
            classification = "malicious"

        elif malicious_probability <= 0.30:
            classification = "safe"

        else:
            classification = "suspicious"

        # ==================================
        # STEP 4: Identify URL indicators
        # ==================================

        feature_values = features.iloc[0]

        indicators = []

        if feature_values["has_ip"] == 1:
            indicators.append(
                "URL uses an IP address."
            )

        if feature_values["suspicious_word_count"] > 0:
            indicators.append(
                "Potentially suspicious keywords detected."
            )

        if feature_values["has_shortening_service"] == 1:
            indicators.append(
                "URL shortening service detected."
            )

        if feature_values["num_subdomains"] >= 3:
            indicators.append(
                "Multiple subdomains detected."
            )

        if feature_values["num_at"] > 0:
            indicators.append(
                "@ symbol detected in URL."
            )

        if feature_values["num_digits"] > 10:
            indicators.append(
                "High number of digits detected."
            )

        if feature_values["num_hyphens"] >= 3:
            indicators.append(
                "Multiple hyphens detected."
            )

        if not indicators:
            indicators.append(
                "No predefined URL indicators detected."
            )

        # ==================================
        # STEP 5: Generate explanation
        # ==================================

        explanation = (
            f"XGBoost classified this URL as {classification}. "
            f"The predicted malicious probability is "
            f"{malicious_probability * 100:.2f}%. "
            "This prediction is based on learned URL characteristics."
        )

        # ==================================
        # STEP 6: Collect evidence
        # ==================================

        evidence = [
            f"URL: {url}",
            f"Malicious probability: {malicious_probability * 100:.2f}%",
            f"Legitimate probability: {legitimate_probability * 100:.2f}%",
            "Model: XGBoost",
            "Feature extraction: Numerical URL lexical features"
        ]

        # ==================================
        # STEP 7: Return shared AgentResult
        # ==================================

        return AgentResult(
            agent="URL Analysis Agent",
            status="completed",
            classification=classification,
            risk_score=None,
            indicators=indicators,
            explanation=explanation,
            evidence=evidence
        )

    except Exception as error:

        return AgentResult(
            agent="URL Analysis Agent",
            status="error",
            classification="unknown",
            risk_score=None,
            indicators=[],
            explanation=f"URL analysis failed: {str(error)}",
            evidence=[]
        )
