# Implementation Plan

## Overview

Build the Support Ticket Management System in thin vertical slices, proving the state machine and persistence early. Backend and integration tests lead; frontend follows once API contract is stable. Lifecycle artifacts update in the same session as each milestone — not batched at the end.

**Estimated Core effort:** 8–12 focused hours across milestones M1–M7. M8 (docs/review) overlaps the full week.

**Stack:** `src/frontend/` (React + Vite + TS) · `src/backend/` (FastAPI) · PostgreSQL · Alembic · pytest · JWT auth

## Milestones

### M1 — Structure

**Goal:** Runnable repo skeleton; no business logic yet.

| Task | Output |
|------|--------|
| Confirm folder layout | `src/frontend/`, `src/backend/`, `tests/`, `database/` |
| Backend package scaffold | `app/main.py`, config, CORS, `/health` |
| Frontend scaffold | Vite + React + TS, router shell, env for `VITE_API_URL` |
| Root tooling | `.env.example`, `.gitignore`, README skeleton |
| Test harness placeholder | `tests/backend/conftest.py` stub |

**Done when:** `uvicorn` and `npm run dev` start locally; README lists prerequisites.

**Status:** Complete.

---

### M2 — Workflow / Rules

**Goal:** Cursor rules and skills guide consistent AI-assisted development.

| Task | Output |
|------|--------|
| Project rules | `.cursor/rules/*.mdc` (context, state machine, API sync, errors, tests, security, artifacts) |
| Skills | `tool-specific/cursor-workflow/skills/*` |
| Prompt templates | `prompt-templates.md`, `context-strategy.md` |
| Docker stretch | `docker-compose.yml`, `docker-up-local` skill |

**Done when:** Rules reference exact transitions; skills document when to use and which files to update.

**Status:** Complete.

---

### M3 — Database

**Goal:** Schema, migrations, seed data — persistence foundation.

| Task | Output |
|------|--------|
| SQLAlchemy models | `User`, `Ticket`, `Comment` per `data-model.md` |
| Alembic setup | `alembic.ini`, `alembic/versions/001_initial.py` |
| Enums | `priority`, `status` as DB-level or app-level enums |
| Seed script | `app/seed.py` — 2+ users (bcrypt passwords), tickets in each status, comments |
| Setup docs | `database/setup-notes.md` updated |

**Done when:** `alembic upgrade head` + `python -m app.seed` populates DB; data visible in psql; survives restart.

**Status:** Complete.

---

### M4 — Backend

**Goal:** Full API per `api-contract.md`; state machine enforced in service layer.

| Task | Output |
|------|--------|
| Auth | `POST /api/auth/login`, JWT middleware, `get_current_user` dependency |
| Ticket CRUD | list (with search/filter), create, get, patch (no status field) |
| Status endpoint | `PATCH /api/tickets/{id}/status` → `ticket_state_machine.py` |
| Comments | `POST /api/tickets/{id}/comments` |
| CSV export | `GET /api/tickets/export` scoped to `createdBy` |
| Error handlers | Unified `{ error, message, details }` shape |
| Sync contract | `api-contract.md` matches all routes |

**Done when:** All endpoints pass manual curl/Postman checks; invalid transitions return `invalid_status_transition`; `sync-api-docs` skill validates contract.

**Status:** Complete.

---

### M5 — Tests

**Goal:** Mandatory assessment proof — real-DB state machine integration tests.

| Task | Output |
|------|--------|
| Test DB fixture | PostgreSQL test database; rollback between tests |
| Auth fixture | Login helper returning Bearer headers |
| State machine tests | `tests/backend/integration/test_ticket_status_transitions.py` |
| Additional integration tests | create validation, export scoping, 401 without token |
| Record results | `test-results.md`, `test-strategy.md` checkboxes |

**Done when:** `pytest tests/backend/integration -v` all green; valid + invalid transitions covered per `testing-discipline.mdc`.

**Status:** Complete (45 backend tests).

**Use skill:** `write-state-machine-tests`

---

### M6 — Frontend

**Goal:** UI covering all Core flows with meaningful error states.

| Task | Output |
|------|--------|
| Auth pages | Login (styled), logout, token storage, protected route + session restore |
| Ticket list | Table, search/filter, export, professional app shell |
| Create ticket | Form with validation error display |
| Ticket detail | View + edit fields, assignee select, comment thread, workflow panel |
| Status actions | Buttons derived from current status; error on invalid attempt |
| CSV export | Download button calling export endpoint |
| Error UX | API `message` + field `details` mapping |
| User management | Admin Team page: create + edit users |
| Component tests | Vitest + RTL (14 tests) |
| Default admin | `admin@admin.com` / `admin` on first seed; documented, not on login UI |

