# Support Ticket Management System

AI-assisted full-stack assessment project for managing support tickets.

## Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Frontend | React + Vite + TypeScript |
| Backend  | FastAPI                 |
| Database | PostgreSQL              |
| Auth     | JWT                     |

## Project Structure

```
src/
  frontend/   # React application
  backend/    # FastAPI application
tests/        # Test suites
database/     # Schema, migrations, and seed data
```

## Prerequisites

- Node.js (v18+)
- Python (v3.11+)
- PostgreSQL (v14+)
- Docker (optional, for containerized database)

## Local Setup

Copy environment placeholders before starting:

```bash
cp .env.example .env
```

### 1. Database

```bash
docker compose up -d postgres
# or see database/setup-notes.md for native PostgreSQL
cd src/backend
alembic upgrade head
python -m app.seed
```

### 2. Backend

```bash
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: http://localhost:8000/api/health · API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd src/frontend
npm install
export VITE_API_URL=http://localhost:8000
npm run dev
```

Verify: http://localhost:5173 — sign in with the default admin from [database/seed-data/README.md](./database/seed-data/README.md) (`admin@admin.com` / `admin` on first startup)

## Run with Docker

Stretch/local verification — not production deployment.

### Prerequisites

- Docker Engine + Docker Compose v2

### Quick start

```bash
cp .env.example .env
chmod +x scripts/docker/*.sh
docker compose up --build
```

| Service  | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:8000 |
| API health | http://localhost:8000/api/health |

On first startup the backend entrypoint waits for PostgreSQL, runs migrations (`alembic upgrade head`), then seeds (`python -m app.seed`) when the database is empty. A default admin user is created (`admin@admin.com` / `admin`) — see [database/seed-data/README.md](./database/seed-data/README.md). Credentials are documented only; they are not displayed on the login page.

### Rebuild after dependency changes

```bash
docker compose up --build -d
```

Source code is volume-mounted — backend (`--reload`) and Vite pick up most code edits without rebuild. Rebuild when `requirements.txt` or `package.json` changes.

### Stop

```bash
docker compose stop          # stop containers, keep data
docker compose down          # remove containers, keep postgres volume
docker compose down -v       # remove containers + database volume (fresh DB)
```

### Troubleshooting

```bash
docker compose ps
docker compose logs backend --tail=100
```

Use the `docker-up-local` skill in Cursor for guided startup verification and failure debugging.

## Running Tests

```bash
# Backend (requires PostgreSQL on 5432)
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db
docker compose up -d postgres
pip install -r tests/requirements.txt
pytest tests/backend -v

# Frontend
cd src/frontend && npm test
```

See [test-results.md](./test-results.md) for latest run (**45** backend + **14** frontend tests passed).

## Features

- JWT authentication with session restore (`/api/auth/me`)
- Ticket CRUD, comments, status state machine, CSV export
- Search/filter on ticket list
- Admin team management: create and edit users at `/users`
- Docker Compose full stack for local verification

## Environment Variables

Copy `.env.example` to `.env` and adjust placeholders locally. Never commit `.env`.

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection (use host `postgres` in Docker, `localhost` when running backend natively) |
| `JWT_SECRET` | Signing key for auth tokens (placeholder in example) |
| `VITE_API_URL` | Frontend → backend URL (`http://localhost:8000` for browser) |

## Documentation

| Artifact | Description |
|----------|-------------|
| [requirements-analysis.md](./requirements-analysis.md) | Requirement breakdown |
| [acceptance-criteria.md](./acceptance-criteria.md) | Acceptance criteria checklist |
| [implementation-plan.md](./implementation-plan.md) | Implementation plan and milestones |
| [design-notes.md](./design-notes.md) | Architecture and design decisions |
| [api-contract.md](./api-contract.md) | API endpoint specifications |
| [test-strategy.md](./test-strategy.md) | Testing approach |
| [ui-flow.md](./ui-flow.md) | Frontend navigation and user flows |
| [test-results.md](./test-results.md) | Latest test and verification results |
| [debugging-notes.md](./debugging-notes.md) | Issues investigated and fixes applied |
| [reflection.md](./reflection.md) | AI-assisted development reflection |
| [final-ai-usage-summary.md](./final-ai-usage-summary.md) | Curated AI session summary |
| [database/seed-data/README.md](./database/seed-data/README.md) | Default admin and seed data |

## Submission Package (M7)

| Artifact | Description |
|----------|-------------|
| [candidate-info.md](./candidate-info.md) | Submission index — fill name/role before hand-in |
| [pr-description.md](./pr-description.md) | PR-style feature summary |
| [tool-workflow.md](./tool-workflow.md) | How Cursor was used across phases |
| [ai-prompts/](./ai-prompts/) | 15 curated prompt sessions by phase |
| [code-review-notes.md](./code-review-notes.md) | Review findings |
| [review-fixes.md](./review-fixes.md) | Fixes applied after review |

## License

Assessment project — not for production use.
