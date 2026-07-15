# Data Model

## Entity Relationship Overview

```
User 1──* Ticket (created_by)
User 1──* Ticket (assigned_to, optional)
User 1──* Comment
Ticket 1──* Comment
```

## User (`users`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, autoincrement | |
| name | varchar(100) | NOT NULL | |
| email | varchar(255) | UNIQUE, NOT NULL | indexed |
| role | `user_role` enum | NOT NULL | `agent`, `admin` |
| password_hash | varchar(255) | NOT NULL | bcrypt |
| created_at | timestamptz | NOT NULL, default now() | |

## Ticket (`tickets`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, autoincrement | |
| title | varchar(200) | NOT NULL | |
| description | text | NOT NULL | |
| priority | `ticket_priority` enum | NOT NULL, indexed | `low`, `medium`, `high` |
| status | `ticket_status` enum | NOT NULL, default `open`, indexed | state machine enforced in API |
| assigned_to_id | FK → users.id | nullable, indexed | ON DELETE SET NULL |
| created_by_id | FK → users.id | NOT NULL, indexed | ON DELETE RESTRICT |
| created_at | timestamptz | NOT NULL, default now() | |
| updated_at | timestamptz | NOT NULL, default now() | |

## Comment (`comments`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, autoincrement | |
| ticket_id | FK → tickets.id | NOT NULL, indexed | ON DELETE CASCADE |
| message | text | NOT NULL | |
| created_by_id | FK → users.id | NOT NULL | ON DELETE RESTRICT |
| created_at | timestamptz | NOT NULL, default now() | |

## Status State Machine

Canonical API/DB values: `open`, `in_progress`, `resolved`, `closed`, `cancelled`

```
open         → in_progress, cancelled
in_progress  → resolved, cancelled
resolved     → closed
closed       → (terminal)
cancelled    → (terminal)
```

## Indexes

| Table | Index | Purpose |
|-------|-------|---------|
| users | `ix_users_email` | login lookup |
| tickets | `ix_tickets_status` | filter by status |
| tickets | `ix_tickets_priority` | filter by priority |
| tickets | `ix_tickets_created_by_id` | CSV export scope |
| tickets | `ix_tickets_assigned_to_id` | assignee queries |
| comments | `ix_comments_ticket_id` | detail view |

Title search uses `ILIKE` on `title` column (no separate index for assessment scale).

## Migrations

Alembic migrations live in `src/backend/alembic/versions/`.
Initial migration: `001_initial_schema.py`

## Seed Data

Script: `src/backend/app/seed.py` — run via `python -m app.seed` or Docker entrypoint on empty DB.

| First startup | Value |
|---------------|-------|
| Default admin email | `admin@admin.com` |
| Default admin password | `admin` |
| Sample agent | `agent@example.com` / `admin` |
| Sample tickets | 6 (all statuses) |
| Sample comments | 4 |

See [database/seed-data/README.md](./database/seed-data/README.md) for full details.

## User Management API

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/api/users` | Any authenticated | List users (assignee picker) |
| POST | `/api/users` | Admin | Create user |
| PATCH | `/api/users/{id}` | Admin | Update user (optional password) |
| GET | `/api/auth/me` | Any authenticated | Current user profile |
