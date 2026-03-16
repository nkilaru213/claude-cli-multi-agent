# Project Memory: AI Triage Assistant

## Objective
Build a well-managed internal AI triage assistant for operations teams.

The system should:
- accept incident text from users
- classify the incident type
- retrieve likely runbook guidance
- return a safe triage summary
- make it easy to add product, architecture, and implementation artifacts

## Working norms
- Write plans before major code changes.
- Keep artifacts in `docs/handoffs/`.
- Prefer small, readable files.
- Do not invent infrastructure that is not documented in this repo.
- Preserve explainability and traceability for AI outputs.
- Flag open risks clearly.

## Standard delivery flow
1. Read the use case in `docs/specs/ai-triage-use-case.md`
2. Create/update `docs/handoffs/product-brief.md`
3. Create/update `docs/handoffs/architecture.md`
4. Create/update `docs/handoffs/implementation-plan.md`
5. Implement only the approved scope in `src/`

## Commands
```bash
python3 src/app.py
python3 -m py_compile src/*.py
```

## Tech assumptions
- Python sample app for easy portability
- Retrieval is mocked with local data
- No external API dependency
- This repo demonstrates Claude Code CLI workflow, not production infra
