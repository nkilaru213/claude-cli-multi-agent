#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 scripts/run_pipeline.py --mode coordinator --spec "${1:-docs/specs/ai-triage-use-case.md}"
