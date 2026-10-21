# Research Crew

This project is a multi-agent research system. Start a job with `/research <topic>`.
The main session is the coordinator: it plans and delegates to the subagents in `.claude/agents/`
(searcher, analyst, synthesizer, reporter), and it never does the searching itself.
Reports go to `reports/`. Files in `docs/` are fictional sample reports used for the demo.
