from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from loguru import logger
import sys
sys.path.append("../../")

from core.publisher import default_publisher_service

router = APIRouter(prefix="/users", tags=["users"])

publisher = default_publisher_service()

@router.post("/register")
def register_user(payload: Dict[str, Any] = Body(...)):
    try:
        response = publisher.call_rpc(
            event_type="REGISTER_USER_RPC",
            payload=payload
        )
        
        if not response.get("success"):
            raise HTTPException(status_code=500, detail=response.get("error", "Error registering user"))
        
        user_data = response.get("data")
        
        publisher.publish(
            event_type="USER_REGISTERED_EVENT",
            payload=user_data
        )
        
        return {"status": "success", "user": user_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def list_users(name: Optional[str] = None, surname: Optional[str] = None, dni: Optional[str] = None):
    try:
        payload = {"name": name, "surname": surname, "dni": dni}
        
        response = publisher.call_rpc(
            event_type="LIST_USERS_RPC",
            payload=payload
        )
        
        if not response.get("success"):
            raise HTTPException(status_code=500, detail=response.get("error", "Error listing users"))
        
        return {"users": response.get("data", [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
def update_user(payload: Dict[str, Any] = Body(...)):
    try:
        if "id" not in payload:
            raise HTTPException(status_code=400, detail="Field 'id' is required")
        
        response = publisher.call_rpc(
            event_type="UPDATE_USER_RPC",
            payload=payload
        )
        
        if not response.get("success"):
            error_msg = response.get("error", "Error updating user")
            raise HTTPException(status_code=500, detail=error_msg)
        
        user_data = response.get("data")
        
        if isinstance(user_data, dict) and "error" in user_data:
            raise HTTPException(status_code=404, detail=user_data["error"])
        
        publisher.publish(
            event_type="USER_UPDATED_EVENT",
            payload=user_data
        )
        
        return {"status": "success", "user": user_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))