# Debugging Notes

Chronological record of non-trivial issues encountered during development. See also [review-fixes.md](./review-fixes.md) for the same fixes in review format.

---

## Issue: Alembic seed fails — null value in column `id`

**Date:** 2026-07-10 (M3)

### Problem

Running `python -m app.seed` after `alembic upgrade head` failed with a PostgreSQL error: primary key `id` was not auto-generated on insert.

### How I Investigated

- Read stack trace pointing at `users` insert
- Inspected `001_initial_schema.py` — `id` columns defined as `Integer` PK without `autoincrement=True`
- Compared with SQLAlchemy model definitions

### How AI Helped

- Code review (`review-ticket-feature` style) flagged missing autoincrement on all three tables
- Suggested `autoincrement=True` on `users.id`, `tickets.id`, `comments.id`

### What I Validated

- `alembic downgrade base && alembic upgrade head` on fresh volume
- `python -m app.seed` completed: 2 users, 6 tickets, 4 comments

### Final Fix

Added `autoincrement=True` to PK columns in `src/backend/alembic/versions/001_initial_schema.py`.

---

## Issue: Migration fails — enum type already exists

**Date:** 2026-07-10 (M3)

### Problem

`alembic upgrade head` failed on second run or after partial apply with `type "user_role" already exists` (or similar for ticket enums).

### How I Investigated

- Read Alembic migration — enum types created explicitly, then referenced again in `create_table` with default SQLAlchemy enum behaviour creating types a second time
- Checked PostgreSQL `\dT+` for duplicate type definitions

### How AI Helped

- Suggested `postgresql.ENUM(..., create_type=False)` when enum is already created via `.create()` earlier in the migration

### What I Validated

- Clean `docker compose down -v` + `alembic upgrade head` succeeds
- Re-run migrate on existing DB does not error

### Final Fix

Use `postgresql.ENUM(..., create_type=False)` for enum columns in `001_initial_schema.py`.

---

## Issue: Seed inserts wrong enum values (`ADMIN` vs `admin`)

**Date:** 2026-07-10 (M3)

### Problem

Seed or ORM inserts sent Python enum **names** (`ADMIN`) instead of **values** (`admin`), causing PostgreSQL enum mismatch errors.

### How I Investigated

- Compared DB enum definition (`admin`, `agent`) with values in failed INSERT
- Traced SQLAlchemy `Enum` column configuration on `User.role` and `Ticket.status`

### How AI Helped

- Recommended `values_callable=lambda x: [e.value for e in x]` on SQLAlchemy `Enum` columns

### What I Validated

- Seed completes; `SELECT role FROM users` returns `admin` / `agent` lowercase
- Ticket statuses stored as `open`, `in_progress`, etc.

### Final Fix

Added `values_callable` to enum columns in `app/models/user.py` and `app/models/ticket.py`.

---

## Issue: pytest auth tests fail — passlib / bcrypt incompatibility

**Date:** 2026-07-15 (M5)

### Problem

Login integration tests failed during password verify/hash with errors from passlib when using `bcrypt` 4.1+.

### How I Investigated

- Ran `pytest tests/backend/integration/test_api_auth.py -v`
- Read passlib/bcrypt release notes — known breakage with bcrypt 4.1

### How AI Helped

- Identified version pin as smallest fix: `bcrypt>=4.0.0,<4.1.0` in `requirements.txt`

### What I Validated

- Full `pytest tests/backend` — 32/32 passed at the time
- Manual login via API still works

### Final Fix

Pinned `bcrypt` in `src/backend/requirements.txt`.

---

## Issue: Port 5432 already in use

**Date:** 2026-07-15 (M4/M5)

### Problem

Docker Postgres or local `pytest` could not bind to port **5432** — conflict with a system PostgreSQL instance already running on the host.

### How I Investigated

```bash
docker compose ps
ss -tlnp | grep 5432
docker compose logs postgres --tail=50
```