**Done when:** Full manual walkthrough passes acceptance criteria; `ui-flow.md` matches implementation.

**Status:** Complete (user verified).

**Build order within M6:** auth shell → list → create → detail/read → update → comments → status actions → export → filter → team management → styling polish.

---

### M7 — Docs / Review

**Goal:** Submission-ready artifacts and honest review trail.

| Task | Output |
|------|--------|
| README | Full local setup + Docker + test commands |
| Design artifacts | `design-notes.md`, `data-model.md`, `ui-flow.md` finalized |
| AI workflow | `tool-workflow.md`, `ai-prompts/*` curated sessions |
| Review | `code-review-notes.md`, `review-fixes.md` via `review-ticket-feature` skill |
| Closure | `reflection.md`, `pr-description.md`, `final-ai-usage-summary.md`, `candidate-info.md` |

**Done when:** Mentor can clone repo, follow README, run tests, and trace AI workflow without asking questions.

---

## Task Breakdown (dependency order)

```
M1 Structure
  └─ M2 Workflow/Rules ✓
       └─ M3 Database
            └─ M4 Backend (auth → tickets → status → comments → export)
                 ├─ M5 Tests (can start after status endpoint)
                 └─ M6 Frontend (after auth + list endpoints exist)
                      └─ M7 Docs/Review (continuous; finalize at end)
```

## AI Usage Plan

| Milestone | How to use Cursor |
|-----------|-------------------|
| M1–M2 | Context via rules; capture sessions to `ai-prompts/planning.md` |
| M3 | `@data-model.md` + design rule; review generated models for FK/nullable correctness |
| M4 | `@api-contract.md` + `state-machine.mdc`; invoke `sync-api-docs` after each router |
| M5 | `write-state-machine-tests` skill; reject mocked-DB test suggestions |
| M6 | `@ui-flow.md` + `api-error-shape.mdc`; `review-ticket-feature` per page |
| M7 | `capture-prompt-session`; `review-ticket-feature` for final pass |

**Per session:** attach relevant artifact, invoke skill if one fits, update docs same session.

## Risks

| Risk | Impact | Likelihood |
|------|--------|------------|
| State machine logic duplicated in router and service | Drift; invalid transitions slip through | Medium |
| Status updatable via general PATCH | Breaks assessment signature requirement | Medium |
| Tests use SQLite or mocked DB | Mandatory integration proof invalid | Medium |
| `api-contract.md` drifts from code | Reviewer confusion; lost ownership signal | High |
| AI generates auth bypass or client-set `createdBy` | Security flaw; wrong CSV scope | Medium |
| Scope creep (user CRUD, notifications) | Core late; artifacts thin | Medium |
| Docker/port conflicts block local demo | Cannot manually verify | Low |
| Frontend builds before API stable | Rework; inconsistent error handling | Medium |
| Secrets committed in `.env` | Assessment failure; security issue | Low |
| Time spent on app vs artifacts | Weak feedback on AI workflow | High |

## Mitigation

| Risk | Mitigation |
|------|------------|
| State machine duplication | Single `ticket_state_machine.py`; routers call it; rule enforces; integration tests |
| Status via PATCH | Pydantic schema for update excludes `status`; test asserts rejection |
| SQLite/mock tests | `testing-discipline.mdc`; `write-state-machine-tests` skill; CI/local Postgres only |
| Contract drift | `api-contract-sync.mdc`; `sync-api-docs` skill after every router change |
| Auth/`createdBy` bypass | JWT dependency on all write routes; test that spoofed `createdBy` is ignored |
| Scope creep | `acceptance-criteria.md` as gate; defer Stretch unless time remains |
| Docker issues | `docker-up-local` skill + `debugging-notes.md`; document native setup as fallback |
| Frontend rework | Complete M4 auth + list + status endpoints before M6; use `api-contract.md` |
| Secrets | `.env.example` only; `security-and-env.mdc`; review diff before commit |
| Thin artifacts | `artifact-discipline.mdc`; `capture-prompt-session` after each milestone |

## Current Status

| Milestone | Status |
|-----------|--------|
| M1 Structure | **Complete** |
| M2 Workflow/Rules | **Complete** |
| M3 Database | **Complete** |
| M4 Backend | **Complete** |
| M5 Tests | **Complete** |
| M6 Frontend | **Complete** (incl. user management + styling) |
| M7 Docs/Review | **Complete** |

**Status:** Complete.

---

## Project complete

All milestones M1–M7 delivered. See [candidate-info.md](./candidate-info.md) for submission index.
