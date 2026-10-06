from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ..core.mongo_db import mongo_manager
from ..core.security import get_current_user
from ..services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["User Notifications"])

def _serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d

@router.get("", response_model=List[Dict[str, Any]])
def get_user_notifications(current_user=Depends(get_current_user)):
    user_id = getattr(current_user, "user_id", getattr(current_user, "id", None))
    notifs_col = mongo_manager.get_collection("notifications")
    cursor = notifs_col.find({"user_id": user_id}).sort("created_at", -1).limit(50)
    return [_serialize(n) for n in cursor]

@router.put("/{notification_id}/read", response_model=Dict[str, Any])
def mark_notification_read(notification_id: str, current_user=Depends(get_current_user)):
    user_id = getattr(current_user, "user_id", getattr(current_user, "id", None))
    notifs_col = mongo_manager.get_collection("notifications")
    result = notifs_col.update_one(
        {"notification_id": notification_id, "user_id": user_id},
        {"$set": {"is_read": True, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "success", "message": "Notification marked as read"}
