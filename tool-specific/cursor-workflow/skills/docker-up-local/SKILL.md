---
name: docker-up-local
description: >-
  Starts the Support Ticket Management System local Docker stack (postgres,
  backend, frontend) for manual verification. Use when the user wants to run
  docker compose, verify the app locally, rebuild containers, or debug Docker
  startup failures.
---

# Docker Up Local

Stretch workflow support — **not production deployment**. Brings up postgres + FastAPI + Vite for manual smoke testing.

## When to Use

- User says "docker up", "start the stack", "run locally in Docker"
- Manual verification before/after a feature slice
- Debugging container startup, migration, or seed failures
- Rebuilding images after dependency changes (`requirements.txt`, `package.json`)

## Step 1 — Inspect Repo Structure

Verify these paths exist and match `docker-compose.yml`:

| Expected path | Purpose |
|---------------|---------|
| `docker-compose.yml` | Orchestration |
| `src/backend/Dockerfile` | Backend image |
| `src/frontend/Dockerfile` | Frontend image |
| `src/backend/app/main.py` | FastAPI entry (`app.main:app`) |
| `src/backend/requirements.txt` | Python deps |
| `src/frontend/package.json` | Node deps |
| `scripts/docker/backend-entrypoint.sh` | Wait → migrate → seed → start |
| `scripts/docker/migrate.sh` | `alembic upgrade head` |
| `scripts/docker/seed.sh` | `python -m app.seed` |
| `.env.example` | Placeholder env vars |

If paths differ, **update `docker-compose.yml` volumes/build contexts before running** — do not silently assume.

## Step 2 — Pre-flight Checks

Tell the user to confirm:

```bash
docker --version
docker compose version
```

Ensure `.env` exists (never commit it):

```bash
cp .env.example .env
```

Review `.env` — placeholders only per `security-and-env.mdc`. Inside Docker, `DATABASE_URL` must use host `postgres`, not `localhost`.

Make scripts executable (once per clone):

```bash
chmod +x scripts/docker/*.sh
```

## Step 3 — Start Commands

**First start or after Dockerfile / dependency changes:**

```bash
docker compose up --build
```

**Detached:**

```bash
docker compose up --build -d
```

**Rebuild single service after code-only changes** (volumes mount source — usually just restart):

```bash
docker compose restart backend
docker compose restart frontend
```

**Force rebuild one service:**

```bash
docker compose up --build -d backend
```

## Step 4 — Exposed URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API health | http://localhost:8000/api/health |
| API docs (when implemented) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

## Step 5 — Post-startup Verification

Run these checks and report results to the user:

### Infrastructure

```bash
docker compose ps
curl -s http://localhost:8000/api/health
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173
```

Expect all containers `running`; health returns `{"status":"ok",...}`; frontend HTTP 200.

### Application (once features are implemented)

1. **Open ticket list** — login if auth enabled → navigate to ticket list → tickets load from API
2. **Create ticket** — submit form with title, description, priority → appears in list
3. **Invalid status transition rejected** — on `open` ticket, attempt `resolved` → UI shows error; API returns `invalid_status_transition`
4. **CSV export works** — export as logged-in user → CSV downloads with only self-created tickets

If features are not implemented yet, note which steps are blocked and what infrastructure checks passed.

## Step 6 — Stop / Down Commands

```bash
# Stop containers, keep data volume
docker compose stop

# Stop and remove containers, keep postgres volume
docker compose down

# Stop, remove containers AND delete database volume (fresh DB)
docker compose down -v
```

## Startup Failure — Debug Workflow

Do **not** silently regenerate files. Follow `debug-backend-issue` patterns:

1. **Capture logs**
   ```bash
   docker compose logs postgres --tail=50
   docker compose logs backend --tail=100
   docker compose logs frontend --tail=50
   ```

2. **Classify failure**

   | Symptom | Likely cause |
   |---------|----------------|
   | `postgres` unhealthy | Port 5432 in use, bad credentials |
   | Backend restart loop | `DATABASE_URL` wrong, migration error, missing `requirements.txt` dep |
   | `alembic.ini not found` | Migrations not scaffolded yet — expected until backend DB setup |
   | `app/seed.py not found` | Seed not implemented yet — expected until seed script added |
   | Frontend blank / ECONNREFUSED | Backend not up, `VITE_API_URL` mismatch |
   | `permission denied` on entrypoint | Run `chmod +x scripts/docker/*.sh` |

3. **Fix** — smallest change; update Docker paths if repo layout changed.

4. **Document** — append to `debugging-notes.md`:

   ```markdown
   ## Issue: Docker startup failure
   **Date:** YYYY-MM-DD

   ### Problem
   <symptom>

   ### How I Investigated
   <logs commands run>

   ### How AI Helped
   <docker-up-local skill guidance used>

   ### What I Validated
   <what confirmed the fix>

   ### Final Fix
   <change made>
   ```

5. **Capture session** — optional `capture-prompt-session` to `ai-prompts/debugging.md`.

## Expected Output (when skill completes)

- Confirmation that Docker paths match repo layout
- Exact commands for the user's situation (first start / rebuild / down)
- Infrastructure verification results (or log excerpts if failed)
- Application verification checklist status (pass / blocked / fail)
- Limitations noted (see below)
- `debugging-notes.md` entry if startup failed

## Files This Skill May Update

| File | When |
|------|------|
| `debugging-notes.md` | Startup or migration failure |
| `ai-prompts/debugging.md` | Session capture after Docker debug |
| `docker-compose.yml` | Path mismatch fix |
| `README.md` | If ports or commands change |

## Limitations

- **Dev mode only** — `--reload` / Vite HMR; not production-hardened
- **Postgres data persists** in `postgres_data` volume until `docker compose down -v`
- **Migrate/seed skip gracefully** until `alembic.ini` and `app/seed.py` exist
- **Browser → API** uses `http://localhost:8000` (`VITE_API_URL`); backend → DB uses `postgres` hostname
- **Port conflicts** — if 5432/8000/5173 are taken, edit `docker-compose.yml` port mappings
- **No HTTPS, no multi-stage prod images** — assessment stretch only
