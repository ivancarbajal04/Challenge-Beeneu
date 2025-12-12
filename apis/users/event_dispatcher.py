from loguru import logger
from typing import Dict, Any, List
from pydantic import ValidationError
import sys

sys.path.append("../../")
from apis.users.schemas import UserCreate, UserUpdate, UserFilter
from apis.users.repository import UserRepository, UserNotFoundError, UserValidationError

class EventHandlers:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    def register_user_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_data = UserCreate(**payload)
            created_user = self.repo.create(user_data.model_dump())
            return created_user
        except ValidationError as e:
            logger.error(f"[UsersAPI] Validation error: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"[UsersAPI] Error in register_user_rpc: {str(e)}")
            return {"error": str(e)}

    def list_users_rpc(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            filters = UserFilter(**payload).model_dump(exclude_unset=True)
            return self.repo.list_all(filters)
        except Exception as e:
            logger.error(f"[UsersAPI] Error listing users: {str(e)}")
            return []

    def update_user_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            update_request = UserUpdate(**payload)
            update_data = update_request.model_dump(exclude_unset=True, exclude={"id"})
            
            updated_user = self.repo.update(update_request.id, update_data)
            return updated_user
        except ValidationError as e:
             logger.error(f"[UsersAPI] Validation error: {str(e)}")
             return {"error": str(e)}
        except UserNotFoundError as e:
            logger.error(f"[UsersAPI] User not found: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"[UsersAPI] Error updating user: {str(e)}")
            return {"error": str(e)}

    def send_email(self, payload: Dict[str, Any]) -> None:
        logger.info(f"[UsersAPI] Sending email to {payload.get('name')} {payload.get('surname')}")