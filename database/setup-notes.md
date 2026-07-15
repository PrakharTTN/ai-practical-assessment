# Database Setup Notes

## Database Choice

PostgreSQL 16 (Docker image `postgres:16-alpine` or local install 14+)

## Prerequisites

- PostgreSQL running locally **or** `docker compose up -d postgres`
- Python 3.11+ with backend dependencies installed

## Environment Variables

| Variable | Description | Local (native) | Docker backend |
|----------|-------------|----------------|----------------|
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql://ticket_user:changeme@localhost:5432/tickets_db` | `postgresql://ticket_user:changeme@postgres:5432/tickets_db` |

Copy `.env.example` to `src/backend/.env` for native runs, or repo-root `.env` for Docker Compose.

## Setup Steps

```bash
# From repo root
docker compose up -d postgres

# Wait for healthy
docker compose ps
```

### Option B — Local PostgreSQL

```bash
psql -U postgres -c "CREATE USER ticket_user WITH PASSWORD 'changeme';"
psql -U postgres -c "CREATE DATABASE tickets_db OWNER ticket_user;"
```

### 2. Run Migrations

```bash
cd src/backend
pip install -r requirements.txt

# Native: ensure DATABASE_URL uses localhost
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db

alembic upgrade head
```

Expected output: `Running upgrade  -> 001, Initial schema`

### 3. Seed Data

```bash
cd src/backend
python -m app.seed
```

Expected output: `Created 2 users, 6 tickets, 4 comments.`

Re-running seed is safe — it skips if users already exist.

### 4. Verify in psql

```bash
psql postgresql://ticket_user:changeme@localhost:5432/tickets_db -c "SELECT status, count(*) FROM tickets GROUP BY status;"
```

Expected: one ticket per status (`open`×2, `in_progress`, `resolved`, `closed`, `cancelled`).

### Full stack (Docker)

```bash
docker compose up --build
```

Backend entrypoint runs migrate + seed automatically on startup.

## Schema Overview

| Table | Rows (after seed) |
|-------|-------------------|
| users | 2 |
| tickets | 6 |
| comments | 4 |

Migrations: `src/backend/alembic/versions/001_initial_schema.py`

## Dev Seed Credentials

Default admin on first startup: `admin@admin.com` / `admin` — see [seed-data/README.md](./seed-data/README.md). Dev-only; not shown in the login UI.

Admins can create additional users via the Team page (`/users`) or `POST /api/users`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `connection refused` on localhost | Start postgres: `docker compose up -d postgres` |
| `database "tickets_db" does not exist` | Create DB (see Option B) or run full docker compose |
| `role "ticket_user" does not exist` | Create user or use docker postgres service |
| `type "user_role" already exists` | DB partially migrated; `docker compose down -v` for fresh volume |
| Alembic can't find module `app` | Run commands from `src/backend/` directory |
| Seed says "already exists" | Expected on re-run; use `docker compose down -v` to reset |
