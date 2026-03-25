#!/usr/bin/env python3
"""Production-style orchestration wrapper for the Claude CLI POC."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROOT_DIR = Path(__file__).resolve().parent.parent
HANDOFF_DIR = ROOT_DIR / "docs" / "handoffs"
RUNS_DIR = ROOT_DIR / "artifacts" / "runs"
DEFAULT_SPEC = ROOT_DIR / "docs" / "specs" / "ai-triage-use-case.md"


@dataclass(frozen=True)
class Stage:
    name: str
    agent: str
    prompt: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Claude CLI multi-agent pipeline")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC), help="Path to the input spec")
    parser.add_argument(
        "--mode",
        choices=["sequential", "feedback-loop", "coordinator"],
        default="sequential",
        help="Pipeline mode to execute",
    )
    parser.add_argument("--max-review-iterations", type=int, default=1, help="Max developer rework loops")
    return parser


def ensure_dependencies() -> str:
    claude_path = shutil.which("claude")
    if not claude_path:
        raise SystemExit(
            "Claude CLI was not found on PATH. Install it, authenticate, then rerun this command."
        )
    return claude_path


def now_stamp() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def create_run_dir() -> Path:
    run_dir = RUNS_DIR / now_stamp()
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_run_metadata(run_dir: Path, mode: str, spec_path: Path) -> None:
    metadata = {
        "mode": mode,
        "spec_path": str(spec_path),
        "started_at_utc": datetime.utcnow().isoformat() + "Z",
    }
    (run_dir / "run-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def invoke_claude(claude_path: str, agent: str, prompt: str, log_path: Path) -> str:
    command = [claude_path, "--agent", agent, prompt]
    result = subprocess.run(command, cwd=ROOT_DIR, text=True, capture_output=True)
    combined_output = f"$ {' '.join(command)}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    log_path.write_text(combined_output, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Claude stage '{agent}' failed. See {log_path}")
    return result.stdout.strip()


def snapshot_handoffs(run_dir: Path) -> None:
    snapshot_dir = run_dir / "handoffs"
    snapshot_dir.mkdir(exist_ok=True)
    for path in HANDOFF_DIR.glob("*.md"):
        shutil.copy2(path, snapshot_dir / path.name)


def run_stages(claude_path: str, run_dir: Path, stages: Iterable[Stage]) -> list[dict[str, str]]:
    summary: list[dict[str, str]] = []
    for stage in stages:
        print(f"[{stage.name}] running {stage.agent}...")
        log_path = run_dir / f"{stage.name}.log"
        output = invoke_claude(claude_path, stage.agent, stage.prompt, log_path)
        summary.append({"stage": stage.name, "agent": stage.agent, "log": str(log_path), "output": output})
        snapshot_handoffs(run_dir)
    return summary


def sequential_stages(spec_path: Path) -> list[Stage]:
    return [
        Stage(
            name="01-product",
            agent="product-agent",
            prompt=(
                f"Read CLAUDE.md and {spec_path}, then write docs/handoffs/product-brief.md "
                "using the required structure in your agent instructions."
            ),
        ),
        Stage(
            name="02-architecture",
            agent="architect-agent",
            prompt=(
                f"Read CLAUDE.md, {spec_path}, and docs/handoffs/product-brief.md, then write "
                "docs/handoffs/architecture.md using the required structure in your agent instructions."
            ),
        ),
        Stage(
            name="03-development",
            agent="developer-agent",
            prompt=(
                "Read CLAUDE.md, docs/handoffs/product-brief.md, and docs/handoffs/architecture.md, then "
                "write docs/handoffs/implementation-plan.md, update src/, and run lightweight validation if possible."
            ),
        ),
        Stage(
            name="04-review",
            agent="reviewer-agent",
            prompt=(
                "Review docs/handoffs/product-brief.md, docs/handoffs/architecture.md, "
                "docs/handoffs/implementation-plan.md, and src/. Write docs/handoffs/review-notes.md "
                "with findings and a verdict."
            ),
        ),
    ]


def run_feedback_loop(claude_path: str, run_dir: Path, spec_path: Path, max_review_iterations: int) -> list[dict[str, str]]:
    summary = run_stages(claude_path, run_dir, sequential_stages(spec_path))

    for iteration in range(1, max_review_iterations + 1):
        review_text = (HANDOFF_DIR / "review-notes.md").read_text(encoding="utf-8").lower()
        if "needs improvement" not in review_text:
            break
        print(f"[feedback-loop] iteration {iteration}: reviewer requested changes")
        rework_stages = [
            Stage(
                name=f"05-dev-rework-{iteration}",
                agent="developer-agent",
                prompt=(
                    "Read docs/handoffs/product-brief.md, docs/handoffs/architecture.md, "
                    "docs/handoffs/implementation-plan.md, and docs/handoffs/review-notes.md. "
                    "Address the highest-priority review issues that fit the approved MVP, update src/, "
                    "and refresh docs/handoffs/implementation-plan.md."
                ),
            ),
            Stage(
                name=f"06-review-recheck-{iteration}",
                agent="reviewer-agent",
                prompt=(
                    "Re-review the latest implementation using docs/handoffs/product-brief.md, docs/handoffs/architecture.md, "
                    "docs/handoffs/implementation-plan.md, docs/handoffs/review-notes.md, and src/. "
                    "Update docs/handoffs/review-notes.md with the latest findings and verdict."
                ),
            ),
        ]
        summary.extend(run_stages(claude_path, run_dir, rework_stages))
    return summary


def run_coordinator(claude_path: str, run_dir: Path, spec_path: Path) -> list[dict[str, str]]:
    stage = Stage(
        name="01-coordinator",
        agent="coordinator-agent",
        prompt=(
            f"Deliver the solution described in {spec_path}. Read CLAUDE.md first. Use the product-agent first, "
            "then the architect-agent, then the developer-agent, then the reviewer-agent. Make each agent write its "
            "handoff into docs/handoffs/. Do not skip reviews between stages. At the end, summarize what was "
            "delivered, review findings, open risks, deferred items, and next steps."
        ),
    )
    return run_stages(claude_path, run_dir, [stage])


def write_summary(run_dir: Path, summary: list[dict[str, str]]) -> None:
    minimal = [{k: v for k, v in row.items() if k != "output"} for row in summary]
    (run_dir / "run-summary.json").write_text(json.dumps(minimal, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    if not spec_path.exists():
        raise SystemExit(f"Spec not found: {spec_path}")

    claude_path = ensure_dependencies()
    run_dir = create_run_dir()
    write_run_metadata(run_dir, args.mode, spec_path)

    try:
        if args.mode == "sequential":
            summary = run_stages(claude_path, run_dir, sequential_stages(spec_path))
        elif args.mode == "feedback-loop":
            summary = run_feedback_loop(claude_path, run_dir, spec_path, args.max_review_iterations)
        else:
            summary = run_coordinator(claude_path, run_dir, spec_path)
    except Exception as exc:  # pragma: no cover - defensive shell for operators
        (run_dir / "FAILED.txt").write_text(str(exc) + "\n", encoding="utf-8")
        raise
    finally:
        snapshot_handoffs(run_dir)

    write_summary(run_dir, summary)
    print(f"Run complete. Artifacts saved under {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
