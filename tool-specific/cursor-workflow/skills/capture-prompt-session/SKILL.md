---
name: capture-prompt-session
description: >-
  Captures a Cursor AI session into ai-prompts/ for the Support Ticket
  Management assessment. Use after planning, design, implementation, testing,
  debugging, code review, or documentation work worth preserving.
---

# Capture Prompt Session

## When to Use

- Completed a meaningful Cursor session (not trivial one-liners)
- Implemented or debugged a ticket feature
- Made a design or requirement decision with AI help
- User asks to log prompt history for assessment submission
- `artifact-discipline.mdc` reminder applies

## Steps

1. **Classify phase** — pick target file:
   | Phase | File |
   |-------|------|
   | Requirements / planning | `ai-prompts/planning.md` |
   | Architecture / design | `ai-prompts/design.md` |
   | Code generation | `ai-prompts/implementation.md` |
   | Tests | `ai-prompts/testing.md` |
   | Debugging | `ai-prompts/debugging.md` |
   | Code review | `ai-prompts/code-review.md` |
   | Docs / artifacts | `ai-prompts/documentation.md` |

2. **Draft entry** — append new section (most recent at top or bottom — stay consistent):

   ```markdown
   ## Session: <short title>
   **Date:** YYYY-MM-DD

   ### Prompt
   <user prompt summary or key excerpt>

   ### AI Response Summary
   <what AI proposed>

   ### Accepted
   <what was used verbatim>

   ### Changed
   <what was modified and why>

   ### Rejected
   <what was discarded and why>
   ```

3. **Link artifacts** — note related files touched (e.g., `api-contract.md`, `test-results.md`).

4. **Export optional** — if full chat export exists, save to `tool-specific/cursor-workflow/exports/` and link filename in entry.

5. **Update summary** — add one-line entry to `final-ai-usage-summary.md` session table if milestone-sized.

## Expected Output

- New session block in appropriate `ai-prompts/<phase>.md`
- Confirmation of phase, title, and files linked
- Optional export path if chat exported

## Files Updated

| File | Action |
|------|--------|
| `ai-prompts/<phase>.md` | Primary — session entry |
| `final-ai-usage-summary.md` | Milestone sessions only |
| `tool-specific/cursor-workflow/exports/` | Optional raw export |
| `tool-workflow.md` | If workflow pattern emerged |
