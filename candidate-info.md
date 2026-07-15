# Candidate Information

| Field | Value |
|-------|-------|
| **Name** | Prakhar Nigam |
| **Role** | Software Engineer |
| **Primary Technology Stack** | Python (FastAPI), PostgreSQL, TypeScript (React + Vite) |
| **Primary AI Tool Used** | Cursor Agent |
| **Project Option Selected** | Support Ticket Management System |
| **Assessment Start Date** | 2026-07-10 |
| **Submission Date** | 2026-07-15 |

## Project Summary

Internal support ticket web application. Authenticated users create and manage tickets through a fixed status lifecycle (`open` → `in_progress` → `resolved` → `closed`, with `cancelled` branches). Features include comments, search/filter, CSV export (self-created tickets only), JWT auth, Docker-based local stack, and admin team management (create/edit users).

**Deliverables:** Working full-stack app, 45 backend + 14 frontend tests, Alembic migrations, seed data, and complete AI-assisted workflow documentation.

## Tools Used

| Category | Tools |
|----------|-------|
| IDE / AI | Cursor, Cursor rules & skills |
| Backend | FastAPI, SQLAlchemy, Alembic, passlib/bcrypt, python-jose |
| Frontend | React 18, Vite, TypeScript, React Router, Vitest, Testing Library |
| Database | PostgreSQL 16 |
| Testing | pytest, Vitest |
| DevOps | Docker Compose |
| Version control | Git |

## Setup Summary

```bash
# Quick start (Docker — recommended)
cp .env.example .env
chmod +x scripts/docker/*.sh
docker compose up --build
# → http://localhost:5173 (login: admin@admin.com / admin — see database/seed-data/README.md)

# Tests
docker compose up -d postgres
pytest tests/backend -v          # 45 tests
cd src/frontend && npm test      # 14 tests
```

See [README.md](./README.md) for native setup, environment variables, and troubleshooting.

## Submission Artifacts Index

| Artifact | Purpose |
|----------|---------|
| [README.md](./README.md) | Setup and run instructions |
| [acceptance-criteria.md](./acceptance-criteria.md) | Definition of done checklist |
| [test-results.md](./test-results.md) | Test and verification evidence |
| [reflection.md](./reflection.md) | Honest reflection on AI usage |
| [pr-description.md](./pr-description.md) | PR-style submission summary |
| [tool-workflow.md](./tool-workflow.md) | How Cursor was used across phases |
| [final-ai-usage-summary.md](./final-ai-usage-summary.md) | Curated session overview |
| [ai-prompts/](./ai-prompts/) | 15 prompt sessions by phase |
| [debugging-notes.md](./debugging-notes.md) | Issues and fixes log |
| [code-review-notes.md](./code-review-notes.md) | Review findings |
