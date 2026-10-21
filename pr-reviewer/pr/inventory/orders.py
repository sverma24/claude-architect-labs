from inventory.pricing import price_for
from inventory.stock import reserve


def place_order(conn, sku: str, qty: int, currency: str = "USD") -> dict:
    if not reserve(conn, sku, qty):
        return {"ok": False, "reason": "out_of_stock"}
    return {"ok": True, "currency": currency, "total_cents": price_for(sku) * qty}
