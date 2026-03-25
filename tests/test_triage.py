"""Basic regression tests for the triage assistant."""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from triage import estimate_severity, generate_triage_response  # noqa: E402


class TriageTests(unittest.TestCase):
    def test_pipeline_incident_is_classified(self) -> None:
        result = generate_triage_response(
            "The nightly billing job failed and warehouse connections are timing out."
        )
        self.assertEqual(result["category"], "data pipeline incident")
        self.assertEqual(result["severity"], "medium")
        self.assertGreaterEqual(result["confidence"], 0.5)

    def test_auth_incident_routes_to_identity_owner(self) -> None:
        result = generate_triage_response("Login failures started after token rotation and SSO errors.")
        self.assertEqual(result["category"], "authentication incident")
        self.assertEqual(result["escalation_owner"], "identity-oncall")

    def test_high_severity_signal_is_detected(self) -> None:
        self.assertEqual(estimate_severity("Critical outage affecting all users"), "high")


if __name__ == "__main__":
    unittest.main()
