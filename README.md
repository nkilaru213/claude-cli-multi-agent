# Claude CLI Multi-Agent System (Production-Style POC)

This repository is a production-style proof of concept for a multi-agent delivery workflow built around Claude CLI.

It is designed for a realistic internal AI solution flow where specialized agents collaborate through explicit handoff documents, generated code, review notes, and timestamped run artifacts.

## What this repo demonstrates

- a **Product agent** that turns a spec into a testable product brief
- an **Architect agent** that produces implementation-ready system design
- a **Developer agent** that updates code and implementation notes
- a **Reviewer agent** that checks scope alignment, maintainability, and risks
- a **Coordinator mode** for end-to-end orchestration through Claude CLI
- a **Feedback-loop mode** for reviewer-driven rework
- a local **AI triage assistant** sample app that acts as the implementation target

## Why this is stronger than a basic demo

This repo is structured so your POC looks more like an engineering system than a one-off prompt chain:

- explicit artifact handoffs in `docs/handoffs/`
- run snapshots in `artifacts/runs/<timestamp>/`
- reproducible scripts for sequential, coordinator, and feedback-loop execution
- local validation with Python tests
- a sample app with structured models, retrieval logic, CLI input handling, and safer triage output

## Repository structure

```text
.
├── .claude/
│   ├── agents/
│   └── settings.json
├── artifacts/
│   └── runs/
├── docs/
│   ├── handoffs/
│   └── specs/
├── scripts/
│   ├── run_pipeline.py
│   ├── run-sequential.sh
│   ├── run-feedback-loop.sh
│   └── run-coordinator.sh
├── src/
│   ├── app.py
│   ├── models.py
│   ├── retriever.py
│   └── triage.py
└── tests/
    └── test_triage.py
```

## Prerequisites

- Python 3.10+
- Claude CLI installed and authenticated
- a shell environment where `claude` is available on `PATH`

## Claude CLI setup

Install and authenticate Claude CLI using your preferred internal or official workflow. This repo assumes the following is true before you run it:

```bash
claude --help
```

If that command fails, the orchestration wrapper will stop early and tell you Claude CLI is missing.

## Core run modes

### 1. Sequential mode

Runs the four specialist agents in a fixed order.

```bash
bash scripts/run-sequential.sh
```

### 2. Coordinator mode

Lets the coordinator own the workflow and handoffs.

```bash
bash scripts/run-coordinator.sh
```

### 3. Feedback-loop mode

Runs the main pipeline, reads reviewer notes, and optionally triggers one or more developer rework passes.

```bash
bash scripts/run-feedback-loop.sh
```

## Using a different spec

All run scripts accept a spec path as the first argument.

```bash
bash scripts/run-sequential.sh docs/specs/ai-triage-use-case.md
```

## Run artifacts

Every pipeline execution creates a timestamped folder under `artifacts/runs/`.

Each run contains:

- `run-metadata.json`
- `run-summary.json`
- per-stage CLI logs
- a snapshot of generated handoff markdown files
- `FAILED.txt` if orchestration stops because a Claude stage fails

This makes your POC much easier to demo, debug, and audit.

## Local app usage

The sample implementation target is a local AI incident triage assistant.

### Interactive mode

```bash
python3 src/app.py
```

### One-shot mode

```bash
python3 src/app.py --incident "The nightly billing job failed again and warehouse connections are timing out."
```

### Compact JSON mode

```bash
python3 src/app.py --incident "Critical outage affecting all users" --json
```

## Validation

### Syntax check

```bash
python3 -m py_compile src/*.py
```

### Unit tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Multi-agent contract

The system is intentionally handoff-driven.

1. Product writes `docs/handoffs/product-brief.md`
2. Architecture consumes that brief and writes `docs/handoffs/architecture.md`
3. Development consumes both handoffs, updates `src/`, and writes `docs/handoffs/implementation-plan.md`
4. Review checks implementation quality and writes `docs/handoffs/review-notes.md`
5. Orchestration snapshots those artifacts into a timestamped run directory

This makes the flow easy to inspect and extend.

## Recommended demo flow for your POC

For a polished demo:

1. show the input spec in `docs/specs/`
2. run `bash scripts/run-feedback-loop.sh`
3. open the latest folder under `artifacts/runs/`
4. show the handoff evolution and logs
5. run `python3 src/app.py --incident "..."` to show the final implementation working

That sequence makes the project feel much closer to a real internal engineering workflow.

## Production-minded improvements already included

- stricter agent role boundaries
- explicit handoff files
- timestamped run artifacts
- stage-level CLI logging
- local test coverage for triage behavior
- structured response fields such as confidence, escalation owner, and disclaimer
- safer next-step guidance instead of overconfident recommendations

## Strong next upgrades

If you want to push this beyond POC and into a stronger platform story, the best next additions are:

- a small web UI for viewing specs, handoffs, and run history
- JSON schema validation for handoff documents
- a `security-agent` and `qa-agent`
- a real knowledge base persisted outside Python source
- containerization with Docker
- CI checks that run tests and linting automatically

## Notes

- This repo uses Claude CLI, not the Claude API.
- CLI syntax can vary slightly by installation or enterprise wrapper. If your environment uses a different command shape, update `scripts/run_pipeline.py` in one place instead of rewriting every run script.
- The sample app is still intentionally lightweight; the value of the repo is the multi-agent workflow and artifact traceability.
