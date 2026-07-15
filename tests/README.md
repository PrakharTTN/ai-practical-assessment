# Tests

Test suites for the Support Ticket Management System.

## Backend (`tests/backend/`)

Integration tests against **real PostgreSQL** — no SQLite, no mocked database.

```
tests/
  backend/
    conftest.py                          # client, admin_headers, agent_headers
    helpers.py                           # create_ticket, ticket_in_status utilities
    test_health.py                       # GET /api/health smoke test
    integration/
      test_api_auth.py                   # login, 401 cases
      test_api_tickets.py                # CRUD, filter, validation
      test_api_export.py                 # CSV scoping
      test_api_users.py                  # user management, /api/auth/me
      test_ticket_status_transitions.py  # state machine (mandatory)
  requirements.txt                       # pytest, httpx
```

**Latest run:** 45 passed — see [test-results.md](../test-results.md).

```bash
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db
docker compose up -d postgres
pytest tests/backend -v
```

Requires PostgreSQL on port **5432** (Docker `tickets-postgres` or local install).

## Frontend (`src/frontend/`)

Component tests with Vitest + React Testing Library (14 tests).

```bash
cd src/frontend
npm test
```

See [test-strategy.md](../test-strategy.md) for scope and coverage notes.
