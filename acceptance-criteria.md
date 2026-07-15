# Acceptance Criteria

Use this as the definition-of-done checklist. Each item is verifiable via UI action, API call, or test run.

## Core — Tickets

- [x] Authenticated user can create a ticket with title, description, and priority via the UI
- [x] Created ticket appears in the list with status `open` and `createdBy` matching the logged-in user
- [x] User can view all tickets loaded from the database (not hardcoded/mock data)
- [x] User can open a ticket detail view showing title, description, priority, status, assignee, timestamps, and comments
- [x] User can update ticket title, description, priority, and assignee from the UI
- [x] Ticket updates persist after page refresh
- [x] User can add a comment on a ticket; comment appears on detail view with author and timestamp
- [x] At least one search or filter works on the ticket list (e.g. filter by status or search by title)

## Core — Status State Machine

- [x] `open` → `in_progress` succeeds (API 2xx; UI reflects new status)
- [x] `open` → `cancelled` succeeds
- [x] `in_progress` → `resolved` succeeds
- [x] `in_progress` → `cancelled` succeeds
- [x] `resolved` → `closed` succeeds
- [x] `open` → `resolved` is rejected by API with `error: invalid_status_transition`
- [x] `open` → `closed` is rejected
- [x] `in_progress` → `open` is rejected
- [x] `resolved` → `in_progress` is rejected
- [x] `closed` → `open` is rejected
- [x] `cancelled` → `in_progress` is rejected
- [x] Same-status transition (e.g. `open` → `open`) is rejected
- [x] Frontend does not offer invalid transition actions for the current status
- [x] Frontend displays a clear error message when an invalid transition is attempted
- [x] Status cannot be changed via the general ticket update endpoint (only via status endpoint)

## Core — CSV Export

- [x] Authenticated user can export CSV of their self-created tickets from the UI
- [x] CSV contains ticket detail fields (id, title, description, priority, status, assignee, timestamps)
- [x] CSV does **not** include tickets created by other users
- [x] Export requires authentication (401 without token)

## Core — Persistence

- [x] Data remains available after backend restart
- [x] Data remains available after PostgreSQL container restart (with volume retained)
- [x] Alembic migration scripts exist and apply cleanly on fresh database
- [x] Seed script populates sample users, tickets, and comments

## Validation

- [x] `POST /api/tickets` without title returns 422 with field-level error
- [x] `POST /api/tickets` without description returns 422
- [x] `POST /api/tickets` with invalid priority returns 422
- [x] `POST /api/tickets/{id}/comments` with empty message returns 422
- [x] `assignedTo` with non-existent user ID returns 4xx with clear error
- [x] Invalid status value in status endpoint returns 422 before transition check
- [x] Client-supplied `createdBy` on create is ignored; server uses JWT subject

## Error Handling

- [x] API errors use shape `{ "error": "<code>", "message": "<text>", "details": {} }`
- [x] `invalid_status_transition` errors include `current_status` and `requested_status` in response
- [x] UI shows API error `message` on failed create/update/status/comment
- [x] UI maps 422 `details` to form field errors on ticket create/update
- [x] 401 responses redirect user to login on the frontend

## Authentication

- [x] `POST /api/auth/login` returns JWT for valid user credentials
- [x] Invalid login returns 401 without revealing whether email exists
- [x] Protected API routes reject missing or expired JWT with 401
- [x] Frontend login/logout flow works; protected routes require auth
- [x] Passwords stored as bcrypt hashes only (never plaintext in DB or code)
- [x] Default admin created on first startup (`admin@admin.com` / `admin`) — documented in `database/seed-data/README.md`, not shown on login page

## User Management (post-M6 enhancement)

- [x] Admin can create new users (admin or support role) via `/users` UI
- [x] Admin can edit existing users (name, email, role, optional password reset)
- [x] Support agents cannot access user create/update endpoints (403)
- [x] Duplicate email rejected on create and update (409)

## Testing

- [x] Integration test suite runs against real PostgreSQL (not SQLite, not mocked DB)
- [x] Parametrized or individual tests cover all five valid transitions (pass)
- [x] Integration tests cover at least six invalid transitions listed above (fail with `invalid_status_transition`)
- [x] Test run results recorded in `test-results.md`
- [x] `pytest` command documented in README and passes locally
- [x] Frontend component tests (Vitest) cover status helpers, auth guard, and error display

## Documentation

- [x] README instructions bring up backend, frontend, and database from clean clone
- [x] `.env.example` committed with placeholder values only; `.env` gitignored
- [x] `api-contract.md` documents every implemented route including auth and errors
- [x] `database/setup-notes.md` describes migrate + seed steps
- [x] No secrets, tokens, or real passwords in git history

## Stretch (optional — partial credit)

- [x] Docker Compose starts postgres + backend + frontend (`docker-up-local` skill)
- [x] OpenAPI/Swagger available at `/docs` and matches implemented routes
- [x] Role-based access for user management (admin-only create/edit users)
- [ ] Role-based ticket transitions (e.g. only assignee can transition) — not implemented

## Definition of Done (submission)

- [x] All Core checkboxes above pass
- [x] `requirements-analysis.md`, `acceptance-criteria.md`, `implementation-plan.md` complete
- [x] Prompt history captured in `ai-prompts/` (15 curated sessions)
- [x] `reflection.md` and `pr-description.md` written
- [x] `final-ai-usage-summary.md` and `candidate-info.md` complete
- [x] `debugging-notes.md` documents investigated issues