Temporarily mapped Docker Postgres to **5433** in `docker-compose.yml` and config files.

### How AI Helped

- `docker-up-local` skill symptom table: "postgres unhealthy — Port 5432 in use"
- Suggested either stop host Postgres or change port mapping

### What I Validated

- User stopped local PostgreSQL service
- Reverted all configs to port **5432** for consistency with assessment docs
- `docker compose up -d postgres` + `pytest` both work on 5432

### Final Fix

Stop host Postgres (preferred); keep `POSTGRES_PORT=5432` in `docker-compose.yml`. Documented in `test-results.md` and `ai-prompts/implementation.md`.

---

## Issue: Frontend ticket detail missing nested user fields

**Date:** 2026-07-15 (M6)

### Problem

API returned ticket JSON with nested `creator` / `assignee` / `author` from SQLAlchemy relationships, but Pydantic response models expected `created_by` / `assigned_to`. Frontend received incomplete or validation-failed responses.

### How I Investigated

- Compared network response shape in browser devtools with `types/api.ts`
- Read `TicketOut` schema and model `relationship()` back_populates names

### How AI Helped

- Suggested Pydantic v2 `validation_alias` on output fields to accept ORM attribute names while serializing API names

### What I Validated

- Ticket list and detail load in UI
- `created_by.name` and `assigned_to` display correctly
- `npm run build` passes

### Final Fix

Added `Field(validation_alias="creator")` / `"assignee"` / `"author"` in `src/backend/app/schemas/ticket.py`.

---

## Issue: Docker full-stack first build slow / frontend deps in image

**Date:** 2026-07-15 (M6 verification)

### Problem

First `docker compose up --build` took several minutes; frontend image runs `npm install` on build. Not a failure, but worth noting for onboarding.

### How I Investigated

```bash
docker compose up --build -d
docker compose ps
curl -s http://localhost:8000/api/health
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173
```

### How AI Helped

- `docker-up-local` skill: use `--build` on first start or after `package.json` / `requirements.txt` changes; volume mount picks up code edits without rebuild

### What I Validated

- All three containers running (postgres healthy, backend, frontend)
- Health 200, frontend 200
- Backend entrypoint: migrate → seed → uvicorn
- API smoke: login, list, create, invalid transition, export — all pass

### Final Fix

No code change required. Documented expected first-build time and rebuild triggers in README / `docker-up-local` skill usage.

---

## Issue: Login page exposed dev credentials

**Date:** 2026-07-15 (M6 polish)

### Problem

Login UI displayed text like "Use seeded credentials (admin@example.com / password123)" — poor security UX for anything beyond local dev.

### How I Investigated

- User feedback during manual verification
- Grep for `password123` and `admin@example` in frontend

### How AI Helped

- Removed hint from `LoginPage.tsx`
- Changed default seed admin to `admin@admin.com` / `admin`
- Documented credentials only in `database/seed-data/README.md`

### What I Validated

- Login page shows no credentials
- Fresh `docker compose down -v && up --build` seeds new admin
- User can sign in with documented default admin

### Final Fix

`src/backend/app/seed.py`, `LoginPage.tsx`, seed/README docs. See [review-fixes.md](./review-fixes.md) Fix 5.

---

## Summary

| # | Area | Symptom | Fix |
|---|------|---------|-----|
| 1 | Migration | Seed PK insert fails | `autoincrement=True` |
| 2 | Migration | Enum already exists | `create_type=False` |
| 3 | ORM/seed | Wrong enum strings | `values_callable` |
| 4 | Tests | passlib/bcrypt error | Pin bcrypt `<4.1` |
| 5 | Docker | Port 5432 conflict | Stop host Postgres; keep 5432 |
| 6 | API/UI | Nested user field mismatch | Pydantic `validation_alias` |
| 7 | Docker | Slow first build | Expected; `--build` when deps change |
| 8 | UX | Credentials on login page | Remove hint; document in seed README |

No unresolved blocking issues at M6 completion.
