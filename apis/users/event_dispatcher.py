from loguru import logger
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any, List

def get_argentina_time() -> datetime:
    return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))

USERS: List[Dict[str, Any]] = []
USER_UPDATES_COUNT: int = 0

def register_user_rpc(payload: Dict[str, Any]) -> Dict[str, Any]:
    user_id = len(USERS) + 1
    user = {
        "id": user_id,
        "name": payload.get("name"),
        "surname": payload.get("surname"),
        "dni": payload.get("dni"),
        "address": payload.get("address"),
        "created_at": get_argentina_time().isoformat(),
        "updated_at": get_argentina_time().isoformat(),
    }
    USERS.append(user)

    logger.info(f"[UsersAPI] User registered: {user}")

    send_email(user)

    return user

def list_users_rpc(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    filters = {k: v for k, v in payload.items() if v is not None}
    result = [
        u for u in USERS
        if all(u.get(k) == v for k, v in filters.items())
    ]

    logger.info(f"[UsersAPI] Listing users with filters {filters}: found {len(result)} users")

    return result

def update_user_rpc(payload: Dict[str, Any]) -> Dict[str, Any]:
    global USER_UPDATES_COUNT
    user_id = payload.get("id")
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        logger.error(f"[UsersAPI] User with id {user_id} not found")
        return {"error": "User not found"}

    for field in ["name", "surname", "dni", "address"]:
        if field in payload:
            user[field] = payload[field]

    user["updated_at"] = get_argentina_time().isoformat()
    USER_UPDATES_COUNT += 1
    logger.info(f"[UsersAPI] User updated: {user}")

    return user

def send_email(payload: Dict[str, Any]) -> None:
    logger.info(f"[UsersAPI] Sending email to {payload.get('name')} {payload.get('surname')}")

EVENT_HANDLERS = {
    "REGISTER_USER_RPC": register_user_rpc,
    "LIST_USERS_RPC": list_users_rpc,
    "UPDATE_USER_RPC": update_user_rpc,
    "SEND_EMAIL": send_email,
}