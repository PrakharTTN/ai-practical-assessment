---
name: debug-backend-issue
description: >-
  Systematically debugs FastAPI backend issues in the Support Ticket Management
  System. Use when API returns unexpected errors, state transitions fail, DB
  persistence breaks, or auth/JWT problems occur.
---

# Debug Backend Issue

## When to Use

- API returns 500, unexpected 4xx, or wrong response shape
- Status transition behaves incorrectly
- Data not persisting across restart
- JWT auth failing on ticket routes
- pytest integration tests failing against PostgreSQL

## Steps

1. **Reproduce** — capture exact request: method, path, headers, body, and response status + JSON.

2. **Classify** — map to domain area:
   - State machine → check `ticket_state_machine` + `state-machine.mdc`
   - Validation → Pydantic schemas + `api-error-shape.mdc`
   - Auth → JWT middleware, token expiry, `createdBy` assignment
   - DB → migrations, connection string, session commit/rollback

3. **Trace** — follow call chain: `routers/` → `services/` → `models/` → DB. Read logs; do not guess.

4. **Isolate** — write or run a minimal failing pytest case if none exists; prefer integration test over manual curl.

5. **Fix** — smallest correct change; do not bypass state machine or validation to "make it work".

6. **Verify** — run affected tests + state-machine suite if status-related.

7. **Document** — add entry to `debugging-notes.md` with problem, investigation, AI role, validation, fix.

## Expected Output

- Root cause stated in plain language
- Fix applied (or clear blocker identified)
- Failing test now passes (or new regression test added)
- `debugging-notes.md` entry with dated issue section
- If error shape changed, `api-contract.md` synced

## Files Updated

| File | Action |
|------|--------|
| `src/backend/**` | Bug fix |
| `tests/**` | Regression test if applicable |
| `debugging-notes.md` | Issue record |
| `ai-prompts/debugging.md` | Prompt session capture |
| `api-contract.md` | If error responses changed |
| `test-results.md` | If test run performed |
