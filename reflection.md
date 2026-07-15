# Reflection

## What I Built

A support ticket management web app: agents and admins log in, manage tickets through a fixed lifecycle (`open` → `in_progress` → `resolved` → `closed`, with `cancelled` branches), add comments, export their own tickets as CSV, and (for admins) onboard team members. Backend enforces the state machine; frontend only shows valid next actions.

## How I Used AI (across the lifecycle)

1. **Analysis** — Scoped the assessment brief into requirements, acceptance criteria, and a 7-milestone plan
2. **Scaffolding** — Repo structure, Docker, Cursor rules/skills
3. **Database** — Models, migration, seed; reviewed for autoincrement and enum issues
4. **Backend** — Full API with unified error shape; contract synced after each router
5. **Tests** — Integration suite on real Postgres; state machine as mandatory proof
6. **Frontend** — Pages, auth, styling, team management; Vitest for key components
7. **Verification** — Docker stack, manual walkthrough, documentation updates

## What AI Helped With Most

- Boilerplate speed (FastAPI routers, Pydantic schemas, React page structure)
- Integration test parametrization for state machine cases
- Docker compose + entrypoint scripting
- Consistent error-handling patterns across backend and frontend
- CSS/layout iteration for professional UI without a component library

## What AI Got Wrong

- Initial migration missing `autoincrement=True` on PKs
- Enum creation duplicated in Alembic
- `bcrypt` 4.1 incompatibility with passlib — caught by test failures
- Brief port change to 5433 during local conflict — reverted after user feedback
- Early login page exposed seeded credentials — fixed per security/UX feedback

## How I Validated AI Output

- Ran `pytest` and `npm test` after each backend/frontend slice
- Manual curl smoke tests and Docker `docker-up-local` checklist
- User verification of team management and UI styling
- Code review notes + `review-fixes.md` for tracked findings

## What I Would Improve Next

- E2E browser tests (Playwright) for login → ticket → export flow
- Prevent demoting/deleting the last admin
- Password reset and email invite instead of admin-set temporary passwords
- `ai-prompts/` session capture during work, not only at M7

## Reusable Workflow (prompts, rules, specs, templates)

- Milestone plan with acceptance criteria as gate
- `state-machine.mdc` + integration tests pattern
- `api-contract-sync.mdc` — contract updated with every route change
- `docker-up-local` skill for reproducible demos
- `test-results.md` as single source for verification evidence
- `debugging-notes.md` filled when issues occur (see 8 documented issues)
- 15 curated sessions in `ai-prompts/` — see `final-ai-usage-summary.md`

## M7 Closure

- All lifecycle artifacts complete and cross-linked from `candidate-info.md`
- User verified M6; submission review recorded in `code-review-notes.md`
- Fill name/role in `candidate-info.md` before final hand-in
