from datetime import datetime

ORDERS = {"ORD-1": {"id": "ORD-1", "user_id": "u1", "created_at": datetime.utcnow(), "status": "paid"}}


def get_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"data": None, "error": {"code": "not_found", "message": f"No order {order_id}"}}
    return {"data": order, "error": None}


def cancel_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"data": None, "error": {"code": "not_found", "message": f"No order {order_id}"}}
    order["status"] = "cancelled"
    order["cancelled_at"] = datetime.utcnow()
    return {"data": order, "error": None}
