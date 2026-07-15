# Prompt Templates

Copy, fill placeholders, and attach referenced files with `@`.

---

## Requirements / Planning

```
@requirements-analysis.md @acceptance-criteria.md

I'm implementing the Support Ticket Management System (FastAPI + React + PostgreSQL).

Feature: <e.g., ticket status transitions>

Break down into:
1. Backend tasks
2. Frontend tasks
3. Tests required (cite testing-discipline)
4. Artifacts to update

Do not write code yet.
```

---

## Design / API Contract

```
@data-model.md @design-notes.md

Design <feature> for the ticket system.

Include:
- Endpoints (method, path, auth)
- Request/response JSON shapes
- Validation rules and error codes per api-error-shape
- Status transitions if applicable (only allowed transitions from state-machine rule)

Output: updates for api-contract.md and data-model.md sections.
```

---

## Backend Implementation

```
@api-contract.md @.cursor/rules/state-machine.mdc

Implement <endpoint or service> in src/backend/ per api-contract.md.

Constraints:
- Status changes only via PATCH /api/tickets/{id}/status and ticket_state_machine service
- JWT auth on all ticket routes; createdBy from token on create
- Error shape: { error, message, details }

After implementation, sync api-contract.md if anything diverged.
```

---

## State Machine + Tests

```
@.cursor/rules/state-machine.mdc @.cursor/rules/testing-discipline.mdc

Implement ticket status state machine and PostgreSQL integration tests.

Valid: open→in_progress, open→cancelled, in_progress→resolved, in_progress→cancelled, resolved→closed
Invalid: must return invalid_status_transition

Use write-state-machine-tests skill workflow. Run pytest and update test-results.md.
```

---

## Frontend Feature

```
@ui-flow.md @api-contract.md @.cursor/rules/api-error-shape.mdc

Implement <page/component> in src/frontend/.

Requirements:
- Show API error message and field details on forms
- Status buttons only for valid next states from current status
- Protected route; redirect to login if unauthenticated

Match ui-flow.md for <flow name>.
```

---

## Debug

```
@debugging-notes.md

Bug: <symptom>
Request: <method path body>
Response: <status + JSON>
Expected: <behavior>

Follow debug-backend-issue skill. Smallest fix; add regression test if missing.
Document in debugging-notes.md when resolved.
```

---

## Code Review

```
@acceptance-criteria.md @code-review-notes.md

Review my changes for <feature> (backend + frontend + tests).

Check: state machine, api-contract sync, error shape, auth, real-DB tests, no secrets.

Use review-ticket-feature skill format: Critical / Suggestion / Nice-to-have.
```

---

## Capture Session

```
Use capture-prompt-session skill.

Phase: <planning|design|implementation|testing|debugging|code-review|documentation>
Title: <short title>
Summary of what we did: <2-3 sentences>
Accepted: <what we kept>
Changed: <what we modified>
Rejected: <what we skipped>
Files touched: <list>
```

---

## CSV Export

```
@api-contract.md @acceptance-criteria.md

Implement GET /api/tickets/export returning CSV of tickets where createdBy matches authenticated user.

Columns: id, title, description, priority, status, assignedTo, createdAt, updatedAt
Auth required; no userId override param.
Update api-contract.md and add integration test.
```

---

## Auth (Stretch)

```
@api-contract.md @.cursor/rules/security-and-env.mdc

Implement JWT login: POST /api/auth/login.

- bcrypt password hashes in DB
- Bearer token on ticket/comment/export routes
- .env.example with placeholders only

Do not commit secrets. Update api-contract.md auth section.
```
