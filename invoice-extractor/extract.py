# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2"]
# ///
"""Invoice extraction pipeline, run through Claude Code (`claude -p --json-schema`), so no API key is needed.

For each document in docs/:
  1. extract with a strict JSON schema (no syntax errors possible)
  2. validate the MEANING with Pydantic (totals add up, dates are real, a referenced PO was extracted)
  3. on a validation error, retry once with the document, the failed JSON and the exact errors
  4. route to human review: low confidence, conflicting totals, or errors a retry couldn't fix
Then score against labels.json, overall and per document type.

usage: uv run extract.py                     (all documents)
       uv run extract.py inv-04              (documents whose name contains inv-04)
       uv run extract.py inv-01 --simulate-slip
           (demo only: corrupts the first pass's calculated_total, so you can watch the retry fix it)
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ValidationError, model_validator

HERE = Path(__file__).parent
SCHEMA = (HERE / "invoice.schema.json").read_text()
PROMPT = (HERE / "prompts/extract.md").read_text()
CONFIDENCE_FLOOR = 0.7


class Line(BaseModel):
    description: str
    quantity: float
    amount: float


class Invoice(BaseModel):
    vendor: str
    invoice_number: str | None
    issue_date: date | None
    due_date: date | None
    currency: str
    currency_other: str | None
    category: str
    category_detail: str | None
    line_items: list[Line]
    stated_total: float | None
    calculated_total: float
    conflict_detected: bool
    po_number: str | None
    field_confidence: dict[str, float]

    @model_validator(mode="after")
    def semantics(self):
        """Checks a JSON schema can't express. These catch values in the wrong place or that don't add up."""
        errors = []
        line_sum = round(sum(line.amount for line in self.line_items), 2)
        if abs(line_sum - self.calculated_total) > 0.01:
            errors.append(f"calculated_total is {self.calculated_total} but the line items sum to {line_sum}")
        if self.stated_total is not None and abs(self.stated_total - self.calculated_total) > 0.01 \
                and not self.conflict_detected:
            errors.append("stated_total and calculated_total differ, so conflict_detected must be true")
        if self.currency == "other" and not self.currency_other:
            errors.append("currency is 'other', so currency_other must name it")
        if self.category in ("other", "unclear") and not self.category_detail:
            errors.append(f"category is '{self.category}', so category_detail must explain it")
        if self.issue_date and self.due_date and self.due_date < self.issue_date:
            errors.append("due_date is before issue_date")
        if errors:
            raise ValueError("; ".join(errors))
        return self


def claude(prompt: str) -> dict:
    """One non-interactive Claude Code call that must return JSON matching the schema."""
    out = subprocess.run(["claude", "-p", prompt, "--output-format", "json", "--json-schema", SCHEMA, "--tools", ""],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
    return json.loads(out.stdout)["structured_output"]


def check(doc_text: str, data: dict) -> list[str]:
    """Validation errors for one extraction ([] when it passes)."""
    errors = []
    try:
        Invoice.model_validate(data)
    except ValidationError as e:
        errors += [err["msg"].removeprefix("Value error, ") for err in e.errors()]
    # A rule about the source: if the document refers to a PO number, we need it.
    if re.search(r"\bPO\b|purchase order", doc_text, re.I) and not data.get("po_number"):
        errors.append("the document refers to a PO number, but po_number is null")
    return errors


SIMULATE_SLIP = "--simulate-slip" in sys.argv


def process(path: Path) -> dict:
    text = path.read_text()
    data = claude(PROMPT + "\n" + text)
    if SIMULATE_SLIP:
        data["calculated_total"] = round(data["calculated_total"] + 100, 2)  # a deliberate, labeled demo error
    errors = check(text, data)
    log = {"doc": path.name, "first_errors": errors, "retried": False, "retry_fixed": None}
    if errors:
        # Retry with feedback: the document, what came back, and exactly what's wrong with it.
        log["retried"] = True
        retry = claude(PROMPT + "\n" + text + "\n\nYour previous extraction:\n" + json.dumps(data) +
                       "\n\nIt failed these checks:\n- " + "\n- ".join(errors) +
                       "\n\nFix what the document supports. If the information isn't in the document, keep the field null.")
        retry_errors = check(text, retry)
        log["retry_fixed"] = not retry_errors
        data, errors = retry, retry_errors
    low = [f for f, c in data["field_confidence"].items() if c < CONFIDENCE_FLOOR]
    reasons = ([f"low confidence: {', '.join(low)}"] if low else []) + \
              (["totals conflict"] if data["conflict_detected"] else []) + \
              ([f"unresolved: {e}" for e in errors])
    return {**log, "final_errors": errors, "review_reasons": reasons, "extraction": data}


def matches(got, want) -> bool:
    options = want if isinstance(want, list) else [want]
    for w in options:
        if w is None and got is None:
            return True
        if isinstance(w, (int, float)) and isinstance(got, (int, float)) and abs(w - got) < 0.01:
            return True
        if isinstance(w, str) and isinstance(got, str) and w.lower() in got.lower():
            return True
    return False


def score(results: list[dict]) -> None:
    labels = json.loads((HERE / "labels.json").read_text())
    fields = ["vendor", "invoice_number", "issue_date", "due_date", "currency", "category", "stated_total"]
    by_field, by_type, total = {f: [0, 0] for f in fields}, {}, [0, 0]
    for r in results:
        want = labels[r["doc"]]
        t = by_type.setdefault(want["type"], [0, 0])
        for f in fields:
            ok = matches(r["extraction"].get(f), want[f])
            for bucket in (by_field[f], t, total):
                bucket[0] += ok
                bucket[1] += 1
            if not ok:
                print(f"  miss  {r['doc']}  {f}: got {r['extraction'].get(f)!r}, expected {want[f]!r}")
    pct = lambda b: f"{100 * b[0] / b[1]:.0f}% ({b[0]}/{b[1]})"
    print(f"\nOverall field accuracy: {pct(total)}")
    print("By document type: " + ", ".join(f"{k} {pct(v)}" for k, v in by_type.items()))
    print("By field: " + ", ".join(f"{k} {pct(v)}" for k, v in by_field.items()))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pick = args[0] if args else ""
    docs = sorted(p for p in (HERE / "docs").glob("*.txt") if pick in p.name)
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(process, docs))
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, indent=2, default=str))
    review = [{"doc": r["doc"], "reasons": r["review_reasons"]} for r in results if r["review_reasons"]]
    (out / "review_queue.json").write_text(json.dumps(review, indent=2))
    for r in results:
        retry = "" if not r["retried"] else (" | retry fixed it" if r["retry_fixed"] else " | retry did NOT fix it")
        print(f"{r['doc']}: {'needs review' if r['review_reasons'] else 'auto-approved'}{retry}")
        for e in r["first_errors"]:
            print(f"    first pass: {e}")
        for reason in r["review_reasons"]:
            print(f"    review: {reason}")
    print(f"\n{len(review)} of {len(results)} documents go to human review (out/review_queue.json)")
    if not pick:
        score(results)


if __name__ == "__main__":
    main()
