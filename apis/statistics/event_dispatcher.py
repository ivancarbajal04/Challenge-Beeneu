from loguru import logger
from typing import Dict, Any
import sys

sys.path.append("../../")
from apis.statistics.repository import StatisticsRepository

class EventHandlers:
    def __init__(self, repository: StatisticsRepository):
        self.repo = repository

    def total_users_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        count = self.repo.get_total_users()
        logger.info(f"[StatisticsAPI] Total users requested: {count}")
        return {"total_users": count}

    def total_updates_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        count = self.repo.get_total_updates()
        logger.info(f"[StatisticsAPI] Total updates requested: {count}")
        return {"total_updates": count}

    def registered_last_24_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        count = self.repo.get_registered_last_24h()
        logger.info(f"[StatisticsAPI] Users registered in last 24h: {count}")
        return {"registered_last_24h": count}

    def user_registered_event(self, payload: Dict[str, Any]) -> None:
        self.repo.increment_total_users()
        logger.info(f"[StatisticsAPI] User registered event handled")

    def user_updated_event(self, payload: Dict[str, Any]) -> None:
        self.repo.increment_total_updates()
        logger.info(f"[StatisticsAPI] User updated event handled")

