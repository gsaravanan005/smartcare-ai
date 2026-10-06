from datetime import datetime, timezone
from typing import Dict, Any, Optional
from ..core.mongo_db import mongo_manager

class AuditLoggerService:
    """
    MongoDB Audit Logger Service for SmartCare AI.
    Logs sensitive security, authentication, and access events to audit_logs collection.
    Scrubs passwords and secret tokens.
    """
    @staticmethod
    def log_event(
        user_id: Optional[int],
        role: Optional[str],
        action: str,
        resource: str,
        resource_id: Optional[Any] = None,
        ip_address: Optional[str] = "127.0.0.1",
        result: str = "SUCCESS",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        # Scrub sensitive data from metadata
        clean_metadata = {}
        if metadata:
            for k, v in metadata.items():
                if any(secret_kw in k.lower() for secret_kw in ["password", "token", "secret", "hash", "key"]):
                    clean_metadata[k] = "[REDACTED]"
                else:
                    clean_metadata[k] = v

        audit_entry = {
            "user_id": user_id,
            "role": role or "unauthenticated",
            "action": action,
            "resource": resource,
            "resource_id": str(resource_id) if resource_id is not None else None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip_address": ip_address,
            "result": result,
            "metadata": clean_metadata
        }

        audit_col = mongo_manager.get_collection("audit_logs")
        audit_col.insert_one(audit_entry)
        return audit_entry

    @staticmethod
    def get_logs(limit: int = 100, user_id: Optional[int] = None) -> list:
        audit_col = mongo_manager.get_collection("audit_logs")
        query = {}
        if user_id:
            query["user_id"] = user_id
        
        cursor = audit_col.find(query, sort=[("timestamp", -1)], limit=limit)
        logs = []
        for doc in cursor:
            d = dict(doc)
            if "_id" in d:
                d["_id"] = str(d["_id"])
            logs.append(d)
        return logs
