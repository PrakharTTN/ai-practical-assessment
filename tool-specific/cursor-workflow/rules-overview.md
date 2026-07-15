# Cursor Rules Overview

Rules live in `.cursor/rules/` and auto-apply based on `alwaysApply` or file globs.

## Rule Index

| Rule | Scope | Purpose |
|------|-------|---------|
| [project-context.mdc](../../.cursor/rules/project-context.mdc) | Always | Stack, entities, core behaviors, folder layout |
| [state-machine.mdc](../../.cursor/rules/state-machine.mdc) | Backend, frontend, tests | Exact ticket status transitions |
| [api-contract-sync.mdc](../../.cursor/rules/api-contract-sync.mdc) | Routers + `api-contract.md` | Contract stays aligned with routes |
| [api-error-shape.mdc](../../.cursor/rules/api-error-shape.mdc) | Backend + frontend | Consistent error JSON for UI |
| [testing-discipline.mdc](../../.cursor/rules/testing-discipline.mdc) | Tests | Real-DB state machine integration tests |
| [security-and-env.mdc](../../.cursor/rules/security-and-env.mdc) | Always | No secrets; env-based config |
| [artifact-discipline.mdc](../../.cursor/rules/artifact-discipline.mdc) | Markdown artifacts | Lifecycle docs updated with work |

## What Each Rule Prevents

### project-context.mdc
- Wrong stack choices (e.g., Django, SQLite) mid-project
- User-management UI scope creep
- Status changes bypassing backend
- Code in wrong directories
- Neglecting assessment artifacts

### state-machine.mdc
- Illegal transitions (`open` → `resolved`, reopening `closed` tickets)
- Status mutation via general PATCH instead of dedicated endpoint
- Frontend offering invalid next statuses
- Undocumented extra transitions

### api-contract-sync.mdc
- Drift between implemented routes and `api-contract.md`
- Missing auth/error documentation for reviewers
- Shipping API changes without updating contract or data model

### api-error-shape.mdc
- Inconsistent error formats breaking React error UI
- Leaking stack traces or SQL to clients
- Pydantic default 422 shape without field mapping
- HTTP 200 responses carrying error payloads

### testing-discipline.mdc
- Mock-only or SQLite tests for mandatory state-machine proof
- Incomplete invalid-transition coverage
- Marking status feature done without passing integration tests
- Missing `test-results.md` evidence

### security-and-env.mdc
- Committed `.env`, JWT secrets, or database passwords
- Hardcoded credentials in source
- CSV export exposing other users' tickets
- Plaintext password storage

### artifact-discipline.mdc
- Empty placeholder docs at submission
- Missing prompt history for assessment feedback
- Fabricated debugging/review notes
- API changes without lifecycle paper trail

## Skills Complementing Rules

| Skill | Pairs with |
|-------|------------|
| `sync-api-docs` | `api-contract-sync.mdc` |
| `write-state-machine-tests` | `testing-discipline.mdc`, `state-machine.mdc` |
| `debug-backend-issue` | `api-error-shape.mdc`, `state-machine.mdc` |
| `review-ticket-feature` | All rules + `acceptance-criteria.md` |
| `capture-prompt-session` | `artifact-discipline.mdc` |
| `docker-up-local` | `security-and-env.mdc`, `debug-backend-issue` |

### docker-up-local

Starts postgres + backend + frontend via `docker compose` for manual smoke testing (stretch workflow).

**Prevents:**
- Wrong build context paths after repo layout changes
- Starting stack without `.env` or executable entrypoint scripts
- Using real secrets in committed env files
- Undocumented Docker failures (guides `debugging-notes.md` entry)
- Claiming app verification without running the post-startup checklist

See [context-strategy.md](./context-strategy.md) for how to combine rules, skills, and docs in Cursor sessions.
