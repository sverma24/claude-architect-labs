"""PreToolUse gate: deterministic rules the prompt can't guarantee.

1. No order lookup or refund until get_customer has verified that exact customer_id.
2. Refunds above $500 are blocked and sent to a human instead.
"""
import json
import sys

import state

REFUND_LIMIT = 500

call = json.load(sys.stdin)
tool = call["tool_name"].split("__")[-1]
args = call["tool_input"]
verified = state.load(call["session_id"])["verified"]


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    sys.exit(0)


if args.get("customer_id") not in verified:
    deny(f"Blocked by policy: {tool} needs a customer_id verified by get_customer in this conversation. "
         "Call get_customer first, then pass its customer_id to this tool.")
if tool == "process_refund" and float(args.get("amount", 0)) > REFUND_LIMIT:
    deny(f"Blocked by policy: refunds above ${REFUND_LIMIT} need a human. "
         "Call escalate_to_human with the customer id, root cause, refund amount and your recommendation.")
