"""Very small rule-based triage module for the demo."""

from typing import Dict
from retriever import retrieve_checks


def classify_incident(text: str) -> str:
    lower_text = text.lower()

    if any(word in lower_text for word in ["warehouse", "pipeline", "etl", "billing job"]):
        return "data pipeline incident"
    if any(word in lower_text for word in ["login", "token", "credential", "auth"]):
        return "authentication incident"
    return "application incident"


def estimate_severity(text: str) -> str:
    lower_text = text.lower()

    if any(word in lower_text for word in ["outage", "sev1", "critical", "all users"]):
        return "high"
    if any(word in lower_text for word in ["failed", "timeout", "error"]):
        return "medium"
    return "low"


def generate_triage_response(text: str) -> Dict[str, object]:
    category = classify_incident(text)
    severity = estimate_severity(text)
    checks = retrieve_checks(category)

    return {
        "category": category,
        "severity": severity,
        "likely_issue": checks[0],
        "suggested_checks": checks,
        "recommended_next_step": (
            "Use this as a helper, then confirm with the on-call owner before taking irreversible action."
        ),
    }
