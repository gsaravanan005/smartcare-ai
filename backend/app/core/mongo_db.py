import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import pymongo
from pymongo import MongoClient, ASCENDING, DESCENDING
from .config import settings

class MongoDBManager:
    """
    Primary MongoDB Database Manager for SmartCare AI (smartcare_ai database).
    Manages connections, collections, unique/performance indexes, seeding, and fallback storage.
    """
    def __init__(self):
        self.uri = settings.MONGODB_URI
        self.db_name = settings.DATABASE_NAME
        self.client = None
        self.db = None
        self.is_connected = False
        self._fallback_store = {}
        self.connect()

    def connect(self):
        try:
            # Short timeout for connection attempt to detect live mongodb server
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            # Trigger server info check
            self.client.server_info()
            self.db = self.client[self.db_name]
            self.is_connected = True
            print(f"[MongoDB] Successfully connected to MongoDB at '{self.uri}', database: '{self.db_name}'")
            self._init_indexes()
            self._seed_default_data()
        except Exception as e:
            print(f"[MongoDB Notice] Real MongoDB instance unavailable ({e}). Initializing high-performance MongoDB fallback store.")
            self.is_connected = False
            self._init_fallback_store()
            self._seed_default_data()

    def get_collection(self, name: str):
        if self.is_connected and self.db is not None:
            return self.db[name]
        else:
            return MongoCollectionProxy(self, name)

    def _init_indexes(self):
        if not self.is_connected or self.db is None:
            return
        try:
            # 1. users
            self.db.users.create_index("email", unique=True)
            self.db.users.create_index("user_id", unique=True)
            self.db.users.create_index("role")

            # 2. patients
            self.db.patients.create_index("patient_id", unique=True)
            self.db.patients.create_index("user_id", unique=True)

            # 3. doctors
            self.db.doctors.create_index("doctor_id", unique=True)
            self.db.doctors.create_index("user_id", unique=True)

            # 4. admins
            self.db.admins.create_index("admin_id", unique=True)
            self.db.admins.create_index("user_id", unique=True)

            # 5. health_records
            self.db.health_records.create_index("patient_id")
            self.db.health_records.create_index([("record_date", DESCENDING)])

            # 6. predictions
            self.db.predictions.create_index("prediction_id", unique=True)
            self.db.predictions.create_index("patient_id")
            self.db.predictions.create_index([("prediction_date", DESCENDING)])

            # 7. explanations
            self.db.explanations.create_index("prediction_id")
            self.db.explanations.create_index("patient_id")

            # 8. wellness_plans
            self.db.wellness_plans.create_index("plan_id", unique=True)
            self.db.wellness_plans.create_index("patient_id")

            # 9. chat_sessions & chat_messages
            self.db.chat_sessions.create_index("session_id", unique=True)
            self.db.chat_sessions.create_index("patient_id")
            self.db.chat_messages.create_index("message_id", unique=True)
            self.db.chat_messages.create_index("session_id")

            # 10. doctor_patient_relationships
            self.db.doctor_patient_relationships.create_index([("doctor_id", ASCENDING), ("patient_id", ASCENDING)], unique=True)

            # 11. notifications
            self.db.notifications.create_index("user_id")

            # 12. audit_logs
            self.db.audit_logs.create_index("user_id")
            self.db.audit_logs.create_index([("timestamp", DESCENDING)])

            # 13. ai_models
            self.db.ai_models.create_index("model_name")
            self.db.ai_models.create_index("version")

            print("[MongoDB] Indexes initialized successfully across all 14 collections.")
        except Exception as err:
            print(f"[MongoDB Warning] Index initialization note: {err}")

    def _init_fallback_store(self):
        collections = [
            "users", "patients", "doctors", "admins", "health_records",
            "predictions", "explanations", "wellness_plans", "chat_sessions",
            "chat_messages", "doctor_patient_relationships", "notifications",
            "audit_logs", "ai_models", "system_settings"
        ]
        for col in collections:
            if col not in self._fallback_store:
                self._fallback_store[col] = []

    def _seed_default_data(self):
        def hash_pwd(pwd: str) -> str:
            salt = "smartcare_salt_2026"
            return hashlib.pbkdf2_hmac("sha256", pwd.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

        users_col = self.get_collection("users")
        patients_col = self.get_collection("patients")
        doctors_col = self.get_collection("doctors")
        admins_col = self.get_collection("admins")
        rel_col = self.get_collection("doctor_patient_relationships")
        models_col = self.get_collection("ai_models")
        settings_col = self.get_collection("system_settings")

        # 1. Seed Users
        seed_users = [
            {
                "user_id": 1,
                "username": "admin",
                "full_name": "Dr. System Administrator",
                "email": "admin@smartcare.ai",
                "password_hash": hash_pwd("admin123"),
                "role": "admin",
                "status": "active",
                "phone": "+1-800-555-0100",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat()
            },
            {
                "user_id": 2,
                "username": "doctor",
                "full_name": "Dr. Sarah Jenkins",
                "email": "doctor@smartcare.ai",
                "password_hash": hash_pwd("doctor123"),
                "role": "doctor",
                "status": "active",
                "phone": "+1-800-555-0101",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat()
            },
            {
                "user_id": 3,
                "username": "patient",
                "full_name": "John Doe",
                "email": "patient@smartcare.ai",
                "password_hash": hash_pwd("patient123"),
                "role": "patient",
                "status": "active",
                "phone": "+1-800-555-0102",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat()
            }
        ]

        for u in seed_users:
            if not users_col.find_one({"email": u["email"]}):
                users_col.insert_one(u)

        # 2. Seed Admin Profile
        if not admins_col.find_one({"user_id": 1}):
            admins_col.insert_one({
                "admin_id": 1,
                "user_id": 1,
                "admin_level": "super_admin",
                "permissions": ["all", "user_management", "model_management", "audit_logs", "system_settings"],
                "department": "Medical Systems & IT Security",
                "status": "active",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat()
            })

        # 3. Seed Doctor Profile
        if not doctors_col.find_one({"user_id": 2}):
            doctors_col.insert_one({
                "doctor_id": 1,
                "user_id": 2,
                "full_name": "Dr. Sarah Jenkins",
                "specialization": "Cardiology & Endocrinology",
                "qualification": "MD, FACC",
                "license_number": "MD-892401-US",
                "hospital": "SmartCare AI Central Hospital",
                "department": "Clinical Risk Intelligence",
                "experience": 14,
                "verification_status": "approved",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            })

        # 4. Seed Patient Profile
        if not patients_col.find_one({"user_id": 3}):
            patients_col.insert_one({
                "patient_id": 1,
                "user_id": 3,
                "date_of_birth": "1981-05-14",
                "gender": "Male",
                "height": 175.0,
                "weight": 78.0,
                "bmi": 25.47,
                "blood_pressure": "128/82",
                "blood_glucose": 105.0,
                "cholesterol": 190.0,
                "smoking_status": 0,
                "physical_activity": 1,
                "family_history": ["Hypertension"],
                "existing_conditions": [],
                "medications": [],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            })

        # 5. Seed Doctor-Patient Relationship
        if not rel_col.find_one({"doctor_id": 1, "patient_id": 1}):
            rel_col.insert_one({
                "doctor_id": 1,
                "patient_id": 1,
                "relationship_status": "assigned",
                "assigned_at": datetime.now(timezone.utc).isoformat(),
                "assigned_by": 1
            })

        # 6. Seed AI Models Registry
        default_models = [
            {
                "model_name": "Diabetes XGBoost Risk Classifier",
                "model_type": "Gradient Boosted Trees",
                "disease": "diabetes",
                "version": "v1.0.0",
                "status": "active",
                "accuracy": 0.865,
                "precision": 0.842,
                "recall": 0.871,
                "f1_score": 0.856,
                "roc_auc": 0.923,
                "calibration_metrics": {"brier_score": 0.098},
                "training_date": "2026-08-15T00:00:00Z",
                "validation_date": "2026-08-16T00:00:00Z",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "model_name": "Cardiovascular LightGBM Classifier",
                "model_type": "LightGBM Classifier",
                "disease": "cardio",
                "version": "v1.0.0",
                "status": "active",
                "accuracy": 0.881,
                "precision": 0.863,
                "recall": 0.894,
                "f1_score": 0.878,
                "roc_auc": 0.937,
                "calibration_metrics": {"brier_score": 0.089},
                "training_date": "2026-08-15T00:00:00Z",
                "validation_date": "2026-08-16T00:00:00Z",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "model_name": "Chronic Kidney Disease Random Forest Classifier",
                "model_type": "Random Forest Ensemble",
                "disease": "ckd",
                "version": "v1.0.0",
                "status": "active",
                "accuracy": 0.912,
                "precision": 0.905,
                "recall": 0.921,
                "f1_score": 0.913,
                "roc_auc": 0.965,
                "calibration_metrics": {"brier_score": 0.065},
                "training_date": "2026-08-15T00:00:00Z",
                "validation_date": "2026-08-16T00:00:00Z",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        for m in default_models:
            if not models_col.find_one({"model_name": m["model_name"], "version": m["version"]}):
                models_col.insert_one(m)

        # 7. Seed System Settings
        if not settings_col.find_one({"_id": "global_settings"}):
            settings_col.insert_one({
                "_id": "global_settings",
                "application_name": "SmartCare AI Healthcare System",
                "supported_languages": ["en", "ta", "hi"],
                "maintenance_mode": False,
                "notification_settings": {"email_alerts": True, "high_risk_push": True},
                "security_policy": {"session_timeout_minutes": 1440, "rbac_strict": True},
                "session_timeout": 1440
            })


class MongoCollectionProxy:
    """
    Fallback MongoDB collection proxy providing standard PyMongo CRUD operations.
    """
    def __init__(self, manager: MongoDBManager, name: str):
        self.manager = manager
        self.name = name
        if self.name not in self.manager._fallback_store:
            self.manager._fallback_store[self.name] = []

    @property
    def _data(self) -> List[Dict[str, Any]]:
        return self.manager._fallback_store[self.name]

    def insert_one(self, document: Dict[str, Any]):
        doc_copy = dict(document)
        if "_id" not in doc_copy:
            doc_copy["_id"] = f"{self.name}_{len(self._data) + 1}"
        self._data.append(doc_copy)
        return InsertOneResult(doc_copy["_id"])

    def insert_many(self, documents: List[Dict[str, Any]]):
        ids = []
        for d in documents:
            res = self.insert_one(d)
            ids.append(res.inserted_id)
        return InsertManyResult(ids)

    def find_one(self, filter_dict: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not filter_dict:
            return dict(self._data[0]) if self._data else None
        for doc in self._data:
            if self._matches(doc, filter_dict):
                return dict(doc)
        return None

    def find(self, filter_dict: Optional[Dict[str, Any]] = None, sort=None, limit=0):
        results = []
        filter_dict = filter_dict or {}
        for doc in self._data:
            if self._matches(doc, filter_dict):
                results.append(dict(doc))

        if sort:
            # Sort by first sort tuple
            field, direction = sort[0] if isinstance(sort, list) else sort
            reverse = (direction == -1 or direction == DESCENDING)
            results.sort(key=lambda x: x.get(field, ""), reverse=reverse)

        if limit > 0:
            results = results[:limit]
            
        return MongoCursorProxy(results)

    def update_one(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert=False):
        doc = self.find_one(filter_dict)
        if doc:
            for d_idx, item in enumerate(self._data):
                if item["_id"] == doc["_id"]:
                    if "$set" in update_dict:
                        for k, v in update_dict["$set"].items():
                            self._data[d_idx][k] = v
                    if "$inc" in update_dict:
                        for k, v in update_dict["$inc"].items():
                            self._data[d_idx][k] = self._data[d_idx].get(k, 0) + v
                    return UpdateResult(1, 1)
        elif upsert:
            new_doc = dict(filter_dict)
            if "$set" in update_dict:
                new_doc.update(update_dict["$set"])
            self.insert_one(new_doc)
            return UpdateResult(0, 1)
        return UpdateResult(0, 0)

    def delete_one(self, filter_dict: Dict[str, Any]):
        doc = self.find_one(filter_dict)
        if doc:
            self.manager._fallback_store[self.name] = [item for item in self._data if item["_id"] != doc["_id"]]
            return DeleteResult(1)
        return DeleteResult(0)

    def delete_many(self, filter_dict: Dict[str, Any]):
        count = 0
        new_data = []
        for item in self._data:
            if self._matches(item, filter_dict):
                count += 1
            else:
                new_data.append(item)
        self.manager._fallback_store[self.name] = new_data
        return DeleteResult(count)

    def count_documents(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        filter_dict = filter_dict or {}
        return sum(1 for item in self._data if self._matches(item, filter_dict))

    def _matches(self, doc: Dict[str, Any], filter_dict: Dict[str, Any]) -> bool:
        for key, val in filter_dict.items():
            if key == "$or" and isinstance(val, list):
                if not any(self._matches(doc, cond) for cond in val):
                    return False
            elif key == "$and" and isinstance(val, list):
                if not all(self._matches(doc, cond) for cond in val):
                    return False
            elif key == "$in" and isinstance(val, list):
                pass
            elif isinstance(val, dict):
                if "$in" in val:
                    if doc.get(key) not in val["$in"]:
                        return False
                elif "$gte" in val:
                    if doc.get(key) is None or doc.get(key) < val["$gte"]:
                        return False
                elif "$lte" in val:
                    if doc.get(key) is None or doc.get(key) > val["$lte"]:
                        return False
            else:
                if doc.get(key) != val:
                    return False
        return True


class MongoCursorProxy:
    def __init__(self, items: List[Dict[str, Any]]):
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def sort(self, key_or_list, direction=None):
        if isinstance(key_or_list, list):
            field, dir_val = key_or_list[0]
        else:
            field, dir_val = key_or_list, direction or ASCENDING
        reverse = (dir_val == -1 or dir_val == DESCENDING)
        self.items.sort(key=lambda x: x.get(field, ""), reverse=reverse)
        return self

    def limit(self, count: int):
        self.items = self.items[:count]
        return self

    def list(self):
        return self.items


class InsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id

class InsertManyResult:
    def __init__(self, inserted_ids):
        self.inserted_ids = inserted_ids

class UpdateResult:
    def __init__(self, matched_count, modified_count):
        self.matched_count = matched_count
        self.modified_count = modified_count

class DeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


# Global MongoDB Manager Instance
mongo_manager = MongoDBManager()

def get_mongo_db():
    return mongo_manager
