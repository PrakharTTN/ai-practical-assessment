# API Contract

All protected routes require header: `Authorization: Bearer <access_token>`

Error shape: `{ "error": "<code>", "message": "<text>", "details": {} }`

---

## Endpoint: Health Check

Method: GET  
Path: `/api/health`  
Purpose: Liveness check for Docker, load balancers, and smoke tests  
Auth: Public

### Response `200`

```json
{
  "status": "ok",
  "service": "ticket-api"
}
```

### Notes

- Root path `GET /health` also returns `{"status": "ok"}` (no `service` field) — legacy/simple probe
- Used by `docker-up-local` skill verification and `tests/backend/test_health.py`

---

## Endpoint: Login

Method: POST  
Path: `/api/auth/login`  
Purpose: Authenticate seeded user and receive JWT  
Auth: Public

### Request

```json
{
  "email": "admin@admin.com",
  "password": "admin"
}
```

### Response `200`

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Validation Rules

- `email` — required, valid email format
- `password` — required, non-empty

### Error Responses

- `401 unauthorized` — invalid email or password

---

## Endpoint: Current User

Method: GET  
Path: `/api/auth/me`  
Purpose: Return authenticated user profile (role, name, email)  
Auth: Bearer JWT required

### Response `200`

```json
{
  "id": 1,
  "name": "Admin User",
  "email": "admin@admin.com",
  "role": "admin"
}
```

### Error Responses

- `401 unauthorized`

---

## Endpoint: List Users

Method: GET  
Path: `/api/users`  
Purpose: Return seeded users for assignee dropdown (no passwords)  
Auth: Bearer JWT required

### Response `200`

```json
[
  { "id": 1, "name": "Admin User", "email": "admin@admin.com", "role": "admin" }
]
```

### Error Responses

- `401 unauthorized`

---

## Endpoint: Create User

Method: POST  
Path: `/api/users`  
Purpose: Onboard a new admin or support agent (admin only)  
Auth: Bearer JWT — **admin role required**

### Request

```json
{
  "name": "Jane Smith",
  "email": "jane@company.com",
  "password": "temporary1",
  "role": "agent"
}
```

`role` — `admin` or `agent` (`agent` = support staff in the UI)

### Response `201`

```json
{
  "id": 3,
  "name": "Jane Smith",
  "email": "jane@company.com",
  "role": "agent"
}
```

### Validation Rules

- `name` — required, 1–100 characters
- `email` — required, valid format, unique
- `password` — required, min 6 characters
- `role` — required enum: `admin`, `agent`

### Error Responses

- `401 unauthorized`
- `403 forbidden` — caller is not admin
- `409 duplicate_email` — email already registered
- `422 validation_error` — invalid fields

---

## Endpoint: Update User

Method: PATCH  
Path: `/api/users/{id}`  
Purpose: Update an existing admin or support agent (admin only)  
Auth: Bearer JWT — **admin role required**

### Request

All fields optional; at least one required. Omit `password` to leave it unchanged.

```json
{
  "name": "Jane Smith",
  "email": "jane.smith@company.com",
  "password": "newpassword1",
  "role": "admin"
}
```

### Response `200`

```json
{
  "id": 3,
  "name": "Jane Smith",
  "email": "jane.smith@company.com",
  "role": "admin"
}
```

### Validation Rules

- `name` — optional, 1–100 characters
- `email` — optional, valid format, unique among other users
- `password` — optional, min 6 characters when provided
- `role` — optional enum: `admin`, `agent`

### Error Responses

- `401 unauthorized`
- `403 forbidden` — caller is not admin
- `404 not_found` — user id does not exist
- `409 duplicate_email` — email already registered
- `422 validation_error` — invalid fields or empty body

---

## Endpoint: List Tickets

Method: GET  
Path: `/api/tickets`  
Purpose: List tickets with optional search/filter  
Auth: Bearer JWT required

### Request

Query parameters (all optional):

| Param | Type | Description |
|-------|------|-------------|
| `status` | enum | `open`, `in_progress`, `resolved`, `closed`, `cancelled` |
| `priority` | enum | `low`, `medium`, `high` |
| `search` | string | Case-insensitive substring match on `title` |

### Response `200`

```json
[
  {
    "id": 1,
    "title": "Cannot reset password",
    "description": "...",
    "priority": "high",
    "status": "open",
    "assigned_to": { "id": 2, "name": "Support Agent", "email": "agent@example.com", "role": "agent" },
    "created_by": { "id": 1, "name": "Admin User", "email": "admin@admin.com", "role": "admin" },
    "created_at": "2026-07-10T12:00:00+00:00",
    "updated_at": "2026-07-10T12:00:00+00:00"
  }
]
```

