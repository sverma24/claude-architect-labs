# Claude Certified Architect – Foundations: hands-on labs

These are the working projects from the **Claude Certified Architect – Foundations Full Course** on YouTube.
Every lab is plain Claude Code configuration plus small local Python servers with fake data, so they run on
a normal Claude subscription. They don't need an API key or any sign-up, and no real money or data is involved.

| Lab | Exam scenario | What it shows |
|---|---|---|
| [refund-desk](refund-desk/) | Customer Support Resolution Agent | MCP tools, structured errors, PreToolUse/PostToolUse hooks, escalation rules |
| [research-crew](research-crew/) | Multi-Agent Research System | coordinator + subagents, parallel delegation, error propagation, sources that disagree |

More labs (team Claude Code repo, CI reviewer, data extraction) are added as the course is recorded.

## Requirements
- [Claude Code](https://code.claude.com), signed in
- [uv](https://docs.astral.sh/uv/), which runs the MCP servers and installs their one dependency (`mcp`) on first run
- Python 3.11+

## Run a lab
```bash
cd refund-desk
claude
```
Trust the folder when Claude Code asks, then type one of the demo messages from the lab's README.

These labs teach exam concepts. They're not production code, and the course questions are original,
not real exam questions.
