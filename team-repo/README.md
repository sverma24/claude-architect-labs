# Lab C: Team Repo

A small Python shop backend with a full team Claude Code setup. It's the Code Generation with Claude Code and
Developer Productivity scenarios from the Claude Certified Architect – Foundations exam guide.

| File | Exam topics |
|---|---|
| `CLAUDE.md` with `@docs/standards/*.md` imports | 3.1 project-level instructions shared through git, @import |
| `shop/billing/CLAUDE.md` | 3.1 directory-level instructions |
| `.claude/rules/tests.md` (`paths: ["**/*_test.py"]`), `.claude/rules/api.md` | 3.3 path-scoped rules for files spread across folders |
| `.claude/commands/review.md` | 3.2 a project slash command (`/review`) every teammate gets |
| `.claude/skills/codebase-map/SKILL.md` (`context: fork`, `allowed-tools`, `argument-hint`) | 3.2 skills, 3.4/5.4 isolating verbose exploration |
| `.mcp.json` with `${TICKETS_TOKEN}`, `tickets.py` (tool + `tickets://open` resource) | 2.4 project MCP servers, env expansion, MCP resources |
| `shop/utils/dates.py` bug (SHOP-12) and `utcnow()` in 5 files (SHOP-15) | 3.4 direct execution vs plan mode |

## Try it
```bash
export TICKETS_TOKEN=demo-token
claude
```
- `/memory` shows which CLAUDE.md files are loaded.
- "Add a test for an empty invoice": the test follows the rules in `.claude/rules/tests.md`.
- "Fix SHOP-12": a small bug with a clear cause. Use direct execution.
- "Fix SHOP-15 across the codebase": many files and design choices. Start in plan mode (Shift+Tab).
- `/codebase-map shop/billing`: maps the folder in a forked context and returns only a summary.
- `/review`: the team checklist.
- Name a session with `claude -n billing-audit`, continue it later with `claude --resume billing-audit`,
  or branch it with `claude --resume billing-audit --fork-session`.

`./reset.sh` restores the code after a demo run.
