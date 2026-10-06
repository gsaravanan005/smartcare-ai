"""
SmartCare AI - Module 5 Risk Monitoring & Clinical Decision Support API Router
Exposes REST endpoints for patient risk history, risk trends, clinical alerts, and clinician portal workflows.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from ..core.database import get_db
from ..core.mongo_db import mongo_manager
from ..core.security import get_current_user, require_role, verify_patient_access
from ..models.models import User, Patient, ClinicalAlert, ClinicianFeedback
from ..schemas.schemas import ClinicalAlertResponse, AlertUpdate, RiskTrendResponse, ClinicianDashboardResponse, ClinicianFeedbackCreate, ClinicianFeedbackResponse
from ..services.risk_monitoring_service import RiskMonitoringService

router = APIRouter(tags=["Module 5 — Risk Monitoring & Clinical Decision Support"])

# -------------------------------------------------------------
# 1. PATIENT RISK HISTORY & TRENDS ENDPOINTS
# -------------------------------------------------------------

@router.get("/risk-history/{patient_id}", response_model=List[Dict[str, Any]])
def get_patient_risk_history(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves chronological risk assessment history for a specified patient ID.
    Enforces strict patient data isolation.
    """
    verify_patient_access(current_user, patient_id, db)
    history = RiskMonitoringService.get_patient_risk_history(db, patient_id)
    return history

