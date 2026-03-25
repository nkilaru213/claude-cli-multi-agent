"""Local in-memory retrieval used by the triage assistant."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from models import RunbookEntry

KNOWLEDGE_BASE: List[RunbookEntry] = [
    RunbookEntry(
        category="data pipeline incident",
        severity_owner="data-platform-oncall",
        likely_issue="warehouse connectivity, credential rotation, or timeout threshold misconfiguration",
        checks=[
            "Confirm warehouse endpoint health and upstream service status.",
            "Verify credentials, tokens, and recent secret rotations.",
            "Inspect retry, backoff, and timeout thresholds for the failing job.",
            "Check whether the latest deployment changed scheduler or connector settings.",
        ],
        signals=["warehouse", "pipeline", "etl", "billing job", "scheduler", "connector", "timeout"],
    ),
    RunbookEntry(
        category="authentication incident",
        severity_owner="identity-oncall",
        likely_issue="expired credentials, identity provider degradation, or broken role mapping",
        checks=[
            "Check identity provider health and authentication latency.",
            "Verify service account secrets, token expiry, and certificate rotation.",
            "Review recent role, policy, or group membership changes.",
            "Confirm whether MFA or federation dependencies changed.",
        ],
        signals=["login", "token", "credential", "auth", "oauth", "sso", "mfa", "certificate"],
    ),
    RunbookEntry(
        category="application incident",
        severity_owner="application-oncall",
        likely_issue="recent deploy regression, dependency failure, or latent infrastructure saturation",
        checks=[
            "Inspect recent deploys, feature flags, and rollback candidates.",
            "Review application logs, error rates, and request latency trends.",
            "Check downstream dependency health and compare against the last healthy baseline.",
            "Confirm whether incidents are isolated to one region, tenant, or user segment.",
        ],
        signals=["deploy", "api", "latency", "exception", "error", "dashboard", "service", "region"],
    ),
]

DEFAULT_ENTRY = RunbookEntry(
    category="application incident",
    severity_owner="application-oncall",
    likely_issue="insufficient signal in the report to isolate a single cause",
    checks=[
        "Collect timestamps, impacted services, and the exact user-visible symptom.",
        "Gather logs, metrics, and recent change history before escalating.",
        "Identify blast radius: user segment, region, and affected workflows.",
    ],
    signals=[],
)


def _score_entry(tokens: Iterable[str], entry: RunbookEntry) -> Tuple[int, List[str]]:
    matched = [signal for signal in entry.signals if signal in tokens]
    return len(matched), matched


def retrieve_best_entry(text: str) -> Tuple[RunbookEntry, List[str], float]:
    """Return the best matching runbook entry with matched signals and confidence."""
    normalized = text.lower()
    best_entry = DEFAULT_ENTRY
    best_matches: List[str] = []
    best_score = 0

    for entry in KNOWLEDGE_BASE:
        score, matches = _score_entry(normalized, entry)
        if score > best_score:
            best_entry = entry
            best_matches = matches
            best_score = score

    confidence = min(0.35 + (0.15 * best_score), 0.95) if best_score else 0.3
    return best_entry, best_matches, confidence
