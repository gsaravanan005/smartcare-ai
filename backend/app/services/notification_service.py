from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from ..core.mongo_db import mongo_manager

class NotificationService:
    """
    MongoDB Notification Service for SmartCare AI.
    Dispatches and retrieves notifications (info, warning, high_risk, system, security).
    """
    @staticmethod
    def create_notification(
        user_id: int,
        type: str, # info, warning, high_risk, system, security
        title: str,
        message: str,
        priority: str = "Medium" # Low, Medium, High, Critical
    ) -> Dict[str, Any]:
        
        notif_entry = {
            "notification_id": f"NOTIF_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:17]}",
            "user_id": user_id,
            "type": type,
            "title": title,
            "message": message,
            "priority": priority,
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        notif_col = mongo_manager.get_collection("notifications")
        notif_col.insert_one(notif_entry)
        return notif_entry

    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False, limit: int = 50) -> List[Dict[str, Any]]:
        notif_col = mongo_manager.get_collection("notifications")
        query = {"user_id": user_id}
        if unread_only:
            query["is_read"] = False
        
        cursor = notif_col.find(query, sort=[("created_at", -1)], limit=limit)
        return [doc for doc in cursor]

    @staticmethod
    def mark_as_read(notification_id: str, user_id: int) -> bool:
        notif_col = mongo_manager.get_collection("notifications")
        res = notif_col.update_one(
            {"notification_id": notification_id, "user_id": user_id},
            {"$set": {"is_read": True}}
        )
        return res.modified_count > 0
