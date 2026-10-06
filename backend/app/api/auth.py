from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.mongo_db import mongo_manager
from ..core.security import hash_password, verify_password, create_access_token, get_current_user
from ..schemas.schemas import UserCreate, UserLogin, Token, UserResponse, ForgotPasswordRequest, ForgotPasswordResponse, LogoutResponse
from ..services.audit_service import AuditLoggerService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, request: Request, db: Session = Depends(get_db)):
    if user_in.role and user_in.role.lower().strip() in ["admin", "super_admin"]:
        AuditLoggerService.log_event(
            user_id=None,
            role="unauthenticated",
            action="PUBLIC_ADMIN_REGISTRATION_FORBIDDEN",
            resource="users",
            ip_address=request.client.host if request.client else "127.0.0.1",
            result="DENIED",
            metadata={"username": user_in.username, "email": user_in.email, "attempted_role": user_in.role}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public administrator registration is restricted. Please contact system administrator."
        )

    # PUBLIC REGISTRATION REQUIREMENT: Self-registration is strictly for PATIENT role
    user_role = "patient"
    effective_username = user_in.username or user_in.email

    users_col = mongo_manager.get_collection("users")
    existing = users_col.find_one({
        "$or": [{"username": effective_username}, {"email": user_in.email}]
    })

    if existing:
        AuditLoggerService.log_event(
            user_id=None,
            role="unauthenticated",
            action="USER_REGISTRATION_FAILED_DUPLICATE",
            resource="users",
            ip_address=request.client.host if request.client else "127.0.0.1",
            result="FAILED",
            metadata={"username": effective_username, "email": user_in.email}
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Determine next user_id
    last_user = list(users_col.find(sort=[("user_id", -1)], limit=1))
    next_user_id = (last_user[0]["user_id"] + 1) if last_user and "user_id" in last_user[0] else 100

    now_iso = datetime.now(timezone.utc).isoformat()
    pwd_hash = hash_password(user_in.password)

    user_doc = {
        "user_id": next_user_id,
        "username": effective_username,
        "email": user_in.email,
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": user_in.full_name or effective_username,
        "role": user_role,
        "status": "active",
        "phone": user_in.phone or "",
        "created_at": now_iso,
        "updated_at": now_iso,
        "last_login": now_iso
    }

    users_col.insert_one(user_doc)

    # Initialize role collection
    if user_role == "patient":
        patients_col = mongo_manager.get_collection("patients")
        last_patient = list(patients_col.find(sort=[("patient_id", -1)], limit=1))
        next_patient_id = (last_patient[0]["patient_id"] + 1) if last_patient and "patient_id" in last_patient[0] else 100

        patients_col.insert_one({
            "patient_id": next_patient_id,
            "user_id": next_user_id,
            "email": user_in.email,
            "full_name": user_in.full_name or effective_username,
            "date_of_birth": getattr(user_in, "date_of_birth", None),
            "gender": getattr(user_in, "gender", None),
            "height": None,
            "weight": None,
            "bmi": None,
            "blood_pressure": None,
            "blood_glucose": None,
            "cholesterol": None,
            "smoking_status": 0,
            "physical_activity": 1,
            "family_history": [],
            "existing_conditions": [],
            "medications": [],
            "created_at": now_iso,
            "updated_at": now_iso
        })
    elif requested_role == "doctor":
        doctors_col = mongo_manager.get_collection("doctors")
        last_doctor = list(doctors_col.find(sort=[("doctor_id", -1)], limit=1))
        next_doctor_id = (last_doctor[0]["doctor_id"] + 1) if last_doctor and "doctor_id" in last_doctor[0] else 100

        doctors_col.insert_one({
            "doctor_id": next_doctor_id,
            "user_id": next_user_id,
            "full_name": user_in.full_name or user_in.username,
            "specialization": "General Medicine",
            "qualification": "MD",
            "license_number": f"LIC-{next_doctor_id:06d}",
            "hospital": "SmartCare AI Hospital",
            "department": "Internal Medicine",
            "experience": 5,
            "verification_status": "pending",
            "created_at": now_iso,
            "updated_at": now_iso
        })

    # Also keep SQLAlchemy User model in sync for legacy compatibility
    try:
        from ..models.models import User, Patient
        existing_sql = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
        if not existing_sql:
            u_sql = User(
                id=next_user_id,
                username=user_in.username,
                email=user_in.email,
                hashed_password=pwd_hash,
                full_name=user_in.full_name,
                role=user_role
            )
            db.add(u_sql)
            db.commit()
            if user_role == "patient":
                p_sql = Patient(id=next_patient_id, user_id=next_user_id)
                db.add(p_sql)
                db.commit()
    except Exception as e:
        print(f"[SQL Sync Warning] {e}")

    AuditLoggerService.log_event(
        user_id=next_user_id,
        role=user_role,
        action="USER_REGISTRATION_SUCCESS",
        resource="users",
        resource_id=next_user_id,
        ip_address=request.client.host if request.client else "127.0.0.1",
        result="SUCCESS",
        metadata={"username": user_in.username, "role": user_role}
    )

    return {
        "id": next_user_id,
        "username": user_in.username,
        "email": user_in.email,
        "full_name": user_in.full_name or user_in.username,
        "role": user_role,
        "created_at": now_iso
    }

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, request: Request, db: Session = Depends(get_db)):
    users_col = mongo_manager.get_collection("users")
    user_doc = users_col.find_one({
        "$or": [{"username": login_in.username}, {"email": login_in.username}]
    })

    user_found = None
    is_mongo = False

    if user_doc:
        pwd_hash = user_doc.get("password_hash") or user_doc.get("hashed_password")
        if verify_password(login_in.password, pwd_hash):
            user_found = user_doc
            is_mongo = True
    else:
        # SQLite Fallback check
        from ..models.models import User
        user_sql = db.query(User).filter((User.username == login_in.username) | (User.email == login_in.username)).first()
        if user_sql and verify_password(login_in.password, user_sql.hashed_password):
            user_found = user_sql
            is_mongo = False

    if not user_found:
        AuditLoggerService.log_event(
            user_id=None,
            role="unauthenticated",
            action="FAILED_LOGIN_ATTEMPT",
            resource="users",
            ip_address=request.client.host if request.client else "127.0.0.1",
            result="DENIED",
            metadata={"identifier": login_in.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/ID or password."
        )

    # Extract fields based on source
    if is_mongo:
        user_id = user_found.get("user_id", user_found.get("id", 1))
        username = user_found.get("username") or user_found.get("email") or login_in.username
        role = (user_found.get("role") or "patient").lower()
        acc_status = (user_found.get("status") or "active").lower()
    else:
        user_id = user_found.id
        username = user_found.username
        role = (user_found.role or "patient").lower()
        acc_status = (getattr(user_found, "status", "active") or "active").lower()

    # 1. Validate Account Status
    if acc_status in ["inactive", "suspended"]:
        AuditLoggerService.log_event(
            user_id=user_id,
            role=role,
            action="LOGIN_BLOCKED_INACTIVE_ACCOUNT",
            resource="users",
            ip_address=request.client.host if request.client else "127.0.0.1",
            result="DENIED",
            metadata={"username": username, "status": acc_status}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently inactive. Please contact support."
        )
    elif acc_status == "pending":
        AuditLoggerService.log_event(
            user_id=user_id,
            role=role,
            action="LOGIN_BLOCKED_PENDING_ACCOUNT",
            resource="users",
            ip_address=request.client.host if request.client else "127.0.0.1",
            result="DENIED",
            metadata={"username": username, "status": acc_status}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is awaiting verification."
        )

    # Check target_role if explicitly requested by caller (e.g. portal-specific login)
    if login_in.target_role:
        req_role = login_in.target_role.lower().strip()
        user_r = role.lower().strip()
        matched = (req_role == user_r) or \
                  (req_role in ["doctor", "clinician"] and user_r in ["doctor", "clinician"]) or \
                  (req_role in ["admin", "super_admin"] and user_r in ["admin", "super_admin"])
        if not matched:
            AuditLoggerService.log_event(
                user_id=user_id,
                role=role,
                action="LOGIN_ROLE_MISMATCH_BLOCKED",
                resource="users",
                ip_address=request.client.host if request.client else "127.0.0.1",
                result="DENIED",
                metadata={"username": username, "actual_role": role, "requested_target_role": login_in.target_role}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this portal."
            )

    # Single Login: User access and role are determined automatically from database record
    # Update last_login
    now_iso = datetime.now(timezone.utc).isoformat()
    if is_mongo and "_id" in user_found:
        users_col.update_one({"_id": user_found["_id"]}, {"$set": {"last_login": now_iso}})
    elif not is_mongo and hasattr(user_found, "last_login"):
        try:
            user_found.last_login = datetime.now(timezone.utc)
            db.commit()
        except Exception:
            pass

    patient_pid = None
    doctor_pid = None

    if role == "patient":
        patients_col = mongo_manager.get_collection("patients")
        p_doc = patients_col.find_one({"$or": [{"user_id": user_id}, {"patient_id": user_id}]})
        if p_doc:
            patient_pid = p_doc.get("patient_id", p_doc.get("id", user_id))
        else:
            patient_pid = user_id
    elif role in ["doctor", "clinician"]:
        doctors_col = mongo_manager.get_collection("doctors")
        d_doc = doctors_col.find_one({"$or": [{"user_id": user_id}, {"doctor_id": user_id}]})
        if d_doc:
            doctor_pid = d_doc.get("doctor_id", d_doc.get("id", user_id))
        else:
            doctor_pid = user_id

    access_token = create_access_token(data={
        "sub": username, 
        "role": role, 
        "user_id": user_id, 
        "patient_profile_id": patient_pid,
        "doctor_profile_id": doctor_pid,
        "status": acc_status
    })

    AuditLoggerService.log_event(
        user_id=user_id,
        role=role,
        action="USER_LOGIN_SUCCESS",
        resource="users",
        resource_id=user_id,
        ip_address=request.client.host if request.client else "127.0.0.1",
        result="SUCCESS",
        metadata={"username": username, "role": role, "patient_profile_id": patient_pid, "doctor_profile_id": doctor_pid}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
        username=username,
        role=role,
        status=acc_status,
        patient_profile_id=patient_pid,
        patient_id=patient_pid,
        doctor_profile_id=doctor_pid,
        doctor_id=doctor_pid
    )

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(req: ForgotPasswordRequest, request: Request):
    # Log attempt without exposing whether email/ID exists
    AuditLoggerService.log_event(
        user_id=None,
        role="unauthenticated",
        action="PASSWORD_RESET_REQUESTED",
        resource="users",
        ip_address=request.client.host if request.client else "127.0.0.1",
        result="SUCCESS",
        metadata={"identifier": req.email_or_id}
    )
    return ForgotPasswordResponse(
        message="If an account with that email or ID exists, password reset instructions have been sent."
    )

@router.post("/logout", response_model=LogoutResponse)
def logout(request: Request, current_user: Any = Depends(get_current_user)):
    user_id = getattr(current_user, "user_id", getattr(current_user, "id", None))
    role = getattr(current_user, "role", "unauthenticated")
    AuditLoggerService.log_event(
        user_id=user_id,
        role=role,
        action="USER_LOGOUT_SUCCESS",
        resource="users",
        ip_address=request.client.host if request.client else "127.0.0.1",
        result="SUCCESS",
        metadata={"user_id": user_id}
    )
    return LogoutResponse(message="Logged out successfully")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: Any = Depends(get_current_user)):
    user_id = getattr(current_user, "user_id", getattr(current_user, "id", None))
    username = getattr(current_user, "username", "user")
    email = getattr(current_user, "email", "user@smartcare.ai")
    full_name = getattr(current_user, "full_name", username)
    role = getattr(current_user, "role", "patient")
    acc_status = getattr(current_user, "status", "active")
    created_at = getattr(current_user, "created_at", datetime.now(timezone.utc).isoformat())
    patient_pid = getattr(current_user, "patient_profile_id", None)
    doctor_pid = getattr(current_user, "doctor_profile_id", None)

    return {
        "id": user_id,
        "user_id": user_id,
        "username": username,
        "email": email,
        "full_name": full_name,
        "role": role,
        "status": acc_status,
        "patient_profile_id": patient_pid,
        "patient_id": patient_pid,
        "doctor_profile_id": doctor_pid,
        "doctor_id": doctor_pid,
        "created_at": created_at
    }
