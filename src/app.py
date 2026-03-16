"""Runnable local entry point for the sample AI triage assistant."""

import json
from triage import generate_triage_response


def main() -> None:
    print("AI Incident Triage Assistant")
    print("Type an incident description and press Enter.\n")
    user_input = input("Incident: ").strip()

    if not user_input:
        print("Please provide an incident description.")
        return

    result = generate_triage_response(user_input)
    print("\nResponse:\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
