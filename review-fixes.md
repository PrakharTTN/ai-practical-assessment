# Review Fixes

## Fix 1 — Migration PK autoincrement

### Finding

`001_initial_schema.py` — PK columns lacked `autoincrement=True`; seed inserts would fail on PostgreSQL.

### Change Made

Added `autoincrement=True` to `users.id`, `tickets.id`, `comments.id`.

### Reference

`src/backend/alembic/versions/001_initial_schema.py`

---

## Fix 2 — Enum duplicate creation on migrate

### Finding

Alembic migration attempted to create PostgreSQL enum types twice.

### Change Made

Switched to `postgresql.ENUM(..., create_type=False)` in migration.

### Reference

`src/backend/alembic/versions/001_initial_schema.py`

---

## Fix 3 — SQLAlchemy enum values

### Finding

Seed inserted `ADMIN` instead of `admin` for role/status enums.

### Change Made

Added `values_callable` on SQLAlchemy `Enum` columns.

### Reference

`src/backend/app/models/user.py`, `src/backend/app/models/ticket.py`

---

## Fix 4 — passlib / bcrypt compatibility

### Finding

`bcrypt` 4.1+ broke passlib password hashing in tests.

### Change Made

Pinned `bcrypt>=4.0.0,<4.1.0` in `requirements.txt`.

---

## Fix 5 — Default admin and login UX

### Finding

Login page displayed seeded credentials; default admin used `admin@example.com`.

### Change Made

- Seed default admin: `admin@admin.com` / `admin`
- Removed credential hint from login UI
- Documented credentials in `database/seed-data/README.md` only
- Professional login page styling

### Reference

`src/backend/app/seed.py`, `src/frontend/src/pages/LoginPage.tsx`

---

## Fix 6 — User onboarding gap

### Finding

No way for admin to add users after initial seed.

### Change Made

- `POST /api/users` and `PATCH /api/users/{id}` (admin only)
- `GET /api/auth/me` for session profile
- Team page at `/users` with create and edit flows
- 13 integration tests in `test_api_users.py`

### Reference

`src/backend/app/routers/users.py`, `src/frontend/src/pages/UsersPage.tsx`

---

## Fix 7 — Post-login UI polish

### Finding

Authenticated pages looked basic compared to login page.

### Change Made

Redesigned app shell: sticky header, nav pills, card panels, data tables, role badges, responsive grids.

### Reference

`src/frontend/src/components/Layout.tsx`, `src/frontend/src/styles.css`, ticket pages
