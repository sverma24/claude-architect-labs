# Lab D: PR Reviewer

Claude Code as an automated reviewer in CI. It's the Claude Code for Continuous Integration scenario from the
Claude Certified Architect – Foundations exam guide. `base/` is the main branch, and `pr/` is a pull request
with planted problems.

| File | Exam topics |
|---|---|
| `review.sh`: `claude -p ... --output-format json --json-schema` | 3.6 non-interactive mode, schema-checked output for PR comments |
| one session per file + an integration pass | 1.6 prompt chaining, 4.6 multi-pass review, independent reviewer instances |
| `prompts/file_review.md` | 4.1 explicit report/skip criteria and severity with examples, 4.2 few-shot format |
| `findings.schema.json` (`detected_pattern`, `confidence`) | 4.3 enums, 4.4 tracking which patterns get dismissed, 4.6 confidence per finding |
| `./review.sh --rerun` | 3.6 re-review after new commits: only new or still-open issues |
| `./review.sh --vague` | 4.1 the same PR with a vague prompt, for comparison |

## The planted problems
| File | Problem | Found by |
|---|---|---|
| `db.py` | SQL built with an f-string (injection) | per-file pass |
| `stock.py` | `<` changed to `<=` (rejects an exact-stock order) | per-file pass |
| `stock.py` | the docstring promises a 500-unit cap that the code doesn't enforce | per-file pass |
| `orders.py` + `pricing.py` | `price_for` renamed to `unit_price`, but orders.py still imports it | integration pass only |
| `orders.py` | the `currency` argument is accepted but never used for the price | integration pass |
| `pricing.py`, `report.py` | style and intentional patterns (camelCase, a TODO, a best-effort `except`) | should be skipped |

In our runs the explicit-criteria review found all five problems and skipped the style bait. The vague prompt
missed the currency bug.

Run it: `./review.sh` (about 45 seconds), then look at `out/findings.json`.
