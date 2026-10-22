# Team Repo exercises

## 1. Personal rule vs project rule (Domain 3)
Add a line to your own `~/.claude/CLAUDE.md` ("Always use pytest fixtures for test data."). Run `/memory` here and
note where it's loaded from. Then move the line into this project's `CLAUDE.md` and run `/memory` again.
*What to look for:* only the project file reaches your teammates when they clone the repo.

## 2. A rule with a paths pattern (Domain 3)
Create `.claude/rules/migrations.md` with a `paths: ["shop/migrations/**"]` header and one convention.
Ask Claude to add a migration, then ask it to edit `shop/cart.py`.
*What to look for:* the rule loads only for files that match the pattern.

## 3. Start without the token (Domain 2)
Unset `TICKETS_TOKEN` and start Claude Code. Ask for open tickets.
*What to look for:* a clear permission error from the server, not an empty list.
