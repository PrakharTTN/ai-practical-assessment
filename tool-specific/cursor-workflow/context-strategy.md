# Context Strategy

How to set context in Cursor for the Support Ticket Management assessment so AI output stays aligned with requirements.

## Layered Context Model

```
┌─────────────────────────────────────────────┐
│  Always-on rules                            │
│  project-context · security-and-env         │
├─────────────────────────────────────────────┤
│  File-triggered rules (auto via globs)      │
│  state-machine · api-contract-sync ·        │
│  api-error-shape · testing-discipline ·     │
│  artifact-discipline                        │
├─────────────────────────────────────────────┤
│  Reference docs (attach or @-mention)       │
│  api-contract.md · data-model.md ·          │
│  acceptance-criteria.md · ui-flow.md          │
├─────────────────────────────────────────────┤
│  Skills (invoke explicitly)                 │
│  sync-api-docs · write-state-machine-tests  │
│  debug-backend-issue · review-ticket-feature│
│  capture-prompt-session                     │
└─────────────────────────────────────────────┘
```

## Session Start Checklist

1. Open relevant files so glob rules activate (router file → `api-contract-sync`; test file → `testing-discipline`)
2. `@acceptance-criteria.md` when scoping a feature
3. `@data-model.md` when touching models or migrations
4. `@api-contract.md` when implementing or reviewing endpoints

## Per-Phase Context

| Phase | Attach | Invoke skill | Update artifacts |
|-------|--------|--------------|------------------|
| Requirements | `requirements-analysis.md` | `capture-prompt-session` | `requirements-analysis.md`, `acceptance-criteria.md` |
| Design | `design-notes.md`, `data-model.md`, `ui-flow.md` | `capture-prompt-session` | Same + `api-contract.md` draft |
| Backend API | Router files, `api-contract.md` | `sync-api-docs` | `api-contract.md`, `data-model.md` |
| State machine | `ticket_state_machine` service | `write-state-machine-tests` | `test-results.md` |
| Frontend | Page components, `ui-flow.md` | `review-ticket-feature` | `ui-flow.md` if flows change |
| Debug | Error response, logs, failing test | `debug-backend-issue` | `debugging-notes.md` |
| Review | Git diff, `acceptance-criteria.md` | `review-ticket-feature` | `code-review-notes.md` |
| Milestone | — | `capture-prompt-session` | `implementation-plan.md`, `pr-description.md` |

## Context to Avoid Sharing

- Real `.env` values or production credentials
- Personal data unrelated to seeded test users
- Entire unrelated chat histories — curate excerpts into `ai-prompts/`

## Anti-Patterns

| Bad | Better |
|-----|--------|
| "Build the ticket API" (no context) | "@api-contract.md implement POST /api/tickets per contract" |
| One giant chat for whole project | Phase-specific sessions captured to `ai-prompts/` |
| Fixing status in router inline | "@state-machine.mdc implement service + tests" |
| Skipping doc update after route change | Run `sync-api-docs` same session |

## Prompt Templates

Reusable starters live in [prompt-templates.md](./prompt-templates.md).
