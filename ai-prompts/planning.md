# Planning Prompts

## Session: Planning documents from assessment context
**Date:** 2026-07-10

### Prompt

Restore `raw-context.md` and create planning documents only:
1. `requirements-analysis.md`
2. `acceptance-criteria.md`
3. `implementation-plan.md`

Requirements: practical engineering language (no filler); edge cases especially for status state machine; testable checkbox acceptance criteria; implementation plan with milestones (structure → workflow/rules → database → backend → tests → frontend → docs/review); risks and mitigation. No code. Also create a paste-ready summary entry in `ai-prompts/planning.md`.

Context from prior sessions: FastAPI + PostgreSQL + React/Vite stack; JWT auth for `createdBy` and CSV export; Cursor rules/skills and Docker stretch already scaffolded.

### AI Response Summary

- Restored `raw-context.md` at repo root from assessment brief
- Wrote `requirements-analysis.md` covering functional/non-functional requirements, assumptions, PO clarifications table, and edge cases (state machine, auth, export, validation, concurrency, UI)
- Wrote `acceptance-criteria.md` as verifiable checkboxes grouped by tickets, state machine, CSV, persistence, validation, errors, auth, testing, docs
- Wrote `implementation-plan.md` with milestones M1–M7, dependency diagram, AI usage plan per milestone, risks/mitigations table, and current status tracker (M2 complete, next M3 database)

### Accepted

- Milestone order: structure → workflow/rules → database → backend → tests → frontend → docs/review
- JWT auth treated as in-scope (not deferred) because CSV export depends on authenticated `createdBy`
- Exact five allowed transitions and explicit invalid-transition test cases in acceptance criteria
- Same-status transition rejected (not silent no-op)
- Status changes isolated to dedicated endpoint; general PATCH cannot change status
- Risks table includes contract drift, SQLite tests, and artifact neglect as high-priority items

### Changed

- Expanded assessment's optional auth to **required for this project** based on prior team decision (not in raw brief alone)
- Added Docker milestone completion note under M2 (stretch workflow already built)
- CSV edge case: empty export returns valid CSV with headers rather than error
- M5 tests can start after status endpoint exists (parallel with rest of M4) — not strictly after full backend

### Rejected

- User-management CRUD UI — remains out of scope per assessment Core
- Ticket/comment delete — marked out of scope unless product owner adds later
- Role-based write restrictions — deferred to Stretch; assumed all authenticated users can edit any ticket for Core
- Reopen transitions (`resolved` → `in_progress`) — explicitly rejected; not in assessment state machine
- Client-only filtering without server query param — rejected; filter must hit backend per assessment
