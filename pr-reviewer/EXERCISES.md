# PR Reviewer exercises

## 1. Re-review after a fix (Domain 3)
Fix the import in `pr/inventory/orders.py` (use `unit_price`), then run `./review.sh --rerun`.
*What to look for:* the review reports only new or still-open issues, not the one you fixed.

## 2. The vague prompt (Domain 4)
Run `./review.sh --vague` and compare `out/pass/vague.json` with `out/findings.json`.
*What to look for:* which findings the vague prompt misses, and how many style comments it adds.
