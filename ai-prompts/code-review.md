# Code Review Prompts

## Session: M3 database review

**Date:** 2026-07-10

### Prompt

Review M3 database layer against `data-model.md` and `state-machine.mdc`. Update `code-review-notes.md`.

### AI Response Summary

Found critical PK autoincrement missing in migration. Verified enum values, FK rules, seed coverage. Logged fixes in `code-review-notes.md` and `review-fixes.md`.

### Accepted

- Critical fix: `autoincrement=True` on all PK columns
- Enum `create_type=False` pattern
- `values_callable` for lowercase enum inserts

### Changed

- Deferred duplicate email index cleanup (cosmetic)

### Rejected

- DB-level CHECK constraints for state machine

---

## Session: M7 final submission review

**Date:** 2026-07-15

### Prompt

Final review before submission — verify acceptance criteria, state machine, auth, tests, docs completeness (`review-ticket-feature` skill).

### AI Response Summary

Walked acceptance criteria: all Core items pass. State machine enforced in single service; 45 integration tests green. Auth + admin user management verified. Docs traceable from README → tests → prompts. Logged deferred items (delete user, role-based transitions, E2E).

### Accepted

- Submission-ready with honest limitations section
- `acceptance-criteria.md` Definition of Done complete except candidate-specific fields

### Changed

- User management marked as enhancement beyond original Core scope but fully implemented

### Rejected

- Checking acceptance boxes without test/manual evidence
- Adding role-based ticket transitions at last minute (scope creep)
