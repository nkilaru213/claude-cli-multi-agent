# Use Case: Internal AI Incident Triage Assistant

## Background
An operations team receives incident reports from multiple internal users. Many reports are duplicates, incomplete, or missing the first troubleshooting steps.

## Goal
Create an internal AI assistant that accepts a short incident description and returns:
- incident category
- severity hint
- likely troubleshooting checklist
- likely runbook snippets
- a safe recommendation for next action

## Constraints
- MVP must run locally
- No external API calls
- Retrieval can use a local in-memory knowledge base
- The response must say it is a helper, not a final authority

## Example input
"The nightly billing job failed again and the dashboard shows timeout errors when connecting to the warehouse."

## Example desired output
- Category: data pipeline incident
- Severity: medium
- Likely issue: warehouse connectivity timeout
- Suggested checks:
  1. confirm warehouse endpoint health
  2. check recent credential rotation
  3. inspect retry threshold configuration
- Recommended next step: escalate to data platform on-call if issue persists after standard checks
