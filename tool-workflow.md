# Tool Workflow

## Primary AI Tool Used

**Cursor** — Agent mode with project rules (`.cursor/rules/*.mdc`), skills (`tool-specific/cursor-workflow/skills/*`), and lifecycle markdown artifacts as context.

## How I Provide Project Context to the Tool

- **Rules:** `project-context.mdc`, `state-machine.mdc`, `api-contract-sync.mdc`, `testing-discipline.mdc`, `artifact-discipline.mdc`, `security-and-env.mdc`
- **Planning artifacts:** `@requirements-analysis.md`, `@implementation-plan.md`, `@acceptance-criteria.md`, `@api-contract.md`, `@ui-flow.md`
- **Skills:** `docker-up-local`, `write-state-machine-tests`, `sync-api-docs`, `review-ticket-feature`, `capture-prompt-session`
- **Per-milestone:** attach only files relevant to the current slice (e.g. router + contract for API work)

## How I Use AI for Requirement Analysis

- Pasted raw assessment brief; asked for scope summary and clarifying questions before coding
- Produced `requirements-analysis.md`, `acceptance-criteria.md`, `implementation-plan.md`
- Captured decisions (no reopen, same-status rejected, JWT for `createdBy`) in analysis doc

## How I Use AI for Planning and Design

- Milestone-driven plan (M1–M7) with dependency order
- `data-model.md`, `design-notes.md`, `api-contract.md` written before/alongside implementation
- State machine documented in rules + contract before status endpoint coded

## How I Use AI for Code Generation

- Thin vertical slices: DB → backend API → tests → frontend pages
- Explicit instructions to follow existing patterns, minimal diffs, no new dependencies unless needed
- Router changes paired with `api-contract.md` updates (enforced by rule)

## How I Validate AI-Generated Code

- `pytest tests/backend` on real PostgreSQL (45 tests)
- `npm test` + `npm run build` for frontend
- Docker full-stack smoke via `docker-up-local` skill
- Manual browser verification for UI flows (user confirmed team management + styling)
- Code review passes documented in `code-review-notes.md` and `review-fixes.md`

## How I Use AI for Testing

- `write-state-machine-tests` skill for mandatory transition tests
- Integration tests for auth, tickets, export, user management
- Vitest component tests for status helpers, ProtectedRoute, ErrorBanner
- Results recorded in `test-results.md`

## How I Use AI for Debugging

- `debugging-notes.md` for dated issue records (migration, port, bcrypt, API aliases, Docker)
- `ai-prompts/debugging.md` for curated debug sessions
- `docker-up-local` skill log classification table
- Iterative fix: capture logs → smallest change → re-run tests

## How I Use AI for Code Review

- `review-ticket-feature` style passes after milestones
- Findings tracked in `code-review-notes.md`; fixes in `review-fixes.md`
- Rejected over-engineering (DB triggers, UUID PKs) documented with rationale

## What Information I Avoid Sharing Unnecessarily with AI Tools

- Real `.env` values, production secrets, personal data
- Per `security-and-env.mdc` and `context-strategy.md`

## How I Would Reuse This Workflow in a Real Project

1. Rules + skills repo template for stack (FastAPI/React/Postgres)
2. Contract-first API with sync rule on every router change
3. Milestone plan with acceptance criteria as definition of done
4. Real-DB integration tests from day one for critical business logic
5. `capture-prompt-session` to `ai-prompts/` for audit trail
6. Docker skill for reproducible local onboarding

**M7 remaining:** Curate 10–15 prompt sessions in `ai-prompts/` and `final-ai-usage-summary.md` — **done** (15 sessions).
