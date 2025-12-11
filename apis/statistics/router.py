from fastapi import APIRouter, HTTPException
from loguru import logger
import sys
sys.path.append("../../")

from core.publisher import default_publisher_service

router = APIRouter(prefix="/statistics", tags=["statistics"])

publisher = default_publisher_service()

@router.get("/total-users")
def get_total_users():
    try:
        response = publisher.call_rpc(
            event_type="TOTAL_USERS_RPC",
            payload={}
        )

        if not response.get("success"):
            raise HTTPException(status_code=500, detail=response.get("error", "Error getting total users"))
        
        return response.get("data", {})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting total users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/total-updates")
def get_total_updates():
    try:
        response = publisher.call_rpc(
            event_type="TOTAL_UPDATES_RPC",
            payload={}
        )

        if not response.get("success"):
            raise HTTPException(status_code=500, detail=response.get("error", "Error getting total updates"))
        
        return response.get("data", {})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting total updates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/registered-last-24h")
def get_registered_last_24h():
    try:
        response = publisher.call_rpc(
            event_type="REGISTERED_LAST_24_RPC",
            payload={}
        )
        if not response.get("success"):
            raise HTTPException(status_code=500, detail=response.get("error", "Error getting registered users"))
        
        return response.get("data", {})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting registered users in last 24h: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))