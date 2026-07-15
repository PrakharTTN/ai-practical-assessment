# Requirement Analysis

## Selected Project Option

**Support Ticket Management System** — backend-heavy full-stack assessment project.

## My Understanding (in your own words)

Internal support staff need a small web app to track tickets from creation through resolution. Users log in, create tickets with title/description/priority, assign them, add comments as work progresses, and move tickets through a **fixed lifecycle** — not free-form status edits.

The system is intentionally small: three entities (User, Ticket, Comment), a state machine that gates every status change, and admin-managed user onboarding (seed provides default admin on first startup). The assessment cares as much about **how the work was done with AI** (planning artifacts, prompt history, tests, debugging notes) as about the running app.

We are building Core features first, plus **JWT authentication** (assessment Stretch, but required for our design because CSV export scopes to the logged-in user's tickets via `createdBy`).

**Stack:** React + Vite + TypeScript · FastAPI · PostgreSQL · SQLAlchemy + Alembic · pytest integration tests against real Postgres.

## Functional Requirements

### Authentication
- `POST /api/auth/login` with email + password returns JWT
- All ticket/comment/export routes require valid Bearer token
- Frontend stores token, redirects unauthenticated users to login
- `createdBy` on new tickets and comments derived from JWT — never from client-supplied user ID

### Tickets
- **Create:** title, description, priority (low | medium | high); status defaults to `open`; `createdBy` = authenticated user
- **List:** all tickets from DB; at least one search or filter (e.g. by status, priority, or title substring)
- **Detail:** single ticket with comments, assignee, timestamps
- **Update:** title, description, priority, `assignedTo` — **status is not updatable via this endpoint**
- **Status change:** dedicated `PATCH /api/tickets/{id}/status` enforced by state machine service
- **Export:** `GET /api/tickets/export` returns CSV of tickets where `createdBy` = authenticated user

### Comments
- Add comment to ticket: `message` required; `createdBy` from JWT
- Comments visible on ticket detail; ordered by `createdAt` ascending

### Users
- Default admin seeded on first startup (`admin@admin.com` / `admin`) — documented in `database/seed-data/README.md`
- Admin can create and edit users (admin or support role) via `/users` UI and API
- Support agents can list users (assignee picker) but cannot create/edit users
- `assignedTo` references any user; nullable (unassigned ticket allowed)

### Status State Machine (signature area)

Canonical values: `open`, `in_progress`, `resolved`, `closed`, `cancelled`

| From | Allowed targets |
|------|-----------------|
| `open` | `in_progress`, `cancelled` |
| `in_progress` | `resolved`, `cancelled` |
| `resolved` | `closed` |
| `closed` | *(terminal — no transitions)* |
| `cancelled` | *(terminal — no transitions)* |

Backend is the authority. Frontend shows only valid next actions for the current status.

## Non-Functional Requirements

- **Persistence:** PostgreSQL; data survives app/container restart
- **Migrations:** Alembic scripts in repo; runnable from README and Docker entrypoint
- **Seed data:** at least 2 users, several tickets in varied statuses, sample comments
- **Validation:** Pydantic on all inputs; DB constraints on enums/FKs
- **Error handling:** consistent JSON `{ error, message, details }`; UI displays messages and field errors
- **Security:** no secrets in repo; `.env.example` only; bcrypt passwords; JWT for API auth
- **Testing:** integration tests on real PostgreSQL proving state machine rules (mandatory)
- **Documentation:** README setup, api-contract.md kept in sync with routes
- **AI workflow:** lifecycle artifacts and curated prompt history (10–15 sessions)

## Assumptions

1. Single-tenant internal tool — no org/team scoping
2. All authenticated users can view all tickets (no row-level read restriction in Core)
3. Any authenticated user can update any ticket and add comments (no role-based write restrictions unless added as Stretch)
4. `assignedTo` can be any seeded user or null; assignee change does not auto-transition status
5. Search/filter is server-side query param on list endpoint (not client-only filtering)
6. CSV export includes ticket fields + enough detail for offline review; comments optional in export (document choice in api-contract)
7. Timestamps stored UTC in DB; displayed in local time in UI
8. Ticket title max length ~200 chars; description and comment message are text fields with reasonable max (e.g. 5000)

## Clarifications (questions for a product owner)

| # | Question | Decision |
|---|----------|----------|
| 1 | How identify user without auth UI? | JWT login; `createdBy` from token |
| 2 | Preferred stack? | FastAPI + PostgreSQL + React/Vite |
| 3 | Can resolved tickets be reopened? | **No** — not in allowed transitions |
| 4 | Same-status transition (open → open)? | **Reject** — treat as invalid/no-op failure |
| 5 | Who can export CSV? | Authenticated user; only their `createdBy` tickets |
| 6 | Delete ticket or comment? | **Out of scope** for Core unless added later |

## Edge Cases

### State machine
- **Skip-ahead:** `open` → `resolved` or `closed` → must 400/422 with `invalid_status_transition`
- **Reopen:** `in_progress` → `open`, `resolved` → `in_progress`, `closed` → anything → rejected
- **Terminal states:** any transition from `closed` or `cancelled` → rejected
- **Same status:** `open` → `open` → rejected (not silently accepted)
- **Concurrent updates:** two users transition same ticket simultaneously → second request sees current DB status; may fail if first already moved (acceptable; no optimistic locking required for Core)
- **Status via general PATCH:** client sends `status` in ticket update body → backend ignores or rejects; only status endpoint may change it
- **Missing ticket on status change:** 404 before state machine check

### Validation
- Empty title, description, or comment message → 422 with field details
- Invalid priority enum → 422
- `assignedTo` referencing non-existent user → 404 or 422
- Invalid status string in status endpoint → 422 before transition logic

### Auth
- Missing/expired/invalid JWT → 401 on protected routes
- Login with wrong password → 401 (generic message, no email enumeration)
- Export without auth → 401
- Client sends `createdBy` in create body → ignored; server sets from JWT

### List / search / filter
- Filter returning zero results → 200 with empty array, not 404
- Search string with SQL-special chars → parameterized queries only (no injection)
- Combined filters (status + priority) → AND logic

### CSV export
- User with zero self-created tickets → valid CSV with headers only (or empty body — document in contract)
- Export must not include other users' tickets even if user can see them in list
- Large export → acceptable for assessment scale; no pagination required

### Persistence / ops
- DB down on startup → backend fails health check; Docker entrypoint retries
- Migration not run → app must not silently run against wrong schema
- Restart mid-request → standard HTTP semantics; no partial comment without ticket

### UI
- Invalid transition clicked → show API `message`; ticket detail still shows correct current status
- Network failure on create → form retains input; error banner shown
- Token expired mid-session → redirect to login with message
