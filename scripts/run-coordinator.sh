#!/usr/bin/env bash
set -euo pipefail

PROMPT='Deliver the AI triage assistant described in docs/specs/ai-triage-use-case.md.
Use the product-agent first, then the architect-agent, then the developer-agent.
Make each agent write its handoff into docs/handoffs/.
At the end, summarize risks, open decisions, and next steps.'

claude --agent coordinator-agent "$PROMPT"