### Error Responses

- `401 unauthorized` — missing or invalid token

---

## Endpoint: Create Ticket

Method: POST  
Path: `/api/tickets`  
Purpose: Create a new support ticket  
Auth: Bearer JWT required

### Request

```json
{
  "title": "Printer not working",
  "description": "Floor 2 printer shows offline",
  "priority": "medium",
  "assigned_to_id": 2
}
```

### Response `201`

Ticket object with `status: "open"`, `created_by` set from JWT (client-supplied `created_by` ignored).

### Validation Rules

- `title` — required, 1–200 chars
- `description` — required, 1–5000 chars
- `priority` — required, one of `low`, `medium`, `high`
- `assigned_to_id` — optional; must reference existing user if provided
- `status` — not accepted on create; always `open`

### Error Responses

- `401 unauthorized`
- `404 not_found` — assignee user does not exist
- `422 validation_error` — missing/invalid fields

---

## Endpoint: Export Tickets (CSV)

Method: GET  
Path: `/api/tickets/export`  
Purpose: Export authenticated user's self-created tickets as CSV  
Auth: Bearer JWT required

### Request

No body. No `userId` override param.

### Response `200`

`Content-Type: text/csv`  
`Content-Disposition: attachment; filename=tickets_export.csv`

Columns: `id`, `title`, `description`, `priority`, `status`, `assigned_to_email`, `created_at`, `updated_at`

Only tickets where `created_by_id` matches the authenticated user.

### Error Responses

- `401 unauthorized`

---

## Endpoint: Get Ticket

Method: GET  
Path: `/api/tickets/{id}`  
Purpose: Retrieve ticket details including comments  
Auth: Bearer JWT required

### Response `200`

```json
{
  "id": 1,
  "title": "...",
  "description": "...",
  "priority": "high",
  "status": "open",
  "assigned_to": null,
  "created_by": { "id": 1, "name": "...", "email": "...", "role": "admin" },
  "created_at": "...",
  "updated_at": "...",
  "comments": [
    {
      "id": 1,
      "message": "...",
      "created_by": { "id": 2, "name": "...", "email": "...", "role": "agent" },
      "created_at": "..."
    }
  ]
}
```

### Error Responses

- `401 unauthorized`
- `404 not_found` — ticket does not exist

---

## Endpoint: Update Ticket

Method: PATCH  
Path: `/api/tickets/{id}`  
Purpose: Update ticket fields (title, description, priority, assignee) — **not status**  
Auth: Bearer JWT required

### Request

```json
{
  "title": "Updated title",
  "priority": "high",
  "assigned_to_id": null
}
```

All fields optional; at least one required.

### Response `200`

Updated ticket object (without comments list populated on patch response — includes comments from detail load).

### Validation Rules

- `status` — **not accepted**; use status endpoint
- `assigned_to_id` — must reference existing user if not null

### Error Responses

- `401 unauthorized`
- `404 not_found` — ticket or assignee not found
- `422 validation_error` — empty body or invalid fields

---

## Endpoint: Change Ticket Status

Method: PATCH  
Path: `/api/tickets/{id}/status`  
Purpose: Transition ticket status via enforced state machine  
Auth: Bearer JWT required

### Request

```json
{
  "status": "in_progress"
}
```

### Response `200`

Updated ticket object.

### Validation Rules — Allowed transitions

| From | To |
|------|-----|
| `open` | `in_progress`, `cancelled` |
| `in_progress` | `resolved`, `cancelled` |
| `resolved` | `closed` |

Same-status and all other transitions are rejected.

### Error Responses

- `400 invalid_status_transition`:

```json
{
  "error": "invalid_status_transition",
  "message": "Cannot transition from 'open' to 'resolved'",
  "details": {},
  "current_status": "open",
  "requested_status": "resolved"
}
```

- `401 unauthorized`
- `404 not_found`

---

## Endpoint: Add Comment

Method: POST  
Path: `/api/tickets/{id}/comments`  
Purpose: Add a comment to a ticket  
Auth: Bearer JWT required

### Request

```json
{
  "message": "Investigating the issue now."
}
```

### Response `201`

```json
{
  "id": 5,
  "message": "Investigating the issue now.",
  "created_by": { "id": 1, "name": "...", "email": "...", "role": "admin" },
  "created_at": "..."
}
```

`created_by` set from JWT.

### Validation Rules

- `message` — required, 1–5000 chars

### Error Responses

- `401 unauthorized`
- `404 not_found` — ticket does not exist
- `422 validation_error` — empty message
