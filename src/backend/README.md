# Backend

FastAPI application with SQLAlchemy, Alembic, and JWT authentication.

## Layout

```
app/
  main.py              # App entry, CORS, error handlers, health routes
  config.py            # Pydantic settings (DATABASE_URL, JWT, CORS)
  database.py          # SQLAlchemy engine and session
  deps.py              # get_current_user, require_admin
  exceptions.py        # AppError unified error type
  seed.py              # Idempotent seed script
  models/              # User, Ticket, Comment + enums
  schemas/             # Pydantic request/response models
  services/
    auth.py            # bcrypt + JWT encode/decode
    ticket_state_machine.py   # Single status enforcement point
  routers/
    auth.py            # POST /api/auth/login, GET /api/auth/me
    users.py           # GET/POST/PATCH /api/users (admin create/update)
    tickets.py         # CRUD, status, comments, CSV export
alembic/               # Migrations (001_initial_schema)
```

## Run locally

```bash
cd src/backend
source .venv/bin/activate
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

## Database

```bash
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db
alembic upgrade head
python -m app.seed
```

Default admin on first seed: `admin@admin.com` / `admin` — see [database/seed-data/README.md](../../database/seed-data/README.md).

Full setup: [database/setup-notes.md](../../database/setup-notes.md).

## Tests

From repo root: `pytest tests/backend -v` (45 tests). See [tests/README.md](../../tests/README.md).
