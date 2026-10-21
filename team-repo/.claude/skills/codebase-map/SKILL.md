---
name: codebase-map
description: Map an unfamiliar part of the codebase - entry points, data flow, who calls what - and return a short summary. Use before changing code you haven't read.
argument-hint: [folder to map, e.g. shop/billing]
context: fork
allowed-tools: Read, Grep, Glob
---
Map the folder $ARGUMENTS.

1. Use Glob to list its files, then Grep for its public functions and for who calls them across the repo.
2. Read only the files you need to follow the main flow.
3. Return at most 15 lines:
   - entry points (file:function)
   - the main data flow, in one or two sentences
   - every caller outside the folder (file:line)
   - risks you noticed (deprecated calls, missing tests)

Don't paste file contents. The main conversation only needs the summary.
