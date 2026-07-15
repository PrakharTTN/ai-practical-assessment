# Test Strategy

## Test Scope

Integration tests against **real PostgreSQL** via FastAPI `TestClient`. No SQLite, no mocked database layer.

| Layer | Location | Status |
|-------|----------|--------|
| Smoke | `tests/backend/test_health.py` | Done |
| Auth | `tests/backend/integration/test_api_auth.py` | Done |
| Tickets CRUD + filter | `tests/backend/integration/test_api_tickets.py` | Done |
| CSV export | `tests/backend/integration/test_api_export.py` | Done |
| State machine | `tests/backend/integration/test_ticket_status_transitions.py` | Done |
| User management | `tests/backend/integration/test_api_users.py` | Done |
| Frontend component | `src/frontend/src/**/*.test.ts(x)` (Vitest + RTL) | Done |

## Unit Tests

State machine logic is covered via API integration tests (hits `ticket_state_machine.py` through `PATCH /api/tickets/{id}/status`). Dedicated unit tests for the service module are optional.

## Component Tests

Run: `cd src/frontend && npm test`

- [x] `getAllowedTransitions` mirrors backend state machine
- [x] `getFieldErrors` maps API validation details
- [x] JWT token sessionStorage helpers
- [x] `ProtectedRoute` redirects unauthenticated users; respects loading state
- [x] `ErrorBanner` shows/hides alert message

## API / Integration Tests

Run: `pytest tests/backend -v` (requires PostgreSQL on port 5432)

### State Machine Tests

- [x] Valid transition: Open → In Progress
- [x] Valid transition: Open → Cancelled
- [x] Valid transition: In Progress → Resolved
- [x] Valid transition: In Progress → Cancelled
- [x] Valid transition: Resolved → Closed
- [x] Invalid transitions rejected with `invalid_status_transition`

### User Management Tests

- [x] Admin can create user; new user can log in
- [x] Admin can update user fields and password
- [x] Agent forbidden from create/update (403)
- [x] Duplicate email on create/update (409)
- [x] `GET /api/auth/me` returns profile for session restore

## Edge Case Tests

- [x] Missing title on create → 422
- [x] Empty comment → 422
- [x] Unauthenticated access → 401
- [x] Invalid JWT → 401
- [x] Ticket not found → 404
- [x] CSV export scoped to `created_by`
- [x] Same-status transition rejected

## Manual Verification

- [x] Full Docker stack (`docker compose up --build`)
- [x] Browser walkthrough: login, tickets, export, team management
- [x] User-confirmed: create/edit users and UI styling

## Tests Not Covered (and why)

| Area | Reason |
|------|--------|
| E2E browser automation | Out of scope; manual + component tests sufficient |
| Load/performance | Out of assessment scope |
| Role-based ticket write restrictions | Not required; all authenticated users can edit tickets |
| Ticket/comment delete | Out of Core scope |
| Concurrent status updates | Documented edge case; no optimistic locking in Core |
| Delete user | Not implemented |
