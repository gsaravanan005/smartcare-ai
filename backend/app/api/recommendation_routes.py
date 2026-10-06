"""
SmartCare AI - Module 4 Recommendation Routes
Exposes REST endpoints for generating and retrieving personalized wellness recommendation plans.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from ..core.database import get_db
from ..core.security import get_current_user, verify_patient_access
from ..models.models import User, Patient, PredictionRecord, RecommendationRecord
from ..schemas.recommendation_schema import RecommendationGenerateRequest, RecommendationPlanResponse, RecommendationItem
from ..services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Personalized Wellness Recommendation"])

@router.post("/generate", response_model=RecommendationPlanResponse)
def generate_recommendations(
    payload: Optional[RecommendationGenerateRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates a personalized wellness plan based on the patient's actual prediction results
    and Module 3 SHAP risk factors with multilingual localization support.
    """
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    patient_id = patient.id if patient else None

    req_patient_id = payload.patient_id if (payload and payload.patient_id) else patient_id
    if req_patient_id:
        verify_patient_access(current_user, req_patient_id, db)

    req_prediction_id = (payload.prediction_id or payload.assessment_id) if payload else None
    req_language = payload.language if (payload and payload.language) else "en"
    health_input = payload.health_input.dict() if (payload and payload.health_input) else None

    try:
        plan = RecommendationService.generate_recommendation_plan(
            db=db,
            patient_id=req_patient_id,
            prediction_id=req_prediction_id,
            health_input=health_input,
            language=req_language
        )
        return plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendation plan: {str(e)}"
        )

@router.get("/patient/{patient_id}", response_model=RecommendationPlanResponse)
def get_patient_recommendations(
    patient_id: int,
    language: Optional[str] = "en",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves or generates personalized wellness plan for a specified patient ID.
    """
    verify_patient_access(current_user, patient_id, db)
    try:
        plan = RecommendationService.generate_recommendation_plan(
            db=db,
            patient_id=patient_id,
            language=language or "en"
        )
        return plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch patient recommendation plan: {str(e)}"
        )


@router.get("/{patient_id}", response_model=RecommendationPlanResponse)
def get_patient_recommendations_alias(
    patient_id: int,
    language: Optional[str] = "en",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Alias route: GET /api/recommendations/{patient_id}
    """
    return get_patient_recommendations(patient_id=patient_id, language=language, current_user=current_user, db=db)

@router.get("/assessment/{assessment_id}", response_model=RecommendationPlanResponse)
def get_assessment_recommendations(
    assessment_id: str,
    language: Optional[str] = "en",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves or generates recommendations linked to a specific assessment or prediction ID.
    Enforces patient ownership.
    """
    db_predictions = mongo_manager.get_collection("predictions")
    pred_doc = db_predictions.find_one({"prediction_id": assessment_id})
    if pred_doc and pred_doc.get("patient_id"):
        verify_patient_access(current_user, pred_doc["patient_id"], db)

    try:
        plan = RecommendationService.generate_recommendation_plan(
            db=db,
            prediction_id=assessment_id,
            language=language or "en"
        )
        return plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch assessment recommendation plan: {str(e)}"
        )
