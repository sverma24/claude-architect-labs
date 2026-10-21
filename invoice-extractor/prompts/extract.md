Extract this invoice or receipt into the JSON schema you were given.

Rules:
- Use only what the document says. If a field isn't in the document, return null. Never guess a value
  to fill a field, and never compute a due date from payment terms that aren't stated.
- Dates are YYYY-MM-DD. "05.10.2026" in a European document is 5 October 2026.
- Amounts are plain numbers in the document's currency. "1.056,13 €" is 1056.13; "two thousand four
  hundred dollars" is 2400.
- Tax shows up as its own line item.
- calculated_total = the sum of the line item amounts. stated_total = the total printed on the document.
  If both exist and differ by more than 0.01, set conflict_detected to true. Report both numbers as they
  are; don't correct either one.
- category: pick one of software, hardware, services or travel when one clearly fits. If the items are
  a mix of categories, use "unclear" and explain the mix in category_detail. If none fits, use "other"
  and say what it is in category_detail.
- field_confidence: 0 to 1 for each field, meaning how sure you are that the value is right. A null
  for a field that is truly absent can have high confidence.

Example (a narrative document):
Document: "Thanks for the photo session on 3 March 2026. That's 350 dollars for the shoot and 50 for
prints. Invoice 44, Lumen Studio."
Result (abridged): vendor "Lumen Studio", invoice_number "44", issue_date null (the session date isn't
the invoice date), due_date null, line_items [{"description": "Photo shoot", "quantity": 1, "amount": 350},
{"description": "Prints", "quantity": 1, "amount": 50}], stated_total null, calculated_total 400,
conflict_detected false, category "services".

Document:
