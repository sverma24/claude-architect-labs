# Lab B: Research Crew

A coordinator plus four subagents, built only from Claude Code configuration. It runs on a Claude
subscription with no API key. It's the Multi-Agent Research System scenario from the
Claude Certified Architect – Foundations exam guide.

| File | Exam topics |
|---|---|
| `.claude/commands/research.md` (the coordinator) | 1.2 hub and spoke and wide decomposition, 1.3 explicit context and parallel spawns, 1.6 iterative refinement, 5.3 failure handling |
| `.claude/agents/*.md` | 1.3 agent definitions, 2.3 scoped tools per agent (the synthesizer only re-checks facts) |
| searcher/analyst JSON output | 5.1 structured hand-offs, 5.6 claim-source maps, dates, conflicts |
| `archive.py` + `.mcp.json` `${ARCHIVE_DOWN:-0}` | 2.4 env expansion, 2.2/5.3 a transient error vs a valid empty result |
| `docs/` (fictional) | two sources that disagree (62% in 2025 vs 81% in 2026) for 5.6 |

Run it: `claude`, then `/research how companies use AI coding assistants in 2026`.
To simulate an outage: `ARCHIVE_DOWN=1 claude`.
