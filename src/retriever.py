"""Simple local retrieval for the demo AI triage assistant."""

from typing import List

RUNBOOKS = {
    "data pipeline incident": [
        "Check warehouse endpoint health and connectivity.",
        "Confirm credentials or tokens were not rotated or expired.",
        "Inspect retry and timeout configuration for the job.",
    ],
    "authentication incident": [
        "Check identity provider status.",
        "Verify service account secrets and expiry timestamps.",
        "Review recent role or policy changes.",
    ],
    "application incident": [
        "Inspect recent deploy changes.",
        "Check dependency health and error logs.",
        "Compare current metrics to the last healthy baseline.",
    ],
}


def retrieve_checks(category: str) -> List[str]:
    """Return a small checklist for the given category."""
    return RUNBOOKS.get(category, ["Collect more logs and identify the impacted component."])
