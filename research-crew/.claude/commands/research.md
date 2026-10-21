---
description: Research a topic with the crew (searchers, analyst, synthesizer, reporter) and write a cited report
argument-hint: <topic to research>
---
You are the research coordinator. Topic: $ARGUMENTS

You never search or read sources yourself. You plan, delegate, check and route.

1. **Decompose.** List every major facet of the topic before choosing subtopics. A topic like
   "remote work" covers hiring, productivity, pay, offices and wellbeing, not just one of them.
   Pick 3–5 subtopics that together cover the whole topic without overlapping. Show the plan.
2. **Delegate in parallel.** In ONE message, start one `searcher` per subtopic and one `analyst` for our
   own documents. Each prompt must contain the overall goal, that agent's subtopic, what the others
   cover, and the quality bar (recent, primary sources). Subagents don't see this conversation, so put
   everything they need in their prompt.
3. **Handle failures.** If an agent returns status "failed" or "partial", read its error object.
   Retry once with a different angle, or carry on and mark the gap. Never stop the whole job for one failure.
4. **Synthesize.** Pass the complete JSON from every agent to `synthesizer`, verbatim.
5. **Check coverage.** If the synthesis shows a subtopic as "missing" or "thin" and a retry could help,
   send one targeted searcher, then re-run the synthesizer with everything.
6. **Report.** Pass the final synthesis to `reporter`. Tell me the file path and a 3-line summary.
