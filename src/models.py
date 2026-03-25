"""Domain models for the local AI triage assistant."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class RunbookEntry:
    """Knowledge base item used for retrieval."""

    category: str
    severity_owner: str
    likely_issue: str
    checks: List[str]
    signals: List[str]


@dataclass
class TriageResult:
    """Structured response returned by the triage pipeline."""

    category: str
    severity: str
    confidence: float
    likely_issue: str
    suggested_checks: List[str]
    recommended_next_step: str
    escalation_owner: str
    matched_signals: List[str] = field(default_factory=list)
    disclaimer: str = (
        "This assistant is a helper for initial triage and does not replace the on-call owner's judgment."
    )

    def to_dict(self) -> Dict[str, object]:
        """Convert to a plain dictionary for JSON serialization."""
        return asdict(self)
