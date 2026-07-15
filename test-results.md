# Test Results

## Summary

| Field | Value |
|-------|-------|
| **Date** | 2026-07-15 |
| **Environment** | Linux, Python 3.12.3, PostgreSQL 16 (Docker `tickets-postgres` on port **5432**) |
| **Database** | `postgresql://ticket_user:***@localhost:5432/tickets_db` (real PostgreSQL, not mocked) |
| **Backend outcome** | **45 passed**, 0 failed, 0 skipped |
| **Frontend outcome** | **14 passed**, 0 failed |

## Commands

```bash
# Backend (requires PostgreSQL on 5432)
cd /home/prakhar/Desktop/ai-practical-assessment
export DATABASE_URL=postgresql://ticket_user:changeme@localhost:5432/tickets_db
docker compose up -d postgres
src/backend/.venv/bin/pytest tests/backend -v

# Frontend
cd src/frontend && npm test
```

## Backend Results by Suite

| Suite | Tests | Passed | Failed |
|-------|-------|--------|--------|
| `test_health.py` | 1 | 1 | 0 |
| `integration/test_api_auth.py` | 5 | 5 | 0 |
| `integration/test_api_export.py` | 3 | 3 | 0 |
| `integration/test_api_tickets.py` | 11 | 11 | 0 |
| `integration/test_api_users.py` | 13 | 13 | 0 |
| `integration/test_ticket_status_transitions.py` | 12 | 12 | 0 |
| **Total** | **45** | **45** | **0** |

## User Management Tests (`test_api_users.py`)

| Test | Result |
|------|--------|
| List users requires auth | PASS |
| List users as authenticated user | PASS |
| `GET /api/auth/me` returns current user | PASS |
| `GET /api/auth/me` requires auth | PASS |
| Admin can create user + login as new user | PASS |
| Agent cannot create user (403) | PASS |
| Duplicate email on create (409) | PASS |
| Create validation (422) | PASS |
| Admin can update name/role | PASS |
| Admin can update password | PASS |
| Agent cannot update user (403) | PASS |
| Update non-existent user (404) | PASS |
| Duplicate email on update (409) | PASS |

## State Machine Integration Tests (mandatory)

### Valid transitions — all pass

| From | To | Result |
|------|-----|--------|
| `open` | `in_progress` | PASS |
| `open` | `cancelled` | PASS |
| `in_progress` | `resolved` | PASS |
| `in_progress` | `cancelled` | PASS |
| `resolved` | `closed` | PASS |

### Invalid transitions — all rejected with `invalid_status_transition`

| From | To | HTTP | `error` code | Status unchanged |
|------|-----|------|--------------|------------------|
| `open` | `resolved` | 400 | `invalid_status_transition` | PASS |
| `open` | `closed` | 400 | `invalid_status_transition` | PASS |
| `in_progress` | `open` | 400 | `invalid_status_transition` | PASS |
| `resolved` | `in_progress` | 400 | `invalid_status_transition` | PASS |
| `closed` | `open` | 400 | `invalid_status_transition` | PASS |
| `cancelled` | `in_progress` | 400 | `invalid_status_transition` | PASS |
| `open` | `open` (same-status) | 400 | `invalid_status_transition` | PASS |

## Auth & Security Tests

| Test | Result |
|------|--------|
| Login with valid credentials (`admin@admin.com`) | PASS |
| Login with invalid password → 401 | PASS |
| Login with unknown email → 401 | PASS |
| Protected route without token → 401 | PASS |
| Protected route with invalid token → 401 | PASS |
| CSV export without auth → 401 | PASS |

## Ticket API Tests

| Test | Result |
|------|--------|
| List tickets (authenticated) | PASS |
| Create ticket — `created_by` from JWT | PASS |
| Create ticket — missing title → 422 | PASS |
| Get ticket detail with comments | PASS |
| Get non-existent ticket → 404 | PASS |
| Update title, priority, assignee | PASS |
| Status not changed via PATCH update | PASS |
| Add comment | PASS |
| Empty comment → 422 | PASS |
| Filter by status | PASS |
| Search by title substring | PASS |

## CSV Export Tests

| Test | Result |
|------|--------|
| Export contains only self-created tickets | PASS |
| Export requires authentication | PASS |

## Frontend Unit Tests (Vitest + RTL)

| File | Tests | Focus |
|------|-------|-------|
| `src/utils/status.test.ts` | 7 | Allowed transitions, formatting |
| `src/api/client.test.ts` | 3 | Field errors, JWT storage |
| `src/components/ProtectedRoute.test.tsx` | 2 | Auth redirect, loading gate |
| `src/components/ErrorBanner.test.tsx` | 2 | Error display |
| **Total** | **14** | |

## Manual Verification (Docker + browser)

**Command:** `docker compose up --build -d`

| Check | Result |
|-------|--------|
| All containers running | PASS |
| Health endpoint | PASS |
| Frontend HTTP 200 | PASS |
| Login page — no credentials displayed | PASS |
| Login as default admin | PASS |
| Ticket list, create, detail, status, comments | PASS |
| CSV export | PASS |
| Team page — create user | PASS |
| Team page — edit user | PASS |
| Professional UI styling (login + app shell) | PASS (user verified) |

### URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

**Default admin:** `admin@admin.com` / `admin` — see `database/seed-data/README.md`

## Infrastructure

| Check | Result |
|-------|-------|
| PostgreSQL on port 5432 | PASS |
| Seed data on first startup | PASS |
| Health endpoint `/api/health` | PASS |
| Data persists across container restart (volume) | PASS |

## Warnings (non-blocking)

- `StarletteDeprecationWarning`: TestClient httpx deprecation — cosmetic
- `DeprecationWarning`: passlib `crypt` module — known with Python 3.12

## Failures and Resolutions

No failures in latest runs.

## Assessment Criteria Met

- [x] Integration tests use real PostgreSQL
- [x] All five valid state transitions tested
- [x] Seven invalid transitions tested with `invalid_status_transition`
- [x] Auth, validation, export, search/filter, user management covered
- [x] Frontend component tests for critical UI logic
- [x] Manual Docker walkthrough verified by user
- [x] Results documented in this file
