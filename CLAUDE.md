# Project Memory: AI Triage Assistant

## Objective
Build a well-managed internal AI triage assistant for operations teams.

The system should:
- accept incident text from users
- classify the incident type
- retrieve likely runbook guidance
- return a safe triage summary
- make it easy to generate product, architecture, implementation, and review artifacts through Claude CLI

## Delivery norms
- Read the relevant spec before making changes.
- Keep all cross-agent communication in `docs/handoffs/`.
- Preserve traceability from product brief to architecture to implementation.
- Prefer small, readable files and minimal local dependencies.
- When uncertain, document assumptions explicitly instead of inventing hidden scope.
- Optimize for a strong POC that can be demoed and extended, not for premature infrastructure complexity.

## Operational guardrails
- No external API calls for the sample app.
- Keep the implementation locally runnable with Python.
- Response language must clearly state that the assistant is advisory, not a final authority.
- Retrieval can remain local and in-memory for the MVP, but interfaces should leave room for productionization later.

## Repository conventions
- Source code lives in `src/`.
- Specs live in `docs/specs/`.
- Agent handoffs live in `docs/handoffs/`.
- Timestamped orchestration artifacts live in `artifacts/runs/`.
- Local validation should use `python3 -m py_compile src/*.py` and `python3 -m unittest discover -s tests -p 'test_*.py'` where possible.

## What good looks like
A strong output from this repo should include:
- a clear product brief with testable acceptance criteria
- a practical architecture with component boundaries and trade-offs
- working local code with simple validation
- review notes that identify real gaps and follow-up work
- a run folder that lets an operator audit what happened
