# Frontend

React + Vite + TypeScript SPA for the Support Ticket Management System.

## Run

```bash
npm install
export VITE_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:5173 and sign in. Default admin on first startup: `admin@admin.com` / `admin` (documented in [database/seed-data/README.md](../../database/seed-data/README.md) — not shown in the UI).

## Build

```bash
npm run build
```

## Features

- JWT login/logout (`sessionStorage`)
- Protected routes with session restore via `/api/auth/me`
- **Team management** (admin only): create and edit support agents and admins at `/users`
- Ticket list with status/priority filter and title search
- Create ticket with assignee picker
- Ticket detail: edit fields, status actions, comments
- CSV export (self-created tickets only)
- API error display (banner + field errors)
- Professional UI: styled login page and app shell (cards, tables, nav)

## Test

```bash
npm test        # Vitest — 14 component tests
npm run build   # production build
```
