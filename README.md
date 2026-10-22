# Claude Certified Architect – Foundations: hands-on labs

These are the working projects from the **Claude Certified Architect – Foundations Full Course** on YouTube.
Every lab is plain Claude Code configuration plus small local Python servers with fake data, so they run on
a normal Claude subscription. They don't need an API key or any sign-up, and no real money or data is involved.

| Lab | Exam scenario | What it shows |
|---|---|---|
| [refund-desk](refund-desk/) | Customer Support Resolution Agent | MCP tools, structured errors, PreToolUse/PostToolUse hooks, escalation rules |
| [research-crew](research-crew/) | Multi-Agent Research System | coordinator + subagents, parallel delegation, error propagation, sources that disagree |
| [team-repo](team-repo/) | Code Generation with Claude Code / Developer Productivity | CLAUDE.md hierarchy, path rules, commands, skills, MCP resources, plan mode, sessions |
| [pr-reviewer](pr-reviewer/) | Claude Code for Continuous Integration | `claude -p` with a JSON schema, per-file and integration passes, explicit review criteria |
| [invoice-extractor](invoice-extractor/) | Structured Data Extraction | schema design, validation-retry, confidence routing, Batches API walkthrough |



## Requirements
- A Claude subscription (Pro or Max)
- [Claude Code](https://code.claude.com), signed in: `curl -fsSL https://claude.ai/install.sh | bash`, then `claude` and sign in
- git, to download the labs: `git clone https://github.com/sverma24/claude-architect-labs`
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`), which runs the MCP servers and installs their one dependency (`mcp`) on first run
- Python 3.11+

## Run a lab
```bash
cd refund-desk
claude
```
Trust the folder when Claude Code asks, then type one of the demo messages from the lab's README.

## Exercises
Every lab has an `EXERCISES.md`. Predict what will happen before you run each one; that's the part that makes it stick.

## If something goes wrong
| Problem | Fix |
|---|---|
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh`, then open a new terminal. |
| The hooks didn't run, or every tool asks for permission | You skipped the trust prompt. Start `claude` in the lab folder again and choose "Yes, I trust this folder". |
| "MCP server failed" or no refund-desk tools | Run `uv run server.py` once in the lab folder to see the error (usually a missing Python 3.11+). |
| A run behaves differently from the video | Run `./reset.sh` (refund-desk, team-repo) to clear earlier refunds and hook state. |

## Glossary
New to these terms? [GLOSSARY.md](GLOSSARY.md) explains every one in plain words.

These labs teach exam concepts. They're not production code, and the course questions are original,
not real exam questions.
