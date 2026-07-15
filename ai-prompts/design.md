# Design Prompts

## Session: Data model and database schema (M3)

**Date:** 2026-07-10

### Prompt

Proceed with M3 database — models, Alembic migration, seed script per `data-model.md` and `implementation-plan.md`.

### AI Response Summary

Created SQLAlchemy models (`User`, `Ticket`, `Comment`), PostgreSQL enums, `001_initial_schema.py`, idempotent `app/seed.py` with bcrypt passwords, and updated `database/setup-notes.md`.

### Accepted

- Three-table schema with FK delete rules (SET NULL assignee, RESTRICT creator, CASCADE comments)
- Indexes on status, priority, created_by for filter/export
- Seed: 2 users, 6 tickets (all statuses), 4 comments

### Changed

- Added `User.created_at` and `Ticket.updated_at` for audit/display (not in minimal brief but useful)

### Rejected

- UUID primary keys — integer autoincrement kept for simplicity

---

## Session: API contract and UI flow design (M4/M6 prep)

**Date:** 2026-07-10

### Prompt

Document API endpoints and frontend flows before/alongside backend implementation. Keep `api-contract.md` as source of truth.

### AI Response Summary

Wrote `api-contract.md` with request/response shapes, error codes, and auth requirements. Wrote `ui-flow.md` for login, list, create, detail, status, export flows. Updated `design-notes.md` with layered architecture.

### Accepted

- Unified error shape `{ error, message, details }`
- Status endpoint separate from general PATCH
- `invalid_status_transition` includes `current_status` and `requested_status`
- Frontend status buttons derived from allowed transitions only

### Changed

- Expanded contract as routes were added (users, auth/me, user CRUD in later milestones)

### Rejected

- GraphQL or tRPC — REST + OpenAPI sufficient for assessment
