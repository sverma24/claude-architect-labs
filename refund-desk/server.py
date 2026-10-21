# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=2.3"]
# ///
"""Refund Desk: a fake support backend exposed as MCP tools (local JSON files, no real payments).

The data comes back the way a real legacy backend sends it: Unix timestamps, US-style dates,
numeric status codes and a pile of fields nobody needs. The hooks in .claude/hooks clean that up.
"""
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

DATA = Path(__file__).parent / "data"
mcp = MCPServer("refund-desk")


def load(name):
    return json.loads((DATA / f"{name}.json").read_text())


def fail(category, retryable, message, customer_message=None, **extra):
    """Structured MCP error: isError=true, with a body the agent can act on."""
    body = {"errorCategory": category, "isRetryable": retryable, "message": message}
    if customer_message:
        body["customerMessage"] = customer_message
    body.update(extra)
    raise ToolError(json.dumps(body))


@mcp.tool()
def get_customer(email: str = "", phone: str = "", name: str = "") -> dict:
    """Find and verify a customer. ALWAYS call this first: it returns the verified customer_id that
    every order and refund tool requires.

    Input: an email or phone number (exact match, preferred), or a full name. A name alone can match
    several customers; then this returns status "multiple_matches" and you must ask the customer for
    their email or phone number. Never pick one of the matches yourself.
    Output: {status: "verified", customer: {...}} or {status: "multiple_matches", candidates: n} or
    {status: "not_found"}. Use lookup_order, not this tool, for questions about an order."""
    people = load("customers")
    if email or phone:
        hits = [c for c in people if (email and c["email"] == email.lower().strip()) or (phone and c["phone"] == phone.strip())]
    elif name:
        hits = [c for c in people if c["name"].lower() == name.lower().strip()]
    else:
        fail("validation", False, "Provide an email, phone or full name.")
    if not hits:
        return {"status": "not_found"}
    if len(hits) > 1:
        return {"status": "multiple_matches", "candidates": len(hits), "ask_for": ["email", "phone"]}
    c = hits[0]
    return {"status": "verified", "customer": {"customer_id": c["id"], "name": c["name"], "tier": c["tier"]}}


@mcp.tool()
def lookup_order(customer_id: str, order_id: str) -> dict:
    """Get one order's details: item, total, status and dates. Use this for any question about an
    order ("where is my order", "check ORD-5001", "can I return this").

    Input: the verified customer_id from get_customer, and an order id like "ORD-5001".
    The order must belong to that customer."""
    orders = {o["id"]: o for o in load("orders")}
    o = orders.get(order_id.strip().upper())
    if not o:
        return {"found": False, "order_id": order_id}  # a valid empty result, not an error
    if o["customer_id"] != customer_id:
        fail("permission", False, f"{order_id} does not belong to {customer_id}.",
             "I can only discuss orders on the account you verified.")
    now = datetime.now()
    ordered = now - timedelta(days=o["ordered_days_ago"])
    delivered = now - timedelta(days=o["delivered_days_ago"]) if o["delivered_days_ago"] is not None else None
    return {
        "found": True,
        "order_id": o["id"], "customer_id": o["customer_id"], "item": o["item"],
        "total_cents": int(o["total"] * 100), "currency": "USD",
        "status": o["status_code"],                      # 1 processing, 2 shipped, 3 delivered, 4 returned
        "created_at": int(ordered.timestamp()),          # Unix seconds
        "delivered_on": delivered.strftime("%m/%d/%Y") if delivered else None,  # US date string
        "warehouse_bin": "B-17-04", "picker_id": "pk_88213", "carrier": "UPS",
        "carrier_events": ["label_created", "picked_up", "in_transit", "out_for_delivery", "delivered"][: o["status_code"] + 2],
        "tax_cents": int(o["total"] * 8.5), "promo_code": None, "gift_wrap": False,
        "fulfillment_center": "OAK-2", "fraud_score": 0.02, "internal_notes": "",
    }


@mcp.tool()
def process_refund(customer_id: str, order_id: str, amount: float, reason: str) -> dict:
    """Refund money for a delivered order, in USD. Only for the verified customer's own orders.

    Policy: refunds are allowed within 30 days of delivery, up to the order total.
    Errors come back with errorCategory (validation / business / transient / permission) and
    isRetryable; retry only when isRetryable is true. For business errors, explain customerMessage
    to the customer instead of retrying."""
    orders = {o["id"]: o for o in load("orders")}
    o = orders.get(order_id.strip().upper())
    if not o or o["customer_id"] != customer_id:
        fail("permission", False, f"{order_id} is not an order of {customer_id}.")
    if amount <= 0 or amount > o["total"]:
        fail("validation", False, f"Amount must be between 0 and the order total {o['total']:.2f}.")
    if o["delivered_days_ago"] is None:
        fail("business", False, "Order not delivered yet.",
             "This order hasn't been delivered yet, so it can't be refunded. You can cancel it instead.")
    if o["delivered_days_ago"] > 30:
        fail("business", False, "Outside the 30-day refund window.",
             f"This order was delivered {o['delivered_days_ago']} days ago, past our 30-day refund window.")
    # The payment gateway times out on the first attempt for ORD-5004 (a transient failure to recover from).
    marker = DATA / ".gateway_tried"
    if o["id"] == "ORD-5004" and not marker.exists():
        marker.write_text("1")
        fail("transient", True, "Payment gateway timed out after 10s. Safe to retry once.")
    refund_id = f"RF-{int(time.time()) % 100000:05d}"
    with open(DATA / "refunds.jsonl", "a") as f:
        f.write(json.dumps({"refund_id": refund_id, "order_id": o["id"], "amount": amount, "reason": reason}) + "\n")
    return {"refund_id": refund_id, "order_id": o["id"], "amount": amount, "status": "issued"}


@mcp.tool()
def escalate_to_human(customer_id: str, summary: str, root_cause: str, recommended_action: str,
                      refund_amount: float) -> dict:
    """Hand the case to a human agent. The human can NOT see this conversation, so the summary must
    stand alone: who the customer is, what they asked, what you found, and what you recommend.

    refund_amount is the refund being requested in USD (0 if none).
    Use when: the customer asks for a human, policy doesn't cover the request (e.g. price matching
    a competitor), a refund was blocked by policy, or you can't make progress."""
    ticket = f"ESC-{int(time.time()) % 100000:05d}"
    with open(DATA / "escalations.jsonl", "a") as f:
        f.write(json.dumps({"ticket": ticket, "customer_id": customer_id, "summary": summary, "root_cause": root_cause,
                            "recommended_action": recommended_action, "refund_amount": refund_amount}) + "\n")
    return {"ticket": ticket, "queue": "tier-2", "eta_hours": 4}


if __name__ == "__main__":
    mcp.run()
