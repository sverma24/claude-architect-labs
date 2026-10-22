# Refund Desk exercises

Run `./reset.sh` before each exercise. Predict the result first, write it down, then run it.

## 1. Change the refund limit to $300
Open `.claude/hooks/gate.py` and change `REFUND_LIMIT = 500` to `300`.
**Predict:** what happens to a $350 refund? Then ask the bot to refund a $350 order and check.
*What to look for:* the hook blocks the call and the bot escalates. Nothing in CLAUDE.md changed, so the rule
lives only in code. Put the limit back to 500 afterwards.

## 2. Run the bot with its hooks switched off
Start it with `claude --settings '{"disableAllHooks": true}'` and send the laptop message from the README
("Refund my laptop ORD-5002, it's priya.shah@example.com.").
**Predict:** does the $1,249 refund go through? Run it a few times.
*What to look for:* with only the instructions in CLAUDE.md, nothing stops the refund. That's the difference
between a prompt (likely) and a hook (every time).

## 3. Make the get_customer description vague (Domain 2)
In `server.py`, replace the `get_customer` docstring with `"""Gets customer info."""` and restart Claude Code.
**Predict:** what does the bot call when someone asks "where is my order ORD-5001"?
*What to look for:* without "use lookup_order, not this tool, for questions about an order", tool choice gets worse.

## 4. Turn a business error into a generic one (Domain 2)
In `process_refund`, change the 30-day `fail("business", ...)` call to `fail("transient", True, "Operation failed.")`.
**Predict:** what does the bot do with Dan's shoes (ORD-5003)?
*What to look for:* it retries a refund it should be explaining. Error categories decide what the agent does next.

## 5. Remove the case facts step (Domain 5)
Delete step 3 ("Keep a case facts block…") from CLAUDE.md. Then have a long conversation about Dan's two orders
and ask about the first one again at the end.
*What to look for:* amounts and dates drift as the conversation gets longer.
