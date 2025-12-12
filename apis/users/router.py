from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from loguru import logger
import sys

sys.path.append("../../")
from core.publisher import default_publisher_service
from apis.users.schemas import UserCreate, UserUpdate, UserFilter

router = APIRouter(prefix="/users", tags=["users"])

publisher = default_publisher_service()

@router.post("/register")
def register_user(user: UserCreate):
    try:
        payload = user.model_dump()
        
        response = publisher.call_rpc(
            event_type="REGISTER_USER_RPC",
            payload=payload
        )
        
        if not response.get("success"):
            error = response.get("error") or response.get("data", {}).get("error", "Error registering user")
            if "validation" in str(error).lower():
                raise HTTPException(status_code=400, detail=str(error))
            raise HTTPException(status_code=500, detail=str(error))
        
        user_data = response.get("data")
        
        try:
            publisher.publish(
                event_type="USER_REGISTERED_EVENT",
                payload=user_data
            )
            
            publisher.publish(
                event_type="SEND_EMAIL",
                payload={"name": user_data["name"], "surname": user_data["surname"]}
            )
        except Exception as e:
            logger.warning(f"Error publishing events: {str(e)}")
        
        return {"status": "success", "user": user_data}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_users(name: Optional[str] = None, surname: Optional[str] = None, dni: Optional[str] = None):
    try:
        payload = {"name": name, "surname": surname, "dni": dni}
        
        response = publisher.call_rpc(
            event_type="LIST_USERS_RPC",
            payload=payload
        )
        
        if not response.get("success"):
            raise HTTPException(status_code=500, detail=str(response.get("error", "Error listing users")))
        
        return {"users": response.get("data", [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
def update_user(user_update: UserUpdate):
    try:
        payload = user_update.model_dump(exclude_unset=True)
        
        response = publisher.call_rpc(
            event_type="UPDATE_USER_RPC",
            payload=payload
        )
        
        if not response.get("success"):
            error_msg = str(response.get("error", "Error updating user"))
            error_data_msg = str(response.get("data", {}).get("error", "")) if response.get("data") else ""
            
            final_error = error_data_msg if error_data_msg else error_msg
            
            if "not found" in final_error.lower():
                raise HTTPException(status_code=404, detail=final_error)
            elif "validation" in final_error.lower():
                raise HTTPException(status_code=400, detail=final_error)
            
            raise HTTPException(status_code=500, detail=final_error)
        
        user_data = response.get("data")
        
        if isinstance(user_data, dict) and "error" in user_data:
            if "not found" in str(user_data["error"]).lower():
                raise HTTPException(status_code=404, detail=user_data["error"])
            if "validation" in str(user_data["error"]).lower():
                 raise HTTPException(status_code=400, detail=user_data["error"])
            raise HTTPException(status_code=400, detail=user_data["error"])
        
        try:
            publisher.publish(
                event_type="USER_UPDATED_EVENT",
                payload=user_data
            )
        except Exception as e:
             logger.warning(f"Error publishing USER_UPDATED_EVENT: {str(e)}")
        
        return {"status": "success", "user": user_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
