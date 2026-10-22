# Glossary: every term the course uses, in plain words


| Term | Plain definition | Analogy used in the course | Card | Taught in |
|---|---|---|---|---|
| LLM (large language model) | a program that reads text and predicts the text that should come next | a very well-read colleague who only ever answers in writing | Predicts the next words from what it reads | F1 |
| token | a chunk of text, roughly three quarters of a word, that the model counts and charges by | syllables on a phone bill | A word-piece; the unit models count | F1 |
| context window | everything the model can see in one request: instructions, conversation, tool results | the desk in front of it; anything off the desk doesn't exist | Everything the model can see at once | F1 |
| stateless | the model remembers nothing between requests, so the app resends the conversation each time | a support agent with no ticket history who reads the whole thread fresh | Remembers nothing between calls | F1 |
| prompt | the text you send the model | the brief you hand a contractor | What you send the model | F2 |
| system prompt | standing instructions that sit above every conversation | the team handbook taped to the monitor | Standing instructions for every conversation | F2 |
| messages / roles | the conversation as a list of turns, each marked user or assistant | a ticket thread with who-said-what | The conversation, turn by turn | F2 |
| probabilistic | the same input can give different outputs; instructions make behaviour likely, not certain | a well-trained new hire who follows the handbook almost always | Likely, never guaranteed | F2 |
| deterministic | same input, same result, every time; what ordinary code gives you | a turnstile that only opens for a valid badge | Same input, same result, always | F2 |
| JSON | a plain-text way to write data as named fields and lists | a filled-in form | Data as labelled fields | F3 |
| schema (JSON schema) | the rules for what a JSON document must contain: which fields, what type, what's required | the blank form with required boxes | The rules a JSON answer must follow | F3 |
| null / nullable | a field that's allowed to say "nothing here" | writing N/A instead of inventing an answer | "Nothing here" is allowed | F3 |
| enum | a field that may only hold one of a fixed list of values | a drop-down menu | Pick from a fixed list | F3 |
| tool | a function in your code that the model can ask to run, described by a name, a description and inputs | a request form the model can fill in for your system | A function the model can ask you to run | F4 |
| tool call (tool_use) | the model's request to run a tool, with the inputs filled in | the filled-in request form | The model asking to run a tool | F4 |
| tool result | what your code sends back after running the tool | the reply stapled to the form | What came back from the tool | F4 |
| tool description | the text that tells the model what a tool does and when to use it | the label on a drawer | How the model picks a tool | F4 |
| agent | a model running in a loop, choosing tools until a goal is done | a new hire working a ticket end to end | A model that loops through tools to a goal | F5 |
| agentic loop | send, read the reply, run the tool it asked for, send the result back, repeat until it's done | a chef calling for ingredients until the dish is ready | Ask, run tool, send back, repeat | F5 |
| stop_reason | a label on every reply: tool_use means "run a tool for me", end_turn means "I'm finished" | the status field on a ticket | Why the model stopped this turn | F5 |
| Claude API (Messages API) | sending requests to Claude from your own code; you write the loop yourself | buying the engine and building the car | Raw access; you build the loop | F6 |
| Agent SDK | a library that gives your program the same agent engine Claude Code uses | buying the car's drivetrain, ready to fit | Claude Code's engine, as a library | F6 |
| Claude Code | Anthropic's agent that runs in your terminal, with tools, hooks, subagents and settings built in | the finished car | The ready-made agent in your terminal | F6 |
| harness | the program that runs the loop around the model: tools, permissions, hooks | the car around the engine | The loop and rules around the model | F6 |
| MCP (Model Context Protocol) | a standard way to plug tools and data into any AI app | a USB-C port | A standard plug for AI tools | F7 |
| MCP server | a small program that offers tools (and resources) over MCP | the device you plug in | Offers tools over MCP | F7 |
| MCP client | the AI app that connects to MCP servers and calls their tools | the laptop with the port | Connects to MCP servers | F7 |
| MCP resource | read-only data an MCP server offers, like a catalogue, without a tool call | a reference binder on the shelf | Read-only data from a server | F7 |
| .mcp.json | the project file that lists which MCP servers to start | the list of devices to plug in at startup | Which MCP servers this project uses | F7 |
| git / repository (repo) | the tool and the folder that keep every version of a project's files | shared drive with full version history | A project's files plus their history | F8 |
| commit | one saved change in git, with a message | a saved checkpoint | One saved change | F8 |
| pull request (PR) | a proposed change that teammates review before it's merged | a change request awaiting approval | A change waiting for review | F8 |
| CI (continuous integration) | automation that runs checks on every change before it's merged | an automatic QA gate on every change | Automatic checks on every change | F8 |
| environment variable | a named value the system hands a program at start-up, often used for secrets | a sealed envelope handed over at the door | A setting passed in at start-up | F8 |
| secret / token (credential) | a password-like key; never written into files you share | a building badge | A key you never commit | F8 |
| CLAUDE.md | a file of instructions Claude Code reads at the start of every session | the team handbook | Instructions loaded every session | F9 |
| permissions (allow / deny) | settings that say which tools Claude Code may use without asking | the access list on a badge | Which tools may run | F9 |
| hook | your own script that runs automatically at a set moment, before or after a tool call, and can block or change it | a security guard at the door | Code that checks every action | 1.4–1.5 (first seen in 00) |
| PreToolUse hook | runs before a tool call and can refuse it | guard checking you before you go in | Runs before a tool; can block it | 1.5 |
| PostToolUse hook | runs after a tool returns and can clean the result before the model reads it | a mailroom that tidies letters before delivery | Runs after a tool; can clean results | 1.5 |
| subagent | a separate agent the main one starts for a sub-job; it only knows the brief it's given | a contractor who only sees the brief you hand them | A helper agent with a blank memory | 1.2–1.3 |
| coordinator | the main agent that plans, hands out work to subagents and combines results | a team lead | The agent that plans and delegates | 1.2 |
| hub and spoke | every message between agents goes through the coordinator | every ticket goes through the team lead | All traffic through the coordinator | 1.2 |
| Task tool | the tool a coordinator calls to start a subagent | raising a work order | How a coordinator starts a subagent | 1.3 |
| allowedTools | the list of tools an agent may use | the access list on a badge | Tools this agent may use | 1.3 |
| frontmatter | the settings block at the top of a markdown file, between two lines of dashes | the header on a form | Settings at the top of a file | 1.3 |
| decomposition | breaking a big job into smaller pieces | splitting a project into tickets | Breaking a job into pieces | 1.2, 1.6 |
| prompt chaining | a fixed sequence of steps decided in advance | an assembly line | Fixed steps, planned ahead | 1.6 |
| dynamic decomposition | a plan that changes as you learn | an investigation | A plan that adapts as you learn | 1.6 |
| escalation / handoff | passing a case to a human with a summary that stands on its own | handing a ticket to tier 2 | Passing a case to a human | 1.4 |
| session / resume / fork | one saved conversation; continue it later; or copy it to try another path | a saved game, and a save-as | Continue a chat, or branch it | 1.7 |
| claude -p | running Claude Code once from a script, with no chat | a command, not a conversation | Claude Code run once from a script | F8, 3.6 |
| glob | a file pattern like `**/*.test.py` | a wildcard in a file search | A wildcard file pattern | 3.3 |
| few-shot examples | a handful of worked examples inside the prompt | showing a new hire three finished tickets | Worked examples in the prompt | 4.2 |
| Batches API | send many requests at once, results within a day, at half price | overnight bulk mail | Bulk requests, half price, slower | 4.5 |
| lost in the middle | models use the start and end of a long input best and can miss the middle | remembering the first and last items on a long list | The middle of long inputs gets missed | 5.1 |
| case facts block | a short list of key facts kept at the top of the agent's notes | a sticky note on the ticket | Key facts the agent always carries | 5.1 |
| provenance | where each claim came from, and when | a citation | Where a claim came from | 5.6 |
