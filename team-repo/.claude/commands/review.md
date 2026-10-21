---
description: Review the current changes against the team checklist
argument-hint: [file or folder, default: all changed files]
---
Review $ARGUMENTS (or every file changed since the last commit if no argument is given) against this checklist.
Report only real problems, as a list of `file:line, problem, fix`. Skip style nits.

1. API handlers return the data/error envelope and never raise.
2. Money is integer cents; no floats.
3. Datetimes are timezone-aware UTC.
4. New behavior has tests that follow the test conventions.
5. No secrets or tokens in code or config.
