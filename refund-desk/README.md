# Lab A: Refund Desk

A customer-support agent built from Claude Code configuration only, with fake local data. There are no
API keys or accounts, and no real money moves. It's the Customer Support Resolution Agent scenario from
the Claude Certified Architect – Foundations exam guide.

| File | Exam topics |
|---|---|
| `server.py`: MCP tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human` | 2.1 tool descriptions, 2.2 structured errors (`errorCategory`, `isRetryable`), access failure vs empty result |
| `.claude/hooks/gate.py` (PreToolUse) | 1.4 programmatic prerequisites, 1.5 blocking refunds over $500 |
| `.claude/hooks/after_tool.py` (PostToolUse) | 1.5 normalizing dates and status codes, 5.1 trimming tool output |
| `CLAUDE.md` | 1.4 decomposition, 5.1 case facts, 5.2 escalation criteria with examples |
| `.mcp.json`, `.claude/settings.json` | 2.4 project-scoped MCP servers, scoped tool permissions |

Run it from this folder: `claude` (you'll be asked to trust the folder once). `./reset.sh` clears refunds,
escalations and hook state between runs. To show the same agent without its hooks (prompt-only
enforcement), run `claude --settings '{"disableAllHooks": true}'`.

## Demo messages
| Message | What should happen |
|---|---|
| "I'm Priya Shah, priya.shah@example.com. My headphones ORD-5001 arrived broken, refund please." | verify, look up the order, refund $89 |
| "Refund my laptop ORD-5002, it's priya.shah@example.com." | the hook blocks the $1,249 refund; the agent escalates with a handoff summary |
| "Hi, I'm Alex Morgan, where's my order?" | multiple matches; the agent asks for an email or phone |
| "dan.okafor@example.com: refund my shoes ORD-5003 and my lamp ORD-5004." | shoes: business error, past 30 days; lamp: transient error, retried once, then refunded |
| "Check order ORD-5001 for me" (no identity given) | lookup is blocked until the agent verifies the customer |
| "I'm Dan, dan.okafor@example.com. Amazon sells the lamp $20 cheaper, match it." | policy gap, so the agent escalates |
| "Just get me a human." | immediate escalation |
