from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.models import User, Patient, HealthRecord
from ..schemas.schemas import HealthRecordCreate, HealthRecordResponse
from ..services.preprocessing_pipeline_service import PreprocessingPipelineService

router = APIRouter(prefix="/health-data", tags=["Patient Health Data"])

@router.post("/submit", response_model=HealthRecordResponse)
def submit_health_record(
    record_in: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        patient = Patient(
            user_id=current_user.id,
            age=record_in.age,
            sex=int(record_in.sex) if record_in.sex is not None else 1,
            height_cm=record_in.height_cm,
            weight_kg=record_in.weight_kg
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

    # Convert Pydantic record to dict
    data_dict = record_in.dict()

    # Preprocess patient features for all 3 disease pipelines
    preprocessed_outputs = {}
    for disease in ["diabetes", "cardio", "ckd"]:
        try:
            preprocessed_outputs[disease] = PreprocessingPipelineService.transform_single_patient_input(
                disease, data_dict
            )
        except Exception as e:
            preprocessed_outputs[disease] = {"error": str(e)}

    # Save to database
    record = HealthRecord(
        patient_id=patient.id,
        high_bp=record_in.high_bp,
        high_chol=record_in.high_chol,
        chol_check=record_in.chol_check,
        stroke=record_in.stroke,
        heart_disease_or_attack=record_in.heart_disease_or_attack,
        any_healthcare=record_in.any_healthcare,
        no_doc_bc_cost=record_in.no_doc_bc_cost,
        diff_walk=record_in.diff_walk,
        smoker=record_in.smoker,
        hvy_alcohol_consump=record_in.hvy_alcohol_consump,
        phys_activity=record_in.phys_activity,
        fruits=record_in.fruits,
        veggies=record_in.veggies,
        gen_hlth=record_in.gen_hlth,
        ment_hlth=record_in.ment_hlth,
        phys_hlth=record_in.phys_hlth,
        ap_hi=record_in.ap_hi,
        ap_lo=record_in.ap_lo,
        glucose=record_in.glucose,
        cholesterol=record_in.cholesterol,
        serum_creatinine=record_in.serum_creatinine,
        blood_urea=record_in.blood_urea,
        hemoglobin=record_in.hemoglobin,
        sodium=record_in.sodium,
        potassium=record_in.potassium,
        packed_cell_volume=record_in.packed_cell_volume,
        white_blood_cell_count=record_in.white_blood_cell_count,
        red_blood_cell_count=record_in.red_blood_cell_count,
        hypertension_flag=record_in.hypertension_flag,
        diabetes_mellitus_flag=record_in.diabetes_mellitus_flag,
        coronary_artery_disease=record_in.coronary_artery_disease,
        appetite=record_in.appetite,
        pedal_edema=record_in.pedal_edema,
        anemia=record_in.anemia,
        preprocessed_features=preprocessed_outputs
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record

@router.get("/records", response_model=List[HealthRecordResponse])
def get_patient_records(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        return []
    records = db.query(HealthRecord).filter(HealthRecord.patient_id == patient.id).order_by(HealthRecord.created_at.desc()).all()
    return records
