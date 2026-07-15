# Implementation Prompts

## Session: M3 — Database layer

**Date:** 2026-07-10

### Prompt

Proceed with M3. Scaffold models, Alembic, seed. Update MDs after completion.

### AI Response Summary

Implemented `app/models/*`, `alembic/versions/001_initial_schema.py`, `app/seed.py`, `app/database.py`. Ran migrate + seed instructions in setup docs.

### Accepted

- PostgreSQL native enums with `values_callable` for lowercase values
- Idempotent seed (skip if users exist)
- Dev credentials documented in `database/seed-data/README.md`

### Changed

- Fixed autoincrement and enum issues found during review (see `debugging-notes.md`)

### Rejected

- SQLite fallback for local dev

---

## Session: M4 — Backend API

**Date:** 2026-07-10 – 2026-07-15

### Prompt

Proceed with M4 backend — full API per contract: auth, tickets CRUD, status state machine, comments, CSV export, search/filter.

### AI Response Summary

Built routers (`auth`, `users`, `tickets`), `ticket_state_machine.py`, JWT deps, Pydantic schemas, unified `AppError` handlers. Synced `api-contract.md` after each route group.

### Accepted

- Single state machine service — routers delegate, no duplicated transition logic
- `created_by` from JWT on ticket/comment create
- CSV export scoped to authenticated user's created tickets
- `GET /api/users` for assignee picker

### Changed

- Pydantic `validation_alias` for ORM relationship names (`creator` → `created_by`)

### Rejected

- Accepting `status` in general ticket PATCH body

---

## Session: M6 — Frontend core

**Date:** 2026-07-15

### Prompt

Delete `raw-context.md`, proceed with M6 frontend. Update required MDs after each stage.

### AI Response Summary

Built React SPA: AuthContext, API client, Login/List/Create/Detail pages, status actions, CSV export, search/filter. Vitest setup with component tests.

### Accepted

- React Router + ProtectedRoute + Layout
- sessionStorage for JWT
- Status buttons from `getAllowedTransitions()` only
- CSS in `styles.css` without UI framework dependency

### Changed

- Port remains 5432 after user stopped conflicting local Postgres

### Rejected

- Redux/global ticket store
- Client-only filtering

---

## Session: M6 — User management, styling, and polish

**Date:** 2026-07-15

### Prompt

(1) Remove seeded credentials from login; default admin `admin@admin.com`. (2) Professional post-login styling. (3) Admin user create/edit. User verified M6.

### AI Response Summary

Added `POST/PATCH /api/users`, `GET /api/auth/me`, Team page, AdminRoute, app shell redesign. Updated seed, docs, 13 user API tests. Curated debugging and review notes.

### Accepted

- Admin-only user management via `require_admin`
- Credentials documented off-UI in `database/seed-data/README.md`
- Edit user with optional password reset
- Professional login + app shell styling

### Changed

- Expanded scope beyond original "no user CRUD UI" — admin onboarding added per user feedback

### Rejected

- Showing dev passwords on login page
- Delete user endpoint (out of scope)
