# Cursor Workflow

Cursor-specific workflow artifacts for the Support Ticket Management assessment.

## Contents

| Path | Purpose |
|------|---------|
| [rules-overview.md](./rules-overview.md) | Index of `.cursor/rules/` and what each prevents |
| [context-strategy.md](./context-strategy.md) | How to layer rules, docs, and skills in sessions |
| [prompt-templates.md](./prompt-templates.md) | Reusable prompt starters per phase |
| [skills/](./skills/) | Project skills (sync docs, tests, debug, review, capture) |
| [exports/](./exports/) | Selected Cursor chat exports (10–15 sessions) |

## Rules

Seven rules in `.cursor/rules/` — see [rules-overview.md](./rules-overview.md).

## Skills

| Skill | Use when |
|-------|----------|
| `sync-api-docs` | Router files change |
| `write-state-machine-tests` | Status transitions implemented/tested |
| `debug-backend-issue` | API or DB bugs |
| `review-ticket-feature` | Feature complete or pre-PR |
| `capture-prompt-session` | Log session to `ai-prompts/` |
| `docker-up-local` | Start full stack with Docker for manual verification |
