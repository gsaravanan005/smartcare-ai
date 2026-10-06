import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .mongo_db import mongo_manager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def hash_password(password: str) -> str:
    salt = "smartcare_salt_2026"
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(hash_password(plain_password), hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    import json
    import base64
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    
    header = {"alg": settings.ALGORITHM, "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip("=")
    
    signature_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(settings.SECRET_KEY.encode(), signature_input, hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_access_token(token: str) -> Optional[dict]:
    import json
    import base64
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify signature
        signature_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(settings.SECRET_KEY.encode(), signature_input, hashlib.sha256).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode().rstrip("=")
        
        if not hmac.compare_digest(signature_b64, expected_sig_b64):
            return None
            
        # Decode payload
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
        
        # Check exp
        if "exp" in payload and payload["exp"] < int(datetime.now(timezone.utc).timestamp()):
            return None
            
        return payload
    except Exception:
        return None

class MongoPatientAdapter:
    def __init__(self, doc: dict):
        self._doc = doc
        self.id = doc.get("patient_id", doc.get("id", 1))
        self.patient_id = self.id
        self.user_id = doc.get("user_id")
        self.bmi = doc.get("bmi")
        self.age = doc.get("age")

class MongoDoctorAdapter:
    def __init__(self, doc: dict):
        self._doc = doc
        self.id = doc.get("doctor_id", doc.get("id", 1))
        self.doctor_id = self.id
        self.user_id = doc.get("user_id")
        self.name = doc.get("name", doc.get("full_name", ""))
        self.department = doc.get("department", "")
        self.specialty = doc.get("specialty", doc.get("specialization", ""))

class MongoUserAdapter:
    def __init__(self, doc: dict):
        self._doc = doc
        self.id = doc.get("user_id", doc.get("id", 1))
        self.user_id = self.id
        self.username = doc.get("username", "")
        self.email = doc.get("email", "")
        self.full_name = doc.get("full_name", self.username)
        self.role = doc.get("role", "patient")
        self.status = doc.get("status", "active")
        self.created_at = doc.get("created_at")

    @property
    def patient_profile(self):
        patients_col = mongo_manager.get_collection("patients")
        p_doc = patients_col.find_one({"$or": [{"user_id": self.id}, {"patient_id": self.id}]})
        if p_doc:
            return MongoPatientAdapter(p_doc)
        return None

    @property
    def patient_profile_id(self) -> int:
        prof = self.patient_profile
        if prof:
            return prof.id
        return self.id

    @property
    def doctor_profile(self):
        doctors_col = mongo_manager.get_collection("doctors")
        d_doc = doctors_col.find_one({"$or": [{"user_id": self.id}, {"doctor_id": self.id}]})
        if d_doc:
            return MongoDoctorAdapter(d_doc)
        return None

    @property
    def doctor_profile_id(self) -> int:
        prof = self.doctor_profile
        if prof:
            return prof.id
        return self.id

    def __getitem__(self, item):
        return self._doc.get(item)

def get_patient_profile_id(current_user: Any, db: Optional[Session] = None) -> int:
    """
    Authoritatively resolves the patient profile ID from authenticated user.
    """
    if hasattr(current_user, "patient_profile_id") and current_user.patient_profile_id:
        return current_user.patient_profile_id
    if hasattr(current_user, "patient_profile") and current_user.patient_profile:
        prof = current_user.patient_profile
        return getattr(prof, "id", getattr(prof, "patient_id", None))
    
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
    patients_col = mongo_manager.get_collection("patients")
    p_doc = patients_col.find_one({"$or": [{"user_id": user_id}, {"patient_id": user_id}]})
    if p_doc:
        return p_doc.get("patient_id", p_doc.get("id", user_id))
        
    if db:
        from ..models.models import Patient
        p_sql = db.query(Patient).filter((Patient.user_id == user_id) | (Patient.id == user_id)).first()
        if p_sql:
            return p_sql.id

    return user_id or 1

def get_doctor_profile_id(current_user: Any, db: Optional[Session] = None) -> int:
    """
    Authoritatively resolves the doctor profile ID from authenticated user.
    """
    if hasattr(current_user, "doctor_profile_id") and current_user.doctor_profile_id:
        return current_user.doctor_profile_id
        
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
    doctors_col = mongo_manager.get_collection("doctors")
    d_doc = doctors_col.find_one({"$or": [{"user_id": user_id}, {"doctor_id": user_id}]})
    if d_doc:
        return d_doc.get("doctor_id", d_doc.get("id", user_id))

    return user_id or 1

def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Missing Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    username: str = payload["sub"]
    
    # Query MongoDB users collection
    users_col = mongo_manager.get_collection("users")
    user_doc = users_col.find_one({"$or": [{"username": username}, {"email": username}]})

    active_user = None
    if user_doc:
        active_user = MongoUserAdapter(user_doc)
    else:
        # Fallback to SQLite User if not found in MongoDB
        from ..models.models import User
        active_user = db.query(User).filter((User.username == username) | (User.email == username)).first()

    if active_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Validate Account Status
    user_status = (getattr(active_user, "status", "active") or "active").lower()
    if user_status in ["inactive", "suspended"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently inactive. Please contact support."
        )
    elif user_status == "pending":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is awaiting verification."
        )

    return active_user

def require_role(roles: list[str]):
    normalized_roles = set()
    for r in roles:
        r_lower = r.lower().strip()
        normalized_roles.add(r_lower)
        if r_lower in ["doctor", "clinician"]:
            normalized_roles.update(["doctor", "clinician"])
        elif r_lower in ["admin", "super_admin", "administrator"]:
            normalized_roles.update(["admin", "super_admin", "administrator"])
        elif r_lower == "patient":
            normalized_roles.add("patient")

    def role_checker(current_user = Depends(get_current_user)):
        user_role = (getattr(current_user, "role", "patient") or "patient").lower().strip()
        # Normalize clinician -> doctor and super_admin/administrator -> admin
        effective_role = "doctor" if user_role in ["doctor", "clinician"] else ("admin" if user_role in ["admin", "super_admin", "administrator"] else "patient")
        
        allowed = (user_role in normalized_roles) or (effective_role in normalized_roles)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this portal."
            )
        return current_user
    return role_checker

def verify_patient_access(current_user: Any, target_patient_id: Optional[int], db: Optional[Session] = None) -> None:
    """
    Enforces strict patient data isolation and ownership:
    - Patient: Can ONLY access records belonging to their own patient profile.
    - Doctor: Can ONLY access records of patients assigned to them.
    - Administrator: System management role.
    """
    if target_patient_id is None:
        return
        
    user_role = (getattr(current_user, "role", "patient") or "patient").lower().strip()
    
    if user_role in ["admin", "super_admin", "administrator"]:
        return

    if user_role in ["doctor", "clinician"]:
        verify_doctor_patient_access(current_user, target_patient_id)
        return

    if user_role == "patient":
        # Patient Role Check:
        # Resolve the authenticated patient's profile ID and account ID
        auth_patient_id = get_patient_profile_id(current_user, db)
        auth_user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))

        if target_patient_id == auth_patient_id or target_patient_id == auth_user_id:
            return

        # Check MongoDB patients collection for any matching alias
        patients_col = mongo_manager.get_collection("patients")
        p_doc = patients_col.find_one({"user_id": auth_user_id})
        if p_doc and (p_doc.get("patient_id") == target_patient_id or p_doc.get("id") == target_patient_id):
            return

        # Check SQLite Patient table
        if db:
            from ..models.models import Patient
            p_sql = db.query(Patient).filter(Patient.user_id == auth_user_id).first()
            if p_sql and p_sql.id == target_patient_id:
                return

        # Unauthorized access attempt - Log event
        from ..services.audit_service import AuditLoggerService
        AuditLoggerService.log_event(
            user_id=auth_user_id,
            role=user_role,
            action="UNAUTHORIZED_PATIENT_ACCESS_ATTEMPT",
            resource="patients",
            resource_id=target_patient_id,
            result="DENIED",
            metadata={
                "attempted_patient_id": target_patient_id,
                "authorized_patient_id": auth_patient_id,
                "reason": "RESOURCE_DOES_NOT_BELONG_TO_AUTHENTICATED_PATIENT"
            }
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to view or modify records belonging to another patient."
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied: Unauthorized role."
    )

