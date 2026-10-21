"""PostToolUse: remember verified customers, and clean up order data before Claude reads it.

get_customer  -> record the verified customer_id for gate.py
lookup_order  -> Unix timestamps and US dates become ISO dates, status codes become words,
                 and only the fields a support agent needs are kept (the rest is noise in context)
"""
import json
import sys
from datetime import datetime

import state

STATUS = {1: "processing", 2: "shipped", 3: "delivered", 4: "returned"}
KEEP = ["found", "order_id", "customer_id", "item", "total", "status", "ordered_on", "delivered_on", "days_since_delivery"]

call = json.load(sys.stdin)
if __import__("os").environ.get("HOOK_DEBUG"):  # dump what the hook received, to inspect shapes
    (state.DIR.parent / "last_tool_call.json").write_text(json.dumps(call, indent=2))
tool = call["tool_name"].split("__")[-1]
response = call.get("tool_response")


def payload(resp):
    """The tool's JSON result, whether it arrives as structured content or as a text block."""
    if isinstance(resp, dict) and isinstance(resp.get("structuredContent"), dict):
        return resp["structuredContent"]
    blocks = resp if isinstance(resp, list) else (resp or {}).get("content", []) if isinstance(resp, dict) else []
    for b in blocks:
        if isinstance(b, dict) and b.get("type") == "text":
            try:
                return json.loads(b["text"])
            except ValueError:
                pass
    if isinstance(resp, str):
        try:
            return json.loads(resp)
        except ValueError:
            pass
    return None


data = payload(response)
if not isinstance(data, dict):
    sys.exit(0)

if tool == "get_customer" and data.get("status") == "verified":
    s = state.load(call["session_id"])
    cid = data["customer"]["customer_id"]
    if cid not in s["verified"]:
        s["verified"].append(cid)
        state.save(call["session_id"], s)

elif tool == "lookup_order" and data.get("found"):
    today = datetime.now().date()
    data["total"] = f"${data.pop('total_cents') / 100:.2f}"
    data["status"] = STATUS.get(data["status"], f"unknown ({data['status']})")
    data["ordered_on"] = datetime.fromtimestamp(data.pop("created_at")).date().isoformat()
    if data.get("delivered_on"):
        d = datetime.strptime(data["delivered_on"], "%m/%d/%Y").date()
        data["delivered_on"] = d.isoformat()
        data["days_since_delivery"] = (today - d).days
    clean = {k: data[k] for k in KEEP if k in data}
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "updatedMCPToolOutput": [{"type": "text", "text": json.dumps(clean)}],
    }}))
