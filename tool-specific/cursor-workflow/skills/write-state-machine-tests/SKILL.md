---
name: write-state-machine-tests
description: >-
  Writes PostgreSQL integration tests for ticket status transitions in the
  Support Ticket Management System. Use when implementing status changes,
  ticket_state_machine service, or mandatory assessment transition tests.
---

# Write State Machine Tests

## When to Use

- Implementing `PATCH /api/tickets/{id}/status`
- Creating or fixing `ticket_state_machine` service
- Assessment requires proof that valid transitions succeed and invalid ones fail
- `testing-discipline.mdc` applies to current work

## Steps

1. **Confirm enforcement point** — read `src/backend/app/services/ticket_state_machine.py` (or create it); tests must hit the API, not call helpers in isolation only.

2. **Test setup** — in `tests/backend/integration/test_ticket_status_transitions.py`:
   - Use pytest fixtures: test DB session, `TestClient`, seeded user, auth headers
   - `DATABASE_URL` must point to PostgreSQL test database
   - Roll back or truncate between tests

3. **Write valid transition tests** — parametrized or individual:
   ```
   open → in_progress
   open → cancelled
   in_progress → resolved
   in_progress → cancelled
   resolved → closed
   ```
   Assert: HTTP 200, response `status` equals target.

4. **Write invalid transition tests** — at minimum:
   ```
   open → resolved, open → closed, in_progress → open,
   resolved → in_progress, closed → open, cancelled → in_progress
   ```
   Assert: HTTP 400 or 422, body `error == "invalid_status_transition"`, status unchanged on re-fetch.

5. **Run tests** — `pytest tests/backend/integration/test_ticket_status_transitions.py -v`

6. **Record results** — append pass/fail summary to `test-results.md`.

## Expected Output

- `tests/backend/integration/test_ticket_status_transitions.py` with real-DB tests
- All valid transitions green; all invalid transitions rejected with correct error code
- Terminal test run output summarized for the user
- `test-results.md` updated with date, command, and counts

## Files Updated

| File | Action |
|------|--------|
| `tests/backend/integration/test_ticket_status_transitions.py` | Create/update tests |
| `tests/backend/conftest.py` | If fixtures needed |
| `test-results.md` | Record run results |
| `test-strategy.md` | Check off state-machine cases |
| `ai-prompts/testing.md` | Optional — capture session |
