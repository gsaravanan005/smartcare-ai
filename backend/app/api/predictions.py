from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid

from ..core.database import get_db
from ..core.mongo_db import mongo_manager
from ..core.security import get_current_user, verify_patient_access
from ..models.models import User, Patient, PredictionRecord
from ..schemas.schemas import HealthRecordCreate
from ..services.prediction_service import PredictionService
from ..services.audit_service import AuditLoggerService

router = APIRouter(prefix="/predictions", tags=["Disease Risk Predictions"])

@router.post("", response_model=Dict[str, Any])
def predict_multi_disease_risk(
    health_input: HealthRecordCreate,
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
    patients_col = mongo_manager.get_collection("patients")
    patient_doc = patients_col.find_one({"user_id": user_id})
    patient_id = patient_doc.get("patient_id") if patient_doc else None

    if not patient_id:
        patient_sql = db.query(Patient).filter(Patient.user_id == user_id).first()
        patient_id = patient_sql.id if patient_sql else None

    # Execute prediction service
    input_dict = health_input.dict()
    res = PredictionService.predict_multi_disease_risk(input_dict, patient_id=patient_id)

    pred_id = f"PRED_{uuid.uuid4().hex[:8].upper()}"
    preds = res["predictions"]
    now_iso = datetime.now(timezone.utc).isoformat()

    # Save to MongoDB predictions collection
    predictions_col = mongo_manager.get_collection("predictions")
    mongo_pred_doc = {
        "prediction_id": pred_id,
        "patient_id": patient_id,
        "model_name": "SmartCare AI Multi-Disease Ensemble",
        "model_version": preds["diabetes"]["model_version"],
        "input_features": input_dict,
        "prediction": preds,
        "risk_score": {
            "diabetes": preds["diabetes"]["probability"],
            "cvd": preds["cardio"]["probability"],
            "ckd": preds["ckd"]["probability"]
        },
        "risk_level": {
            "diabetes": preds["diabetes"]["risk_category"],
            "cvd": preds["cardio"]["risk_category"],
            "ckd": preds["ckd"]["risk_category"]
        },
        "diabetes_probability": preds["diabetes"]["probability"],
        "diabetes_risk_category": preds["diabetes"]["risk_category"],
        "cvd_probability": preds["cardio"]["probability"],
        "cvd_risk_category": preds["cardio"]["risk_category"],
        "ckd_probability": preds["ckd"]["probability"],
        "ckd_risk_category": preds["ckd"]["risk_category"],
        "prediction_date": now_iso,
        "created_at": now_iso,
        "module3_handoff_payload": res["module3_handoff"]
    }
    predictions_col.insert_one(mongo_pred_doc)

    # Sync with SQLite PredictionRecord
    try:
        record = PredictionRecord(
            prediction_id=pred_id,
            patient_id=patient_id,
            diabetes_probability=preds["diabetes"]["probability"],
            diabetes_risk_category=preds["diabetes"]["risk_category"],
            cvd_probability=preds["cardio"]["probability"],
            cvd_risk_category=preds["cardio"]["risk_category"],
            ckd_probability=preds["ckd"]["probability"],
            ckd_risk_category=preds["ckd"]["risk_category"],
            model_version=preds["diabetes"]["model_version"],
            preprocessing_version="v1.0.0",
            calibration_version=preds["diabetes"]["calibration_version"],
            module3_handoff_payload=res["module3_handoff"]
        )
        db.add(record)
        db.commit()

        if patient_id:
            from ..services.risk_monitoring_service import RiskMonitoringService
            RiskMonitoringService.evaluate_and_create_alerts(db, patient_id, record)
    except Exception as e:
        print(f"[SQL Sync Prediction Warning] {e}")

    AuditLoggerService.log_event(
        user_id=user_id,
        role=getattr(current_user, "role", "patient"),
        action="CREATE_DISEASE_RISK_PREDICTION",
        resource="predictions",
        resource_id=pred_id,
        result="SUCCESS",
        metadata={"patient_id": patient_id, "prediction_id": pred_id}
    )

    res["prediction_id"] = pred_id
    return res


@router.get("/patient/{patient_id}")
def get_patient_predictions(patient_id: int, current_user: Any = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_patient_access(current_user, patient_id, db)
    
    predictions_col = mongo_manager.get_collection("predictions")
    mongo_records = list(predictions_col.find({"patient_id": patient_id}, {"_id": 0}, sort=[("created_at", -1)]))

    if mongo_records:
        return mongo_records

    # Fallback to SQLite query
    records = db.query(PredictionRecord).filter(PredictionRecord.patient_id == patient_id).order_by(PredictionRecord.created_at.desc()).all()
    return records
