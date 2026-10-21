from datetime import datetime

from shop.utils.dates import format_day


def invoice_total(lines):
    """Sum invoice lines. Each line is {"qty": int, "unit_cents": int}."""
    return sum(line["qty"] * line["unit_cents"] for line in lines)


def make_invoice(order_id, lines, paid_at=None):
    return {
        "order_id": order_id,
        "total_cents": invoice_total(lines),
        "issued_at": datetime.utcnow().isoformat(),
        "paid_on": format_day(paid_at),
    }
