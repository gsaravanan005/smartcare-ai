from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.mongo_db import mongo_manager
from ..core.security import get_current_user
from ..models.models import User, Patient
from ..schemas.schemas import PatientProfileUpdate, PatientProfileResponse
from ..services.audit_service import AuditLoggerService

router = APIRouter(prefix="/patients", tags=["Patient Demographics"])

@router.get("/profile", response_model=PatientProfileResponse)
def get_patient_profile(current_user: Any = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
    patients_col = mongo_manager.get_collection("patients")
    patient_doc = patients_col.find_one({"user_id": user_id})

    if not patient_doc:
        last_patient = list(patients_col.find(sort=[("patient_id", -1)], limit=1))
        next_patient_id = (last_patient[0]["patient_id"] + 1) if last_patient and "patient_id" in last_patient[0] else 100
        now_iso = datetime.now(timezone.utc).isoformat()
        patient_doc = {
            "patient_id": next_patient_id,
            "user_id": user_id,
            "age": None,
            "sex": None,
            "height_cm": None,
            "weight_kg": None,
            "bmi": None,
            "education_level": None,
            "income_level": None,
            "created_at": now_iso,
            "updated_at": now_iso
        }
        patients_col.insert_one(patient_doc)

    # Sync with SQLite for backward compatibility
    patient_sql = db.query(Patient).filter(Patient.user_id == user_id).first()
    if not patient_sql:
        patient_sql = Patient(id=patient_doc.get("patient_id"), user_id=user_id)
        db.add(patient_sql)
        db.commit()

    AuditLoggerService.log_event(
        user_id=user_id,
        role=getattr(current_user, "role", "patient"),
        action="GET_PATIENT_PROFILE",
        resource="patients",
        resource_id=patient_doc.get("patient_id"),
        result="SUCCESS"
    )

    return {
        "id": patient_doc.get("patient_id", 1),
        "user_id": user_id,
        "age": patient_doc.get("age"),
        "sex": patient_doc.get("sex"),
        "height_cm": patient_doc.get("height_cm") or patient_doc.get("height"),
        "weight_kg": patient_doc.get("weight_kg") or patient_doc.get("weight"),
        "bmi": patient_doc.get("bmi"),
        "education_level": patient_doc.get("education_level"),
        "income_level": patient_doc.get("income_level"),
        "created_at": patient_doc.get("created_at"),
        "updated_at": patient_doc.get("updated_at")
    }

@router.put("/profile", response_model=PatientProfileResponse)
def update_patient_profile(
    profile_in: PatientProfileUpdate,
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
    patients_col = mongo_manager.get_collection("patients")
    patient_doc = patients_col.find_one({"user_id": user_id})

    now_iso = datetime.now(timezone.utc).isoformat()
    if not patient_doc:
        last_patient = list(patients_col.find(sort=[("patient_id", -1)], limit=1))
        next_patient_id = (last_patient[0]["patient_id"] + 1) if last_patient and "patient_id" in last_patient[0] else 100
        patient_doc = {"patient_id": next_patient_id, "user_id": user_id, "created_at": now_iso}

    update_fields = {"updated_at": now_iso}
    if profile_in.age is not None: update_fields["age"] = profile_in.age
    if profile_in.sex is not None: update_fields["sex"] = profile_in.sex
    if profile_in.height_cm is not None: update_fields["height_cm"] = profile_in.height_cm; update_fields["height"] = profile_in.height_cm
    if profile_in.weight_kg is not None: update_fields["weight_kg"] = profile_in.weight_kg; update_fields["weight"] = profile_in.weight_kg
    if profile_in.education_level is not None: update_fields["education_level"] = profile_in.education_level
    if profile_in.income_level is not None: update_fields["income_level"] = profile_in.income_level

    # Auto compute BMI
    h_cm = update_fields.get("height_cm", patient_doc.get("height_cm"))
    w_kg = update_fields.get("weight_kg", patient_doc.get("weight_kg"))
    if h_cm and w_kg:
        h_m = h_cm / 100.0
        update_fields["bmi"] = round(w_kg / (h_m ** 2), 2)

    patients_col.update_one({"user_id": user_id}, {"$set": update_fields}, upsert=True)
    updated_doc = patients_col.find_one({"user_id": user_id})

    # Update SQLite
    patient_sql = db.query(Patient).filter(Patient.user_id == user_id).first()
    if patient_sql:
        if profile_in.age is not None: patient_sql.age = profile_in.age
        if profile_in.sex is not None: patient_sql.sex = profile_in.sex
        if profile_in.height_cm is not None: patient_sql.height_cm = profile_in.height_cm
        if profile_in.weight_kg is not None: patient_sql.weight_kg = profile_in.weight_kg
        if updated_doc.get("bmi"): patient_sql.bmi = updated_doc["bmi"]
        db.commit()

    AuditLoggerService.log_event(
        user_id=user_id,
        role=getattr(current_user, "role", "patient"),
        action="UPDATE_PATIENT_PROFILE",
        resource="patients",
        resource_id=updated_doc.get("patient_id"),
        result="SUCCESS"
    )

    return {
        "id": updated_doc.get("patient_id", 1),
        "user_id": user_id,
        "age": updated_doc.get("age"),
        "sex": updated_doc.get("sex"),
        "height_cm": updated_doc.get("height_cm"),
        "weight_kg": updated_doc.get("weight_kg"),
        "bmi": updated_doc.get("bmi"),
        "education_level": updated_doc.get("education_level"),
        "income_level": updated_doc.get("income_level"),
        "created_at": updated_doc.get("created_at"),
        "updated_at": updated_doc.get("updated_at")
    }
