# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=2.3"]
# ///
"""tickets: a tiny local issue tracker exposed over MCP (fake data).

It needs TICKETS_TOKEN in its environment, the way a real Jira or Linear server needs an API token.
.mcp.json passes it in with ${TICKETS_TOKEN}, so the token itself never lands in the repo.
"""
import json
import os

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("tickets")
TICKETS = {
    "SHOP-12": {"title": "Receipt crashes when an order has no payment date", "status": "open", "area": "billing",
                "details": "make_invoice(order, lines, paid_at=None) raises AttributeError in format_day."},
    "SHOP-15": {"title": "Migrate off datetime.utcnow()", "status": "open", "area": "all",
                "details": "utcnow() is deprecated and returns naive datetimes. Move every call to timezone-aware UTC."},
    "SHOP-9": {"title": "Add invalid_input errors to API handlers", "status": "done", "area": "api", "details": ""},
}


def check_token():
    if not os.environ.get("TICKETS_TOKEN"):
        raise ToolError(json.dumps({"errorCategory": "permission", "isRetryable": False,
                                    "message": "TICKETS_TOKEN is not set. Export it before starting Claude Code."}))


@mcp.resource("tickets://open", name="open-tickets", description="Catalog of every open ticket: id, title, area.",
              mime_type="application/json")
def open_tickets() -> str:
    """The catalog: lets the agent see what exists without calling a tool for each ticket."""
    return json.dumps([{"id": k, "title": v["title"], "area": v["area"]} for k, v in TICKETS.items() if v["status"] == "open"])


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Get one ticket's full details (title, status, area, details) by id, e.g. "SHOP-12".
    To see which tickets exist, read the tickets://open resource instead of guessing ids."""
    check_token()
    t = TICKETS.get(ticket_id.strip().upper())
    return {"found": False, "ticket_id": ticket_id} if t is None else {"found": True, "id": ticket_id.upper(), **t}


if __name__ == "__main__":
    mcp.run()
