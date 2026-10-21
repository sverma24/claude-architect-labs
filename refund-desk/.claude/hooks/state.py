"""Per-session memory for the hooks: which customer ids get_customer has verified."""
import json
import os
from pathlib import Path

DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / ".claude" / "state"


def load(session_id):
    p = DIR / f"{session_id}.json"
    return json.loads(p.read_text()) if p.exists() else {"verified": []}


def save(session_id, state):
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / f"{session_id}.json").write_text(json.dumps(state))
