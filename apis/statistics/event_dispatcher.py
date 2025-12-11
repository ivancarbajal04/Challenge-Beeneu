from loguru import logger
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any

def get_argentina_time() -> datetime:
    return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))

TOTAL_USERS: int = 0
TOTAL_UPDATES: int = 0
REGISTERED_USERS_TIMELINE: list = []

def total_users_rpc(payload: Dict[str, Any]) -> Dict[str, Any]:

    logger.info(f"[StatisticsAPI] Total users requested: {TOTAL_USERS}")

    return {"total_users": TOTAL_USERS}

def total_updates_rpc(payload: Dict[str, Any]) -> Dict[str, Any]:

    logger.info(f"[StatisticsAPI] Total updates requested: {TOTAL_UPDATES}")

    return {"total_updates": TOTAL_UPDATES}

def registered_last_24_rpc(payload: Dict[str, Any]) -> Dict[str, Any]:

    now = get_argentina_time()
    cutoff = now - timedelta(hours=24)
    
    count = sum(1 for timestamp in REGISTERED_USERS_TIMELINE if timestamp > cutoff)

    logger.info(f"[StatisticsAPI] Users registered in last 24h: {count}")

    return {"registered_last_24h": count}

def user_registered_event(payload: Dict[str, Any]) -> None:
    global TOTAL_USERS
    TOTAL_USERS += 1
    
    REGISTERED_USERS_TIMELINE.append(get_argentina_time())

    logger.info(f"[StatisticsAPI] User registered event received: {TOTAL_USERS}")

def user_updated_event(payload: Dict[str, Any]) -> None:
    global TOTAL_UPDATES
    TOTAL_UPDATES += 1

    logger.info(f"[StatisticsAPI] User updated event received: {TOTAL_UPDATES}")


EVENT_HANDLERS = {
    "TOTAL_USERS_RPC": total_users_rpc,
    "TOTAL_UPDATES_RPC": total_updates_rpc,
    "REGISTERED_LAST_24_RPC": registered_last_24_rpc,
    "USER_REGISTERED_EVENT": user_registered_event,
    "USER_UPDATED_EVENT": user_updated_event,
}
