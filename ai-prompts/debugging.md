# Debugging Prompts

## Session: Database migration and seed failures (M3)

**Date:** 2026-07-10

### Prompt

Review M3 database layer; run migrations and seed; fix any issues found.

### AI Response Summary

Identified missing PK autoincrement, duplicate enum creation in Alembic, and SQLAlchemy enum name vs value mismatch. Proposed targeted migration and model fixes.

### Accepted

- `autoincrement=True` on all PK columns
- `postgresql.ENUM(..., create_type=False)`
- `values_callable` on Enum columns

### Changed

- Reset DB with `alembic downgrade base && upgrade head` when migration already partially applied

### Rejected

- Switching to SQLite for local dev — assessment requires PostgreSQL

---

## Session: Port 5432 conflict and test suite (M5)

**Date:** 2026-07-15

### Prompt

Run thorough backend tests; provide test report.

### AI Response Summary

Tests failed on auth due to bcrypt/passlib version clash. Port 5432 conflict with host Postgres suggested temporary 5433 mapping.

### Accepted

- Pin `bcrypt>=4.0.0,<4.1.0`
- Revert to port 5432 after user stopped local Postgres

### Changed

- Brief 5433 experiment reverted for doc consistency

### Rejected

- Mocking database in tests — violates `testing-discipline.mdc`

---

## Session: Docker full-stack verification (M6)

**Date:** 2026-07-15

### Prompt

Unit test M6, then use docker-up-local skill to up backend, frontend, and DB.

### AI Response Summary

Followed `docker-up-local` skill: pre-flight checks, `docker compose up --build -d`, infrastructure curls, API smoke tests mirroring UI checklist.

### Accepted

- Detached Docker start with full rebuild on first run
- Document results in `test-results.md`

### Changed

- None — stack started successfully after prior port fix

### Rejected

- Skipping infrastructure verification when user explicitly requested docker-up-local workflow

---

## Session: Login UX and default admin (M6 polish)

**Date:** 2026-07-15

### Prompt

Remove seeded credentials from login page; default admin `admin@admin.com`; improve login styling.

### AI Response Summary

Updated seed constants, removed login hint text, styled login shell, documented credentials in `database/seed-data/README.md` only.

### Accepted

- Credentials documented off-UI
- `docker compose down -v` to verify fresh seed admin

### Changed

- Updated all test fixtures and docs from `admin@example.com` to `admin@admin.com`

### Rejected

- Displaying any dev password on the login page
