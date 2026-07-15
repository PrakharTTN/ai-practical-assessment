# Seed Data

Seed script: `src/backend/app/seed.py`

Runs automatically on first Docker startup (via `scripts/docker/backend-entrypoint.sh`) or manually with `python -m app.seed`. **Idempotent** — skips if any users already exist.

## Default admin account (first startup)

When the database is empty, seed creates a default administrator:

| Field | Value |
|-------|-------|
| Email | `admin@admin.com` |
| Password | `admin` |
| Role | `admin` |

Use this account to sign in after a fresh install. Credentials are **documented here only** — they are not shown on the login page.

> **Security:** Dev/assessment placeholders only. Change or remove before any real deployment.

## Additional seed user (sample data)

| Email | Password | Role |
|-------|----------|------|
| `agent@example.com` | `admin` | agent |

Used for assignee picker and sample tickets — not required for initial login.

## Sample data created

| Entity | Count | Notes |
|--------|-------|-------|
| Users | 2 | default admin + agent |
| Tickets | 6 | one per status (`open` has 2) |
| Comments | 4 | on open, in_progress, resolved, closed tickets |

## Run seed manually

```bash
cd src/backend
python -m app.seed
```

## Reset and re-seed

```bash
docker compose down -v          # Docker: wipe volume
cd src/backend && alembic downgrade base && alembic upgrade head
python -m app.seed
```

After reset, sign in with `admin@admin.com` / `admin`.
