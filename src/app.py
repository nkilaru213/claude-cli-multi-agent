"""Runnable local entry point for the AI triage assistant."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from triage import generate_triage_response


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local AI incident triage assistant")
    parser.add_argument("--incident", help="Incident description to triage")
    parser.add_argument("--json", action="store_true", help="Print compact JSON instead of pretty JSON")
    return parser


def resolve_incident(provided_incident: Optional[str]) -> str:
    if provided_incident:
        return provided_incident.strip()

    print("AI Incident Triage Assistant")
    print("Type an incident description and press Enter.\n")
    return input("Incident: ").strip()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    incident = resolve_incident(args.incident)

    if not incident:
        print("Please provide an incident description.", file=sys.stderr)
        return 1

    result = generate_triage_response(incident)
    if args.json:
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
