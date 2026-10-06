import os
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from ..core.database import get_db
from ..core.mongo_db import mongo_manager
from ..core.security import (
    get_current_user, 
    verify_patient_access, 
    verify_doctor_patient_access, 
    get_patient_profile_id, 
    require_role,
    check_maintenance_mode
)
from ..services.pdf_report_service import PDFReportService
from ..services.audit_service import AuditLoggerService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Patient Health Reports & PDFs"])

class ReportReviewRequest(BaseModel):
    notes: str
    clinical_action: Optional[str] = "Reviewed — Follow-up Recommended"
    patient_visible: Optional[bool] = True

class ReportVisibilityRequest(BaseModel):
    patient_visible: bool

def _serialize_report(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d

@router.get("/my-reports", response_model=List[Dict[str, Any]])
def get_my_patient_reports(
    current_user=Depends(check_maintenance_mode),
    db: Session = Depends(get_db)
):
    """
    Retrieves all health reports strictly owned by the authenticated patient.
    Derives patient profile ID automatically from the secure token/session.
    """
    auth_patient_id = get_patient_profile_id(current_user, db)
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", auth_patient_id))

    db_reports = mongo_manager.get_collection("reports")
    cursor = db_reports.find(
        {"$or": [{"patient_id": auth_patient_id}, {"patient_id": user_id}]},
        sort=[("created_at", -1)]
    )
    
    results = [_serialize_report(doc) for doc in cursor]

    # If no report exists, auto-generate initial report
    if not results:
        try:
            logger.info(f"[REPORTS_API] Auto-generating initial report for authenticated patient #{auth_patient_id}")
            rep = PDFReportService.generate_patient_pdf_report(patient_id=auth_patient_id)
            results.append(_serialize_report(rep))
        except Exception as e:
            logger.exception(f"[REPORTS_API] Auto-generation failed for patient #{auth_patient_id}: {e}")

    AuditLoggerService.log_event(
        user_id=user_id,
        role=getattr(current_user, "role", "patient"),
        action="GET_MY_PATIENT_REPORTS",
        resource="reports",
        result="SUCCESS",
        metadata={"patient_id": auth_patient_id, "reports_count": len(results)}
    )

    return results

@router.post("/generate/patient/{patient_id}", response_model=Dict[str, Any])
def generate_report_for_patient(
    patient_id: int,
    current_user=Depends(check_maintenance_mode),
    db: Session = Depends(get_db)
):
    """
    Authoritative report generation by patient ID.
    Enforces role-based data isolation and doctor assignment.
    """
    verify_patient_access(current_user, patient_id, db)
    try:
        report_result = PDFReportService.generate_patient_pdf_report(patient_id=patient_id)

        AuditLoggerService.log_event(
            user_id=getattr(current_user, "id", 1),
            role=getattr(current_user, "role", "patient"),
            action="GENERATE_PATIENT_PDF_REPORT_BY_PATIENT",
            resource="reports",
            resource_id=report_result["report_id"],
            result="SUCCESS",
            metadata={"patient_id": patient_id}
        )

        return _serialize_report(report_result)
    except Exception as e:
        logger.exception(f"[REPORTS_API] Failed to generate report for patient {patient_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )

@router.post("/generate/{prediction_id}", response_model=Dict[str, Any])
def generate_report_for_prediction(
    prediction_id: str,
    current_user=Depends(check_maintenance_mode),
    db: Session = Depends(get_db)
):
    """
    Generates or updates the 7-page graphical clinical AI assessment PDF report for a specific prediction ID.
    Enforces strict patient data isolation.
    """
    db_predictions = mongo_manager.get_collection("predictions")
    pred_doc = db_predictions.find_one({"prediction_id": prediction_id})
    if not pred_doc:
        raise HTTPException(status_code=404, detail=f"Prediction record '{prediction_id}' not found.")

    patient_id = pred_doc.get("patient_id")
    if patient_id:
        verify_patient_access(current_user, patient_id, db)
    else:
        patient_id = get_patient_profile_id(current_user, db)

    try:
        report_result = PDFReportService.generate_patient_pdf_report(
            patient_id=patient_id,
            prediction_id=prediction_id
        )

        AuditLoggerService.log_event(
            user_id=getattr(current_user, "id", 1),
            role=getattr(current_user, "role", "patient"),
            action="GENERATE_PATIENT_PDF_REPORT",
            resource="reports",
            resource_id=report_result["report_id"],
            result="SUCCESS",
            metadata={"patient_id": patient_id, "prediction_id": prediction_id}
        )

        return _serialize_report(report_result)
    except Exception as e:
        logger.exception(f"[REPORTS_API] Failed to generate report for prediction {prediction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )

@router.get("/patient/{patient_id}", response_model=List[Dict[str, Any]])
def get_patient_reports(
    patient_id: int,
    current_user=Depends(check_maintenance_mode),
    db: Session = Depends(get_db)
):
    """
    Retrieves all generated health reports for a specified patient.
    Strictly verifies ownership or doctor assignment.
    """
    verify_patient_access(current_user, patient_id, db)
    db_reports = mongo_manager.get_collection("reports")
    
    # Also resolve alternate user_id / patient_id alias if needed
    cursor = db_reports.find({"$or": [{"patient_id": patient_id}, {"user_id": patient_id}]}, sort=[("created_at", -1)])
    
    results = [_serialize_report(doc) for doc in cursor]

    # If no report generated yet, generate one on demand
    if not results:
        try:
            logger.info(f"[REPORTS_API] Auto-generating initial clinical report for patient {patient_id}")
            rep = PDFReportService.generate_patient_pdf_report(patient_id=patient_id)
            results.append(_serialize_report(rep))
        except Exception as e:
            logger.exception(f"[REPORTS_API] Auto-generation failed for patient {patient_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate clinical health report for patient {patient_id}: {str(e)}"
            )

    return results

@router.get("/{report_id}/view", response_model=Dict[str, Any])
def view_report_details(
    report_id: str,
    current_user=Depends(check_maintenance_mode),
    db: Session = Depends(get_db)
):
    """
    Retrieves metadata and status for a specific report ID.
    Enforces patient ownership and visibility policies.
    """
    db_reports = mongo_manager.get_collection("reports")
    report_doc = db_reports.find_one({"report_id": report_id})
    if not report_doc:
        raise HTTPException(status_code=404, detail="Patient Record Unavailable. This health record is not associated with your account.")

    patient_id = report_doc.get("patient_id")
    if patient_id is not None:
        verify_patient_access(current_user, patient_id, db)

    user_role = (getattr(current_user, "role", "patient") or "patient").lower()
    
    # If patient, verify visibility
    if user_role == "patient":
        is_visible = report_doc.get("patient_visible", True)
        rep_status = str(report_doc.get("status", "")).upper()
        if not is_visible and rep_status in ["PENDING_DOCTOR_REVIEW", "REQUIRES_REASSESSMENT"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your health assessment has been generated and is currently being reviewed by your healthcare provider."
            )

    AuditLoggerService.log_event(
        user_id=getattr(current_user, "id", 1),
        role=user_role,
        action="VIEW_REPORT_DETAILS",
        resource="reports",
        resource_id=report_id,
        result="SUCCESS",
        metadata={"patient_id": patient_id}
    )

    return _serialize_report(report_doc)

@router.get("/{report_id}/download")
def download_pdf_report(
    report_id: str,
    inline: bool = Query(True, description="Display inline in browser or force attachment download"),
    token: Optional[str] = Query(None, description="Optional bearer token for iframe and direct browser navigation"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Streams the generated PDF report file.
    Enforces strict JWT token authentication and resource ownership authorization.
    """
    auth_token = None
    if authorization and authorization.startswith("Bearer "):
        auth_token = authorization.split(" ", 1)[1]
    elif token:
        auth_token = token.strip()
        if auth_token.startswith("Bearer "):
            auth_token = auth_token.split(" ", 1)[1]

    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Missing Bearer token in header or query parameter.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = get_current_user(token=auth_token, db=db)

    db_reports = mongo_manager.get_collection("reports")
    report_doc = db_reports.find_one({"report_id": report_id})
    if not report_doc:
        raise HTTPException(status_code=404, detail="Patient Record Unavailable. This health record is not associated with your account.")

    patient_id = report_doc.get("patient_id")
    if patient_id is not None:
        verify_patient_access(current_user, patient_id, db)

    user_role = (getattr(current_user, "role", "patient") or "patient").lower()
    if user_role == "patient":
        is_visible = report_doc.get("patient_visible", True)
        rep_status = str(report_doc.get("status", "")).upper()
        if not is_visible and rep_status in ["PENDING_DOCTOR_REVIEW", "REQUIRES_REASSESSMENT"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your health assessment has been generated and is currently being reviewed by your healthcare provider."
            )

    file_path = report_doc.get("file_path")
    if not file_path or not os.path.exists(file_path):
        try:
            rep = PDFReportService.generate_patient_pdf_report(
                patient_id=report_doc["patient_id"],
                prediction_id=report_doc.get("prediction_id")
            )
            file_path = rep["file_path"]
        except Exception as e:
            logger.exception(f"[REPORTS_API] Regeneration failed for {report_id}: {e}")
            raise HTTPException(status_code=500, detail="Report file not found and regeneration failed.")

    filename = report_doc.get("file_name", f"SmartCare_AI_Report_{report_id}.pdf")
    disposition = "inline" if inline else "attachment"

    AuditLoggerService.log_event(
        user_id=getattr(current_user, "id", 1),
        role=user_role,
        action="DOWNLOAD_PDF_REPORT",
        resource="reports",
        resource_id=report_id,
        result="SUCCESS",
        metadata={"patient_id": patient_id, "inline": inline}
    )

    headers = {
        "Content-Disposition": f'{disposition}; filename="{filename}"'
    }

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename,
        headers=headers
    )

@router.put("/{report_id}/review", response_model=Dict[str, Any])
def review_and_sign_report(
    report_id: str,
    payload: ReportReviewRequest,
    current_user=Depends(require_role(["doctor", "clinician", "admin"])),
    db: Session = Depends(get_db)
):
    """
    Doctor / Clinician review endpoint. Adds clinical notes, transitions status to 'Clinician Reviewed',
    and sets patient_visible = True.
    """
    db_reports = mongo_manager.get_collection("reports")
    report_doc = db_reports.find_one({"report_id": report_id})
    if not report_doc:
        raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found.")

    patient_id = report_doc.get("patient_id")
    now_iso = datetime.now(timezone.utc).isoformat()
    doctor_id = getattr(current_user, "id", 101)
    doctor_name = getattr(current_user, "full_name", getattr(current_user, "username", "Dr. Sarah Jenkins"))

    # Save clinician feedback
    db_feedbacks = mongo_manager.get_collection("clinician_feedback")
    db_feedbacks.insert_one({
        "feedback_id": f"FB_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "assessment_id": report_doc.get("prediction_id"),
        "patient_id": patient_id,
        "clinician_id": doctor_id,
        "clinician_name": doctor_name,
        "feedback_text": payload.notes,
        "clinical_action": payload.clinical_action,
        "created_at": now_iso
    })

    # Update report status to 'Clinician Reviewed' and patient_visible to True
    new_status = "Clinician Reviewed"
    db_reports.update_one(
        {"report_id": report_id},
        {"$set": {
            "status": new_status,
            "report_status": new_status,
            "patient_visible": payload.patient_visible if payload.patient_visible is not None else True,
            "doctor_notes": payload.notes,
            "clinical_action": payload.clinical_action,
            "reviewed_by": doctor_name,
            "reviewed_at": now_iso,
            "updated_at": now_iso
        }}
    )

    # Regenerate PDF with approved clinician feedback included
    PDFReportService.generate_patient_pdf_report(
        patient_id=patient_id,
        prediction_id=report_doc.get("prediction_id")
    )

    AuditLoggerService.log_event(
        user_id=doctor_id,
        role=getattr(current_user, "role", "doctor"),
        action="CLINICIAN_REVIEWED_PATIENT_REPORT",
        resource="reports",
        resource_id=report_id,
        result="SUCCESS",
        metadata={"patient_id": patient_id, "new_status": new_status, "patient_visible": payload.patient_visible}
    )

    return {
        "report_id": report_id,
        "status": new_status,
        "patient_visible": payload.patient_visible,
        "message": f"Report '{report_id}' reviewed and signed successfully."
    }

@router.put("/{report_id}/visibility", response_model=Dict[str, Any])
def toggle_report_visibility(
    report_id: str,
    payload: ReportVisibilityRequest,
    current_user=Depends(require_role(["doctor", "clinician", "admin"])),
    db: Session = Depends(get_db)
):
    """
    Allows Doctor or Admin to update patient_visible flag on a report.
    """
    db_reports = mongo_manager.get_collection("reports")
    report_doc = db_reports.find_one({"report_id": report_id})
    if not report_doc:
        raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found.")

    now_iso = datetime.now(timezone.utc).isoformat()
    db_reports.update_one(
        {"report_id": report_id},
        {"$set": {
            "patient_visible": payload.patient_visible,
            "updated_at": now_iso
        }}
    )

    AuditLoggerService.log_event(
        user_id=getattr(current_user, "id", 1),
        role=getattr(current_user, "role", "doctor"),
        action="UPDATE_REPORT_PATIENT_VISIBILITY",
        resource="reports",
        resource_id=report_id,
        result="SUCCESS",
        metadata={"patient_visible": payload.patient_visible}
    )

    return {
        "report_id": report_id,
        "patient_visible": payload.patient_visible,
        "message": f"Report visibility updated to {'Visible to Patient' if payload.patient_visible else 'Hidden from Patient'}."
    }
