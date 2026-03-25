"""Core triage logic for the local AI triage assistant."""

from __future__ import annotations

from models import TriageResult
from retriever import retrieve_best_entry

HIGH_SEVERITY_SIGNALS = [
    "sev1",
    "critical",
    "all users",
    "outage",
    "payment failure",
    "data loss",
    "security",
]
MEDIUM_SEVERITY_SIGNALS = [
    "failed",
    "timeout",
    "error",
    "degraded",
    "intermittent",
    "stuck",
]


def estimate_severity(text: str) -> str:
    """Estimate severity from language in the incident report."""
    lower_text = text.lower()

    if any(signal in lower_text for signal in HIGH_SEVERITY_SIGNALS):
        return "high"
    if any(signal in lower_text for signal in MEDIUM_SEVERITY_SIGNALS):
        return "medium"
    return "low"


def recommend_next_step(severity: str, owner: str, matched_signals: list[str]) -> str:
    """Return an action-oriented next step."""
    if severity == "high":
        return (
            f"Immediately page {owner}, open an incident channel, and confirm blast radius before making irreversible changes."
        )
    if matched_signals:
        return (
            f"Follow the checklist below and escalate to {owner} if the symptom persists after standard checks."
        )
    return (
        "Gather more context from the reporter, attach logs and timestamps, and route to the most likely on-call owner."
    )


def generate_triage_response(text: str) -> dict[str, object]:
    """Generate a structured triage response for a single incident string."""
    entry, matched_signals, confidence = retrieve_best_entry(text)
    severity = estimate_severity(text)

    result = TriageResult(
        category=entry.category,
        severity=severity,
        confidence=round(confidence, 2),
        likely_issue=entry.likely_issue,
        suggested_checks=entry.checks,
        recommended_next_step=recommend_next_step(severity, entry.severity_owner, matched_signals),
        escalation_owner=entry.severity_owner,
        matched_signals=matched_signals,
    )
    return result.to_dict()
