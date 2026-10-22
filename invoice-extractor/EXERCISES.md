# Invoice Extractor exercises

## 1. Make the due date required (Domain 4)
In `invoice.schema.json`, change `due_date` to `{"type": "string"}`. Run `uv run extract.py` and open the
result for `inv-05-no-due.txt`.
**Predict:** what due date does it get?
*What to look for:* a date that isn't in the document. Put the null back afterwards.

## 2. A retry that can't work (Domain 4)
Add an invoice that says "PO number: see attached purchase order" with no attachment. Run the extractor.
*What to look for:* the retry correctly fails and the invoice goes to review. A retry can't create information the
document doesn't contain.

## 3. Find the weak spot (Domain 5)
Break the scores in `out/results.json` down by document type (table, email, receipt).
*What to look for:* a good overall average can hide one type that's much worse.
