---
name: sync-api-docs
description: >-
  Syncs api-contract.md with FastAPI router implementations for the Support
  Ticket Management System. Use when adding, changing, or removing backend
  routes, or when api-contract.md is out of date with src/backend routers.
---

# Sync API Docs

## When to Use

- After creating or editing any file in `src/backend/**/routers/`
- When user asks to document endpoints or update the API contract
- Before marking an API feature complete
- When review finds mismatch between code and `api-contract.md`

## Steps

1. **Inventory routes** — read all router modules under `src/backend/`; list every `@router.get/post/patch/delete` with method, path, auth dependency, request body schema, response model.

2. **Read current contract** — open `api-contract.md` and note existing sections.

3. **Diff** — identify missing, stale, or orphaned sections (contract entries with no route, routes with no entry).

4. **Update `api-contract.md`** — for each endpoint use the template from `.cursor/rules/api-contract-sync.mdc`:
   - Method, path, purpose
   - Request (body + query params with types)
   - Response (success + error codes)
   - Validation rules (required fields, enums: priority, status)
   - Auth requirement (Bearer JWT or public)

5. **Cross-update** — if schemas changed, update `data-model.md` field tables and `design-notes.md` backend section if architecture shifted.

6. **Verify** — confirm ticket-system endpoints are documented:
   - Auth: `POST /api/auth/login`
   - Tickets: list, create, get, patch, status, comments, export

## Expected Output

- Updated `api-contract.md` with every live route documented
- Short summary listing: endpoints added/changed/removed
- Note any intentional gaps (e.g., stretch features not yet built)

## Files Updated

| File | Action |
|------|--------|
| `api-contract.md` | Primary — full sync |
| `data-model.md` | If request/response shapes changed |
| `design-notes.md` | If new endpoints affect architecture |
| `ai-prompts/documentation.md` | Optional — capture session if user requests |
