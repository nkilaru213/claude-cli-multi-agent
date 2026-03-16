#!/usr/bin/env bash
set -euo pipefail

claude --agent product-agent \
  "Read docs/specs/ai-triage-use-case.md and write docs/handoffs/product-brief.md"

claude --agent architect-agent \
  "Read docs/specs/ai-triage-use-case.md and docs/handoffs/product-brief.md, then write docs/handoffs/architecture.md"

claude --agent developer-agent \
  "Read docs/handoffs/product-brief.md and docs/handoffs/architecture.md, then write docs/handoffs/implementation-plan.md and implement src/"
