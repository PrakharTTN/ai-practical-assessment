# UI Flow

## Authentication Flow

1. User visits any protected route (`/tickets`, `/tickets/new`, `/tickets/:id`, `/users`)
2. `ProtectedRoute` checks JWT in `sessionStorage`; if present, loads profile via `GET /api/auth/me`
3. If missing or invalid → redirect to `/login` (preserves `from` location)
4. User submits email + password → `POST /api/auth/login` → `GET /api/auth/me`
5. On success: token stored, user profile in context, redirect to intended page
6. On failure: error banner with API `message` (no seeded credentials shown on login page)
7. **Logout:** header "Sign out" clears token and profile → redirect to `/login`

**First startup:** default admin `admin@admin.com` / `admin` (documented in `database/seed-data/README.md` only).

## Ticket List Flow

1. After login, user lands on `/tickets`
2. Table shows all tickets from `GET /api/tickets`
3. **Filters:** status dropdown, priority dropdown, title search → Apply resubmits query
4. Row title link → `/tickets/:id`
5. **Export:** "Export My Tickets" → `GET /api/tickets/export` → browser download
6. **New ticket:** nav link → `/tickets/new`

## Create Ticket Flow

1. User opens `/tickets/new`
2. Fills title, description, priority, optional assignee (from `GET /api/users`)
3. Submit → `POST /api/tickets`
4. Validation errors map to field labels via `details`
5. Success → redirect to new ticket detail page

## Ticket Detail Flow

1. User opens `/tickets/:id` → `GET /api/tickets/{id}` with comments
2. **Workflow panel:** status action buttons for allowed transitions only
3. **Edit form:** update title, description, priority, assignee → `PATCH /api/tickets/{id}`
4. Status is read-only in edit form (not in PATCH body)
5. **Comments:** list shown; add via form → `POST /api/tickets/{id}/comments`
6. Page reloads comments after post

## Status Change Flow

1. Detail page shows buttons only for **allowed** next statuses (derived from `getAllowedTransitions`)
2. Click button → `PATCH /api/tickets/{id}/status`
3. Invalid transition: error banner shows API `message` (ticket detail remains visible)
4. Valid transition: status badge updates

### Allowed actions by status

| Current | Buttons shown |
|---------|---------------|
| `open` | In progress, Cancelled |
| `in_progress` | Resolved, Cancelled |
| `resolved` | Closed |
| `closed` | *(none)* |
| `cancelled` | *(none)* |

## Team Management Flow (admin only)

1. Admin sees **Team** in header nav
2. `/users` — two-column layout: create/edit form + user table
3. **Create:** fill name, email, password, role (Support or Admin) → `POST /api/users`
4. **Edit:** click Edit on a row → form switches to edit mode; password optional (blank = unchanged)
5. Save → `PATCH /api/users/{id}`; Cancel clears edit mode
6. Support agents redirected away from `/users` (no nav link)

## CSV Export Flow

1. From ticket list, click "Export My Tickets"
2. Authenticated request to `/api/tickets/export`
3. Blob download as `tickets_export.csv`
4. Contains only tickets where `created_by` = logged-in user

## Error States

| Scenario | UI behavior |
|----------|-------------|
| 401 unauthorized | Redirect to login (protected routes) |
| 403 forbidden | Error banner (e.g. agent on user endpoints) |
| 422 validation | Field errors under inputs + banner |
| 400 invalid status | Banner on detail page; status unchanged |
| 404 not found | Banner + back link |
| 409 duplicate email | Banner + field error on team form |
| Network failure | Generic connection error banner |

## Navigation Map

```
/login                    LoginPage (public)
/tickets                  TicketListPage (protected)
/tickets/new              CreateTicketPage (protected)
/tickets/:id              TicketDetailPage (protected)
/users                    UsersPage (protected, admin only)
/                         → redirect /tickets
```

## Layout (protected)

Sticky header: **Support Desk** brand | Tickets | New Ticket | Team *(admin)* | user chip (name + role) | Sign out

App shell uses card-based panels, data tables, and consistent styling with the login page (gradient background, rounded panels, focus states).
