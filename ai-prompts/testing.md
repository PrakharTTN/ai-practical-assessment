# Testing Prompts

## Session: M5 — Backend integration tests

**Date:** 2026-07-15

### Prompt

Run thorough backend tests on real PostgreSQL. Mandatory state machine tests. Document in `test-results.md`.

### AI Response Summary

Built `tests/backend/integration/*` — auth, tickets, export, status transitions (12 cases). Configured `pytest.ini` pythonpath. Fixed bcrypt pin for passlib compatibility. **32 tests passed** on Docker Postgres.

### Accepted

- Real PostgreSQL only — no SQLite, no mocked DB
- Parametrized valid + invalid transition tests
- Fixtures: `admin_headers`, `agent_headers`, `client`
- Results recorded in `test-results.md`

### Changed

- Expanded from health-only smoke to full integration suite

### Rejected

- Mocking `get_db` or ticket service in integration tests

---

## Session: M6 — Frontend tests and Docker verification

**Date:** 2026-07-15

### Prompt

Unit test M6 first, then use docker-up-local skill to up backend, frontend, and DB for verification.

### AI Response Summary

Added Vitest + RTL (14 tests): status utils, ApiError/field errors, ProtectedRoute, ErrorBanner. Ran `docker compose up --build -d`, infrastructure curls, API smoke tests. User later verified team management and styling manually.

### Accepted

- Vitest in `src/frontend` with `npm test`
- docker-up-local checklist (health, frontend 200, login, CRUD smoke)
- Extended backend suite to 45 tests after user management API

### Changed

- None on Docker — stack started successfully after port 5432 fix

### Rejected

- Skipping Docker verification when user explicitly requested skill workflow
