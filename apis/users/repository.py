from typing import List, Optional, Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from loguru import logger

class UserNotFoundError(Exception):
    pass

class UserValidationError(Exception):
    pass

class UserRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepository, cls).__new__(cls)
            cls._instance.users = []
            cls._instance._updates_count = 0 
        return cls._instance

    @staticmethod
    def get_argentina_time() -> datetime:
        return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = len(self.users) + 1
        now = self.get_argentina_time().isoformat()
        
        user = {
            "id": user_id,
            **user_data,
            "created_at": now,
            "updated_at": now,
        }
        self.users.append(user)
        logger.info(f"User created: {user}")
        return user

    def list_all(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        active_filters = {k: v for k, v in filters.items() if v is not None}
        
        result = [
            u for u in self.users
            if all(str(u.get(k)) == str(v) for k, v in active_filters.items())
        ]
        return result

    def update(self, user_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        user = next((u for u in self.users if u["id"] == user_id), None)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        for key, value in updates.items():
            if value is not None:
                user[key] = value

        user["updated_at"] = self.get_argentina_time().isoformat()
        self._updates_count += 1
        logger.info(f"User updated: {user}")
        return user
    
    def get_updates_count(self) -> int:
        return self._updates_count
