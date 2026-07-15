# Design Notes

## Architecture Overview

```
Browser (React/Vite :5173)
    │  JWT Bearer + JSON
    ▼
FastAPI (:8000)
    │  SQLAlchemy
    ▼
PostgreSQL (:5432)
```

- **Frontend:** SPA with React Router; auth token in `sessionStorage`; profile via `/api/auth/me`
- **Backend:** Layered — routers → services (state machine, auth) → models
- **Database:** PostgreSQL with Alembic migrations + idempotent seed script

## Frontend Design

### Structure

```
src/frontend/src/
  api/           # client.ts, auth.ts, tickets.ts, users.ts
  context/       # AuthContext (login/logout/token/user/role)
  components/    # Layout, ProtectedRoute, AdminRoute, ErrorBanner
  pages/         # Login, TicketList, CreateTicket, TicketDetail, Users
  types/         # TypeScript API types
  utils/         # status transition helpers
  test/          # Vitest setup
```

### Routing

| Route | Page | Auth |
|-------|------|------|
| `/login` | LoginPage | Public |
| `/tickets` | TicketListPage | Protected |
| `/tickets/new` | CreateTicketPage | Protected |
| `/tickets/:id` | TicketDetailPage | Protected |
| `/users` | UsersPage | Protected + admin |

### State management

- Auth: React Context + `sessionStorage`; `user` loaded on mount and after login
- Ticket data: local component state, refetched after mutations
- Team page: local form state with create/edit mode toggle
- No global ticket store (assessment scope)

### UI / styling

- Login: centered card on gradient background; credentials not displayed
- App shell: sticky header, nav pills, user role chip, card panels, data tables
- Shared design tokens: slate/blue palette, 8–14px border radius, subtle shadows
- Responsive: stacked grids below 900px

### Error handling UI

- `ApiError` class parses `{ error, message, details }`
- `ErrorBanner` for API messages; `success-banner` for team page confirmations
- `getFieldErrors()` maps 422 `details` to form fields
- Status errors shown on detail page without clearing ticket view

## Backend Design

### Routers

| Module | Prefix | Responsibility |
|--------|--------|----------------|
| `auth.py` | `/api/auth` | Login, JWT issuance, current user profile |
| `users.py` | `/api/users` | List users; admin create/update |
| `tickets.py` | `/api/tickets` | CRUD, status, comments, export |

### Services

- `auth.py` — bcrypt verify/hash, JWT encode/decode
- `ticket_state_machine.py` — **single** status enforcement point

### Auth & authorization

- `get_current_user` dependency on all protected routes
- `require_admin` dependency on user create/update
- `created_by` always from JWT, never request body

### User onboarding

- First startup: seed creates default admin (`admin@admin.com` / `admin`)
- Post-login: admin creates/edits users via API; passwords bcrypt-hashed server-side

## Database Design

See [data-model.md](./data-model.md). Three tables with PostgreSQL enums and FK constraints.

## Validation Strategy

| Layer | Mechanism |
|-------|-----------|
| API input | Pydantic schemas (`Field` min/max, enums) |
| DB | NOT NULL, FK, enum types |
| Status | `ticket_state_machine.validate_transition()` |
| UI | HTML5 `required` + display API 422 `details` |

## Error Handling Strategy

Backend returns `{ error, message, details, ...extra }`. Frontend `apiFetch` throws `ApiError` for non-2xx. Invalid status includes `current_status` and `requested_status`.

## Testing Strategy Link

See [test-strategy.md](./test-strategy.md).

- Backend: **45** integration tests on real PostgreSQL
- Frontend: **14** Vitest component tests + manual Docker walkthrough
