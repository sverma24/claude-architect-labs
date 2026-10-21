# Lab E: Invoice Extractor

Structured data extraction from messy documents. It's the Structured Data Extraction scenario from the
Claude Certified Architect – Foundations exam guide. It runs through `claude -p --json-schema` on a
Claude subscription.

| File | Exam topics |
|---|---|
| `invoice.schema.json` | 4.3 schema-enforced output, nullable fields, enums with `other`/`unclear` plus a detail field |
| `prompts/extract.md` | 4.2 a few-shot example for a narrative document, 4.3 normalization rules |
| `extract.py` Pydantic validators | 4.4 semantic checks: totals add up, conflicts flagged, required detail fields |
| `extract.py` retry | 4.4 retry with the document, the failed JSON and the exact errors; one retry is enough |
| `extract.py` review routing | 5.5 field-level confidence, conflicts and unresolved errors go to a human |
| `extract.py` scoring | 5.5 accuracy overall vs per document type and field |
| `batch_walkthrough.py` (shown, not run) | 4.5 Message Batches: custom_id, 24-hour window, resubmitting failures |

## What our runs showed
- `inv-04`: the line items add up to $660, but the invoice says $690, so `conflict_detected` is set and the invoice goes to review.
- `inv-06`: it refers to a PO number that's only on an attachment we don't have. The retry can't invent it,
  so the invoice is flagged "retry did NOT fix it" and sent to a human.
- `--simulate-slip` (demo only) corrupts a total on purpose, and the retry with error feedback fixes it.

Run it: `uv run extract.py` (about 30 seconds for all 8 documents).
