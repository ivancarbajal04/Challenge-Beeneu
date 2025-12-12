from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from loguru import logger
from typing import List

class StatisticsRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StatisticsRepository, cls).__new__(cls)
            cls._instance._total_users = 0
            cls._instance._total_updates = 0
            cls._instance._user_registration_timeline = []
        return cls._instance

    @staticmethod
    def get_argentina_time() -> datetime:
        return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))

    def get_total_users(self) -> int:
        return self._total_users

    def get_total_updates(self) -> int:
        return self._total_updates

    def increment_total_users(self) -> None:
        self._total_users += 1
        self._user_registration_timeline.append(self.get_argentina_time())
        logger.info(f"Total users incremented to {self._total_users}")

    def increment_total_updates(self) -> None:
        self._total_updates += 1
        logger.info(f"Total updates incremented to {self._total_updates}")

    def get_registered_last_24h(self) -> int:
        now = self.get_argentina_time()
        cutoff = now - timedelta(hours=24)
        count = sum(1 for timestamp in self._user_registration_timeline if timestamp > cutoff)
        return count
