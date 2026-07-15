# Code Review Notes

## AI-Assisted Review Summary

**Date:** 2026-07-10  
**Scope:** M3 — database layer (models, Alembic migration, seed script, setup docs)  
**Method:** `review-ticket-feature` style pass against `requirements-analysis.md`, `data-model.md`, and `state-machine.mdc`

Overall: solid foundation for M4. One critical migration issue found and fixed (see below).

## My Review Observations

### Critical

- **`001_initial_schema.py` — PK columns lacked autoincrement**  
  `users.id`, `tickets.id`, and `comments.id` were plain `Integer` PKs without `autoincrement=True`. On PostgreSQL this prevents auto-generated IDs; `python -m app.seed` would fail on insert.  
  **Fixed:** added `autoincrement=True` to all three `id` columns.

### Suggestions (deferred to M4 or later)

- **`updated_at` on tickets** — ORM `onupdate=func.now()` does not fire on all update paths. M4 update service should set `updated_at` explicitly.
- **Seed idempotency** — skips entirely if any user exists; partial failed seed could leave empty tickets. Acceptable for assessment; improve if re-seeding becomes common.
- **`db.query()` in seed** — legacy SQLAlchemy 1.x style; migrate to `select()` when touching seed again.
- **Duplicate index on `users.email`** — model `unique=True, index=True` plus migration `UniqueConstraint` + `ix_users_email`. Harmless redundancy.

### Verified alignment

- Enum values match state machine rule (`open`, `in_progress`, `resolved`, `closed`, `cancelled`)
- FK delete rules appropriate (`SET NULL` assignee, `RESTRICT` creator, `CASCADE` comments)
- Indexes on `status`, `priority`, `created_by_id` support filter/export
- Seed covers all statuses and splits `created_by` across admin + agent for CSV testing

### Not runtime-verified

Migrate + seed not executed in review environment (port 5432 conflict). Run locally before M4:

```bash
cd src/backend
alembic upgrade head   # or downgrade base && upgrade head if 001 already applied
python -m app.seed
```

---

## M4–M6 Review Summary

**Date:** 2026-07-15  
**Scope:** Backend API, integration tests, frontend UI, user management, Docker stack  
**Method:** Implementation + test runs + manual Docker/browser verification

### Verified

- State machine enforced only in `ticket_state_machine.py`; 45 integration tests pass on real PostgreSQL
- Status not updatable via general PATCH (tested)
- JWT auth on all protected routes; `created_by` from token
- Frontend `getAllowedTransitions` matches backend rules
- Docker full stack starts; migrate + seed on first run
- Admin user management (create/edit) with role-based 403 for agents
- Login UI professional; no credentials on page; default admin documented separately
- Post-login app shell styling consistent across ticket and team pages

### Enhancements beyond original Core scope

| Addition | Rationale |
|----------|-----------|
| `GET /api/auth/me` | Session restore + role-based nav without decoding JWT client-side |
| Admin user CRUD (create + edit) | User onboarding requirement; admin-only via `require_admin` |
| Vitest component tests | M6 test coverage without E2E framework |
| Default admin `admin@admin.com` | Clear first-login path; credentials in docs only |

### Deferred / not implemented

- Delete user endpoint
- Role-based ticket transition restrictions
- E2E Playwright/Cypress suite
- Optimistic locking on concurrent status updates

## Changes Made After Review

| Finding | Change | File |
|---------|--------|------|
| Missing PK autoincrement | Added `autoincrement=True` to `id` on `users`, `tickets`, `comments` | `src/backend/alembic/versions/001_initial_schema.py` |
| Duplicate enum creation on migrate | Switched to `postgresql.ENUM(..., create_type=False)` so explicit `.create()` is not repeated on `create_table` | `src/backend/alembic/versions/001_initial_schema.py` |
| Seed enum insert used names not values | Added `values_callable` to SQLAlchemy `Enum` columns so DB gets `admin` not `ADMIN` | `app/models/user.py`, `app/models/ticket.py` |
| passlib + bcrypt 4.1 incompatibility | Pinned `bcrypt>=4.0.0,<4.1.0` in requirements | `requirements.txt` |
| Login showed seeded credentials | Default admin `admin@admin.com`; docs only; styled login page | `seed.py`, `LoginPage.tsx`, `seed-data/README.md` |
| No user onboarding UI | Admin Team page + `POST`/`PATCH /api/users` | `UsersPage.tsx`, `routers/users.py` |
| Basic post-login UI | App shell redesign (header, panels, tables) | `Layout.tsx`, `styles.css`, ticket pages |

**Note:** If `001` was already applied without autoincrement, reset and re-migrate:

```bash
alembic downgrade base && alembic upgrade head
# or: docker compose down -v && docker compose up --build
```

## Suggestions Rejected (and why)

| Suggestion | Reason |
|--------------|--------|
| Enforce state machine in DB (CHECK/trigger) | Assessment expects app-layer enforcement + integration tests; DB triggers add complexity without benefit at this scale |
| Switch PKs to UUID | Integer autoincrement is simpler; `data-model.md` allows either |
| Add `User.created_at` to assessment spec retroactively | Already shipped; useful audit field, no downside |
| Fix duplicate email index now | Cosmetic; no functional impact |

---

## M7 Final Submission Review

**Date:** 2026-07-15  
**Method:** `review-ticket-feature` skill — acceptance criteria walkthrough

### Acceptance criteria

| Area | Status |
|------|--------|
| Core tickets | Pass — UI + API + tests |
| State machine | Pass — 5 valid + 7 invalid integration tests |
| CSV export | Pass — scoped export tested |
| Persistence | Pass — Docker volume + migrate/seed |
| Validation & errors | Pass — 422/400/401 shapes tested |
| Auth | Pass — JWT, bcrypt, protected routes |
| User management | Pass — admin create/edit, agent 403 |
| Testing | Pass — 45 backend + 14 frontend |
| Documentation | Pass — README, contract, setup, prompts |
| Stretch | Partial — Docker + Swagger + admin RBAC for users |

### Submission readiness

- Mentor can clone → `docker compose up --build` → login → exercise all flows
- `pytest` and `npm test` documented and passing
- AI workflow traceable: `tool-workflow.md` → `ai-prompts/` (15 sessions) → `final-ai-usage-summary.md`
- Known gaps documented honestly in `pr-description.md` and `reflection.md`

### Remaining candidate action

- Fill name/role in `candidate-info.md` before hand-in
