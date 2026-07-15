# Final AI Usage Summary

## Overview

**Tool:** Cursor Agent (Composer) with project rules (`.cursor/rules/*.mdc`), skills (`tool-specific/cursor-workflow/skills/*`), and lifecycle markdown artifacts as persistent context.

**Project:** Support Ticket Management System — FastAPI + PostgreSQL + React/Vite assessment.

**Approach:** Milestone-driven (M1–M7), contract-first API, real-DB integration tests, docs updated in the same session as code changes.

## Sessions

| # | Phase | File | Title |
|---|-------|------|-------|
| 1 | Planning | `planning.md` | Planning documents from assessment context |
| 2 | Design | `design.md` | Data model and database schema (M3) |
| 3 | Design | `design.md` | API contract and UI flow |
| 4 | Implementation | `implementation.md` | M3 — Database layer |
| 5 | Implementation | `implementation.md` | M4 — Backend API |
| 6 | Implementation | `implementation.md` | M6 — Frontend core |
| 7 | Implementation | `implementation.md` | M6 — User management and styling |
| 8 | Testing | `testing.md` | M5 — Backend integration tests |
| 9 | Testing | `testing.md` | M6 — Frontend tests and Docker verify |
| 10 | Debugging | `debugging.md` | Migration and seed failures |
| 11 | Debugging | `debugging.md` | Port 5432 and bcrypt/test issues |
| 12 | Debugging | `debugging.md` | Docker full-stack verification |
| 13 | Debugging | `debugging.md` | Login UX and default admin |
| 14 | Documentation | `documentation.md` | Lifecycle MD updates + debugging notes |
| 15 | Code review | `code-review.md` | M3 DB review + M7 final submission review |

**Total curated sessions:** 15

## Key Prompts and Outcomes

| Phase | Prompt Summary | Accepted | Changed | Rejected |
|-------|----------------|----------|---------|----------|
| Planning | Scope brief into requirements, acceptance criteria, M1–M7 plan | Milestone order, JWT in-scope, state machine rules | Auth required for CSV scope | User CRUD UI, reopen transitions |
| Design | Schema + contract + ui-flow | Layered arch, error shape, status endpoint isolation | Contract grew with features | GraphQL |
| Implementation | M3–M4 backend + DB | State machine service, real Postgres, JWT `created_by` | validation_alias for nested users | SQLite, status in PATCH |
| Implementation | M6 frontend + polish | Vitest, styled UI, admin Team page | User mgmt beyond original Core | Credentials on login, Redux |
| Testing | 45 pytest + 14 Vitest | Real DB integration, transition matrix | — | Mocked DB |
| Debugging | Migration/seed/port/bcrypt | Documented in debugging-notes | Reverted 5433 port experiment | — |
| Review | M3 + M7 final pass | Critical migration fixes applied | — | DB triggers for state machine |
| Documentation | MDs + M7 closure | Full artifact trail | — | Empty templates left unfilled |

## Lessons Learned

1. **Attach artifacts** — `@api-contract.md` and `@acceptance-criteria.md` reduced drift between AI suggestions and requirements.
2. **Test early on real Postgres** — caught bcrypt and enum issues before frontend work.
3. **Rules enforce non-negotiables** — `state-machine.mdc` and `testing-discipline.mdc` blocked bad shortcuts (SQLite, duplicated transitions).
4. **Same-session doc updates** — `artifact-discipline.mdc` kept reviewers unblocked; debugging-notes should be filled when issues occur, not at the end.
5. **Skills for repeatable ops** — `docker-up-local` and `write-state-machine-tests` saved re-explaining setup each session.
6. **Validate AI output** — autoincrement and enum bugs required human review + test runs; don't trust generated migrations blindly.

## Reusable Artifacts

| Artifact | Path |
|----------|------|
| Cursor rules | `.cursor/rules/*.mdc` |
| Skills | `tool-specific/cursor-workflow/skills/*` |
| Docker stack | `docker-compose.yml`, `scripts/docker/*` |
| Prompt templates | `tool-specific/cursor-workflow/prompt-templates.md` |
| Context strategy | `tool-specific/cursor-workflow/context-strategy.md` |
| API contract template | `api-contract.md` |
| Test results record | `test-results.md` |
| Debugging log format | `debugging-notes.md` |

## Outcome

Submission-ready repo: runnable app (Docker or native), **45 + 14** automated tests, full lifecycle documentation, and traceable AI workflow across 15 curated sessions.