@router.get("/risk-history/{patient_id}/trends", response_model=RiskTrendResponse)
def get_patient_risk_trends(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculates current vs previous risk scores and percentage point differences with safe clinical wording.
    Enforces strict patient data isolation.
    """
    verify_patient_access(current_user, patient_id, db)
    trends = RiskMonitoringService.calculate_risk_trends(db, patient_id)
    return trends

@router.get("/assessments/{assessment_id}", response_model=Dict[str, Any])
def get_assessment_details(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves complete assessment details (predictions, SHAP factors, recommendations, alerts, feedback).
    """
    details = RiskMonitoringService.get_assessment_details(db, assessment_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"Assessment '{assessment_id}' not found.")
    
    # Verify access to this assessment's patient
    if details.get("patient_id"):
        verify_patient_access(current_user, details["patient_id"], db)

    return details

@router.get("/alerts/{patient_id}", response_model=List[ClinicalAlertResponse])
def get_patient_alerts(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves clinical alerts for a patient.
    """
    verify_patient_access(current_user, patient_id, db)
    alerts = db.query(ClinicalAlert).filter(ClinicalAlert.patient_id == patient_id).order_by(ClinicalAlert.created_at.desc()).all()
    return alerts

@router.put("/alerts/{alert_id}", response_model=ClinicalAlertResponse)
def update_alert_status(
    alert_id: int,
    alert_in: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates status of a clinical alert (OPEN -> REVIEWED / RESOLVED).
    Accessible by clinicians and admins.
    """
    if current_user.role not in ["admin", "clinician", "doctor"]:
        raise HTTPException(status_code=403, detail="Clinician or Admin authorization required.")

    alert = db.query(ClinicalAlert).filter(ClinicalAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")

    alert.status = alert_in.status
    alert.reviewed_at = datetime.now(timezone.utc)
    alert.reviewed_by = current_user.full_name or current_user.username

    db.commit()
    db.refresh(alert)
    return alert

# -------------------------------------------------------------
# 2. CLINICIAN PORTAL ENDPOINTS
# -------------------------------------------------------------

@router.get("/clinician/dashboard", response_model=ClinicianDashboardResponse)
def get_clinician_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns clinician dashboard statistics, total patient counts, open alerts, and clinical reviews required.
    Accessible by clinicians and admins.
    """
    if current_user.role not in ["admin", "clinician", "doctor"]:
        raise HTTPException(status_code=403, detail="Clinician or Admin authorization required.")

    metrics = RiskMonitoringService.get_clinician_dashboard_metrics(db)
    return metrics

@router.get("/clinician/patients", response_model=List[Dict[str, Any]])
def get_clinician_patient_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns authorized patient roster with latest risk scores and alert status for clinician view.
    """
    user_role = (getattr(current_user, "role", "patient") or "patient").lower()
    if user_role not in ["admin", "super_admin", "clinician", "doctor"]:
        raise HTTPException(status_code=403, detail="Clinician or Admin authorization required.")

    is_admin = user_role in ["admin", "super_admin"]
    doctor_id = getattr(current_user, "doctor_profile_id", None) or getattr(current_user, "id", None)

    roster = RiskMonitoringService.get_clinician_patient_list(db, doctor_id=doctor_id, is_admin=is_admin)
    return roster

@router.get("/clinician/patients/{patient_id}", response_model=Dict[str, Any])
def get_clinician_patient_detail(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns comprehensive clinician view of a specific patient (profile, history, trends, SHAP summary, recommendations, alerts, feedback log).
    """
    user_role = (getattr(current_user, "role", "patient") or "patient").lower()
    if user_role not in ["admin", "super_admin", "clinician", "doctor"]:
        raise HTTPException(status_code=403, detail="Clinician or Admin authorization required.")

    verify_patient_access(current_user, patient_id, db)

    # 1. Look up patient in SQLite or MongoDB
    patient = db.query(Patient).filter((Patient.id == patient_id) | (Patient.user_id == patient_id)).first()
    
    patients_col = mongo_manager.get_collection("patients")
    users_col = mongo_manager.get_collection("users")
    p_mongo = patients_col.find_one({"$or": [{"patient_id": patient_id}, {"id": patient_id}, {"user_id": patient_id}]})

    if not patient and not p_mongo:
        raise HTTPException(status_code=404, detail=f"Patient #{patient_id} not found.")

    # Resolve patient metadata
    p_id = (p_mongo.get("patient_id") or p_mongo.get("id")) if p_mongo else patient.id
    user_id_val = p_mongo.get("user_id") if p_mongo else patient.user_id

    u_doc = users_col.find_one({"$or": [{"user_id": user_id_val}, {"id": user_id_val}]}) if user_id_val else None
    u_sql = db.query(User).filter(User.id == user_id_val).first() if user_id_val else None

    patient_name = (
        (u_doc.get("full_name") or u_doc.get("username")) if u_doc
        else ((u_sql.full_name or u_sql.username) if u_sql
        else (p_mongo.get("full_name") if p_mongo else f"Patient #{p_id}"))
    )
    patient_email = (u_doc.get("email") if u_doc else (u_sql.email if u_sql else (p_mongo.get("email", "") if p_mongo else "")))

    age_val = (p_mongo.get("age") if p_mongo and "age" in p_mongo else (patient.age if patient else 45))
    sex_raw = (p_mongo.get("gender") or p_mongo.get("sex")) if p_mongo else (patient.sex if patient else "N/A")
    sex_str = "Male" if str(sex_raw) in ["1", "Male", "male", "M"] else ("Female" if str(sex_raw) in ["0", "Female", "female", "F"] else "N/A")

    height_val = (p_mongo.get("height") or p_mongo.get("height_cm")) if p_mongo else (patient.height_cm if patient else 170.0)
    weight_val = (p_mongo.get("weight") or p_mongo.get("weight_kg")) if p_mongo else (patient.weight_kg if patient else 70.0)
    bmi_val = p_mongo.get("bmi") if p_mongo else (patient.bmi if patient else 24.5)

    history = RiskMonitoringService.get_patient_risk_history(db, p_id)
    trends = RiskMonitoringService.calculate_risk_trends(db, p_id)
    alerts = db.query(ClinicalAlert).filter((ClinicalAlert.patient_id == p_id) | (ClinicalAlert.patient_id == user_id_val)).order_by(ClinicalAlert.created_at.desc()).all()
    feedbacks = db.query(ClinicianFeedback).filter((ClinicianFeedback.patient_id == p_id) | (ClinicianFeedback.patient_id == user_id_val)).order_by(ClinicianFeedback.created_at.desc()).all()

    latest_assessment_id = history[0]["assessment_id"] if history else None
    latest_details = RiskMonitoringService.get_assessment_details(db, latest_assessment_id) if latest_assessment_id else {}

    return {
        "patient": {
            "id": p_id,
            "name": patient_name,
            "email": patient_email,
            "age": age_val,
            "sex": sex_str,
            "height_cm": height_val,
            "weight_kg": weight_val,
            "bmi": bmi_val
        },
        "latest_assessment": latest_details,
        "history": history,
        "trends": trends,
        "alerts": [
            {
                "id": a.id,
                "assessment_id": a.assessment_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "message": a.message,
                "reason": a.reason,
                "status": a.status,
                "created_at": a.created_at.isoformat()
            } for a in alerts
        ],
        "feedbacks": [
            {
                "id": f.id,
                "assessment_id": f.assessment_id,
                "clinician_id": f.clinician_id,
                "feedback_text": f.feedback_text,
                "clinical_action": f.clinical_action,
                "created_at": f.created_at.isoformat()
            } for f in feedbacks
        ]
    }

@router.post("/clinician/feedback", response_model=ClinicianFeedbackResponse)
def submit_clinician_feedback(
    feedback_in: ClinicianFeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits clinician review and action for an assessment. Original ML predictions remain 100% immutable.
    """
    if current_user.role not in ["admin", "clinician", "doctor"]:
        raise HTTPException(status_code=403, detail="Clinician or Admin authorization required to submit feedback.")

    feedback = RiskMonitoringService.add_clinician_feedback(
        db=db,
        clinician_user=current_user,
        assessment_id=feedback_in.assessment_id,
        patient_id=feedback_in.patient_id,
        feedback_text=feedback_in.feedback_text,
        clinical_action=feedback_in.clinical_action or "Reviewed"
    )

    return feedback
