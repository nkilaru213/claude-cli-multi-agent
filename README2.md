# Claude CLI Multi-Agent Sample

This sample repo shows how to run a **product**, **architect**, and **developer** agent in Claude Code (CLI) using **project-level subagents** under `.claude/agents/`.

It is designed for a practical use case:

> Build a well-managed internal AI solution for incident triage and knowledge retrieval.

The flow is:

1. **product-agent** turns the business ask into a scoped product brief.
2. **architect-agent** turns the brief into an implementation architecture.
3. **developer-agent** turns the architecture into working code/tasks.
4. A **coordinator agent** orchestrates the three and writes handoff artifacts into `docs/handoffs/`.

## Why this pattern

Claude Code supports **custom subagents** in `.claude/agents/`. Project-level subagents are shared with the team through git, and Claude can delegate based on each agent's `description`. Claude Code also supports restricting which agents a coordinator can spawn using `Agent(agent-name)` in the subagent tools field. Official docs describe `.claude/agents/` as the project location for subagents, YAML frontmatter as the definition format, and `Agent(...)` as the way to allow a main-thread agent to delegate to specific subagents. citeturn305665view0turn353157view1turn353157view3

## Repo structure

```text
claude-cli-multi-agent-sample/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   ├── agents/
│   │   ├── coordinator-agent.md
│   │   ├── product-agent.md
│   │   ├── architect-agent.md
│   │   └── developer-agent.md
│   └── skills/
│       └── solution-delivery-workflow/
│           └── SKILL.md
├── docs/
│   ├── specs/
│   │   └── ai-triage-use-case.md
│   └── handoffs/
│       ├── product-brief.md
│       ├── architecture.md
│       └── implementation-plan.md
├── scripts/
│   ├── run-coordinator.sh
│   ├── run-sequential.sh
│   └── notify-subagent-stop.sh
└── src/
    ├── app.py
    ├── retriever.py
    └── triage.py
```

## Requirements

- Claude Code installed
- Logged in with `claude auth login`
- Run from the repo root

Claude Code CLI supports starting interactive sessions, continuing sessions, checking auth state, listing agents, and choosing an agent for the current session with `--agent`. citeturn319094search3turn305665view0

## Quick start

### 1. Enter the repo

```bash
cd claude-cli-multi-agent-sample
```

### 2. Check authentication

```bash
claude auth status --text
```

### 3. See project agents

```bash
claude agents
```

### 4. Run the coordinator in an interactive session

```bash
claude --agent coordinator-agent
```

Then paste this prompt:

```text
Deliver the AI triage assistant described in docs/specs/ai-triage-use-case.md.
Use the product-agent first, then the architect-agent, then the developer-agent.
Make each agent write its handoff into docs/handoffs/.
At the end, summarize risks, open decisions, and next steps.
```

## Alternative: one-shot non-interactive style

You can also use the helper script:

```bash
bash scripts/run-coordinator.sh
```

## How the agents communicate

Subagents do not directly spawn each other. The **coordinator** is the parent agent and delegates work to the others. The communication model here is:

- shared repo context
- explicit task briefs in prompts
- written handoff files in `docs/handoffs/`
- optional project hooks for visibility

This matches Claude Code’s model: subagents run in their own context, and when you need coordination across specialized agents, the main agent delegates and synthesizes results. Claude’s docs also note that subagents themselves cannot spawn subagents. citeturn305665view0turn353157view1

## Notes for your company structure

Your screenshot shows an `agents/` folder at repo root. For Claude Code itself, the documented project-level subagent location is **`.claude/agents/`**. If your company wants a visible root-level `agents/` folder too, keep it as documentation/templates, but place the real Claude Code subagent definitions under `.claude/agents/` so Claude can load them automatically. citeturn305665view0turn305665view1
