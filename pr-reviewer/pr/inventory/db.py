import sqlite3


def get_item(conn: sqlite3.Connection, sku: str):
    row = conn.execute("SELECT sku, name, qty FROM items WHERE sku = ?", (sku,)).fetchone()
    return None if row is None else {"sku": row[0], "name": row[1], "qty": row[2]}


def search_items(conn: sqlite3.Connection, term: str):
    # Search by name for the admin screen
    rows = conn.execute(f"SELECT sku, name, qty FROM items WHERE name LIKE '%{term}%'").fetchall()
    return [{"sku": r[0], "name": r[1], "qty": r[2]} for r in rows]
