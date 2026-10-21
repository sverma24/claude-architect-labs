# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=2.3"]
# ///
"""news-archive: a tiny local MCP server with a few archived news items.
Set ARCHIVE_DOWN=1 before starting Claude to simulate the archive timing out."""
import json
import os

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("news-archive")
ITEMS = [
    {"id": "arc-101", "date": "2026-03", "title": "Survey: most developers now use AI assistants weekly",
     "text": "An industry survey of 3,000 developers found 76% use AI coding tools weekly."},
    {"id": "arc-102", "date": "2026-08", "title": "Companies add AI review bots to pull requests",
     "text": "Several large engineering orgs report running AI reviewers on every pull request."},
    {"id": "arc-103", "date": "2025-12", "title": "Security teams warn about AI-written code",
     "text": "Security leads say AI-generated code needs the same review as human code."},
]


@mcp.tool()
def search_archive(query: str) -> dict:
    """Search archived news articles by keyword. Returns matching items (id, date, title, text).
    An empty "items" list means the search worked and nothing matched."""
    if os.environ.get("ARCHIVE_DOWN") == "1":
        raise ToolError(json.dumps({"errorCategory": "transient", "isRetryable": True,
                                    "message": "Archive timed out after 30s", "attempted_query": query}))
    words = [w for w in query.lower().split() if len(w) > 2]
    hits = [i for i in ITEMS if any(w in (i["title"] + " " + i["text"]).lower() for w in words)]
    return {"query": query, "items": hits}


if __name__ == "__main__":
    mcp.run()
