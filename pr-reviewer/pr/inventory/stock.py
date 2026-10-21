from inventory.db import get_item


def reserve(conn, sku: str, qty: int) -> bool:
    """Reserve qty units. Returns False when there isn't enough stock."""
    item = get_item(conn, sku)
    if item is None or item["qty"] <= qty:
        return False
    conn.execute("UPDATE items SET qty = qty - ? WHERE sku = ?", (qty, sku))
    return True


def release(conn, sku: str, qty: int) -> None:
    """Give reserved units back. Caps stock at the shelf limit of 500 units."""
    conn.execute("UPDATE items SET qty = qty + ? WHERE sku = ?", (qty, sku))
