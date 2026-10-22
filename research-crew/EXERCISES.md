# Research Crew exercises

A full run takes about 15 minutes of your subscription's usage, so try one exercise per sitting.

## 1. Break the coordinator's planning step (Domain 1)
In `.claude/commands/research.md`, delete step 1 (listing the facets of the topic before choosing subtopics).
Run `/research how companies use AI coding assistants in 2026`.
**Predict:** how many subtopics does it pick now?
*What to look for:* the report covers less of the topic, and the coverage section has nothing to say about what's missing.

## 2. Run with the archive switched off (Domain 5)
Start with `ARCHIVE_DOWN=1 claude` and run the same research command.
*What to look for:* the analyst returns an error object with the queries it tried, and the report's coverage
section says which part is missing instead of pretending the archive was empty.

## 3. Find the conflict (Domain 5)
Read `docs/` yourself first: one source says 62% (2025), the other 81% (2026).
*What to look for:* the report keeps both numbers with their dates and sources rather than picking one.
