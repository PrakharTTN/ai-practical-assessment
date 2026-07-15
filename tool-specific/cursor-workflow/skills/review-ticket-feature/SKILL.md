---
name: review-ticket-feature
description: >-
  Reviews a ticket-system feature (CRUD, status, comments, auth, export, search)
  for correctness against acceptance criteria. Use when completing a feature,
  before PR, or when user asks for code review on ticket functionality.
---

# Review Ticket Feature

## When to Use

- After implementing a ticket feature slice (create, list, detail, update, status, comments, export, search, auth)
- Before marking acceptance criteria checkbox complete
- User requests review of frontend + backend changes together

## Steps

1. **Identify scope** — which feature: e.g., "status transition", "CSV export", "add comment".

2. **Check acceptance criteria** — open `acceptance-criteria.md`; list relevant unchecked items.

3. **Backend review**
   - Route matches `api-contract.md`
   - Validation on all inputs; no direct status mutation outside status endpoint
   - State machine rules per `state-machine.mdc`
   - Error shape per `api-error-shape.mdc`
   - Auth enforced; `createdBy` set from JWT on create
   - No secrets in code

4. **Frontend review**
   - UI shows API error `message` and field `details`
   - Status actions match allowed transitions for current status
   - Protected routes redirect unauthenticated users
   - CSV export triggers correct endpoint

5. **Test review**
   - Integration tests exist for status changes if scope includes status
   - Tests use real PostgreSQL per `testing-discipline.mdc`

6. **Record findings** — classify as Critical / Suggestion / Nice-to-have; update `code-review-notes.md`.

7. **Fix or ticket** — apply critical fixes; log in `review-fixes.md` with commit reference placeholder.

## Expected Output

- Structured review: Critical / Suggestion / Nice-to-have findings
- Mapping to `acceptance-criteria.md` items (pass/fail/partial)
- List of required fixes before feature is "done"
- Updated `code-review-notes.md` section for this feature

## Files Updated

| File | Action |
|------|--------|
| `code-review-notes.md` | Review findings |
| `review-fixes.md` | If fixes applied |
| `acceptance-criteria.md` | Check boxes only when verified |
| `ai-prompts/code-review.md` | Capture review session |
| `src/**`, `tests/**` | Apply critical fixes if in scope |
