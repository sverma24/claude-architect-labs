from datetime import datetime

USERS = {"u1": {"id": "u1", "name": "Priya", "joined_at": datetime.utcnow()}}


def get_user(user_id):
    user = USERS.get(user_id)
    if user is None:
        return {"data": None, "error": {"code": "not_found", "message": f"No user {user_id}"}}
    return {"data": user, "error": None}