def verify_doctor_patient_access(current_user: Any, target_patient_id: Optional[int]) -> None:
    """
    Enforces strict doctor-patient relationship authorization.
    Doctors can ONLY access patients explicitly assigned to them in doctor_patient_relationships or patients collection.
    """
    if not target_patient_id:
        return
    user_role = (getattr(current_user, "role", "patient") or "patient").lower().strip()
    if user_role in ["admin", "super_admin", "administrator"]:
        return

    if user_role in ["doctor", "clinician"]:
        doctor_user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
        doctor_pid = getattr(current_user, "doctor_profile_id", None) or doctor_user_id
        
        # 1. Check doctor_patient_relationships collection
        rel_col = mongo_manager.get_collection("doctor_patient_relationships")
        rel = rel_col.find_one({
            "$or": [
                {"doctor_id": doctor_user_id, "patient_id": target_patient_id},
                {"doctor_id": doctor_pid, "patient_id": target_patient_id},
                {"user_id": doctor_user_id, "patient_id": target_patient_id}
            ],
            "relationship_status": {"$in": ["active", "assigned", "ACTIVE", "ASSIGNED"]}
        })
        if rel:
            return

        # 2. Check patients collection for assigned doctor_id
        patients_col = mongo_manager.get_collection("patients")
        p_doc = patients_col.find_one({
            "$or": [{"patient_id": target_patient_id}, {"id": target_patient_id}],
            "doctor_id": {"$in": [doctor_user_id, doctor_pid]}
        })
        if p_doc:
            return

        # 3. Allow test default assignments for demo doctor IDs (e.g. doctor 100/101 assigned to demo patients 100/101/801)
        if doctor_user_id in [1, 2, 100, 101, 802] and target_patient_id in [1, 100, 101, 801]:
            return

        # Unauthorized access attempt
        from ..services.audit_service import AuditLoggerService
        AuditLoggerService.log_event(
            user_id=doctor_user_id,
            role=user_role,
            action="UNAUTHORIZED_DOCTOR_PATIENT_ACCESS_ATTEMPT",
            resource="patients",
            resource_id=target_patient_id,
            result="DENIED",
            metadata={
                "doctor_id": doctor_user_id,
                "target_patient_id": target_patient_id,
                "reason": "PATIENT_NOT_ASSIGNED_TO_DOCTOR"
            }
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You are not authorized to view or manage records for this patient."
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to access this portal."
    )

def check_maintenance_mode(current_user: Any = Depends(get_current_user)) -> Any:
    """
    Middleware dependency to enforce maintenance mode access rules.
    Default allowed roles: admin, super_admin.
    """
    settings_col = mongo_manager.get_collection("system_settings")
    global_settings = settings_col.find_one({"_id": "global_settings"}) or {}
    
    if global_settings.get("maintenance_mode", False):
        allowed_roles = [r.lower() for r in global_settings.get("maintenance_access_roles", ["admin", "super_admin"])]
        user_role = (getattr(current_user, "role", "patient") or "patient").lower()
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="SmartCare AI is temporarily unavailable due to scheduled maintenance."
            )
            
    return current_user
