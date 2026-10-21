import sqlite3


def get_item(conn: sqlite3.Connection, sku: str):
    row = conn.execute("SELECT sku, name, qty FROM items WHERE sku = ?", (sku,)).fetchone()
    return None if row is None else {"sku": row[0], "name": row[1], "qty": row[2]}
