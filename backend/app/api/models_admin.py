from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import require_role
from ..models.models import ModelRegistry, ModelExperiment, ModelEvaluation
from ..services.data_validation_service import DataValidationService
from ..services.model_training_service import ModelTrainingService
from ..services.tuning_cv_service import TuningCVService
from ..services.calibration_service import CalibrationService
from ..services.experiment_comparison_service import ExperimentComparisonService
from ..services.model_registry_service import ModelRegistryService

router = APIRouter(prefix="/models", tags=["MLOps Model Registry & Performance"])

@router.get("/registry")
def get_model_registry(db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "clinician"]))):
    models = db.query(ModelRegistry).order_by(ModelRegistry.created_at.desc()).all()
    return models

@router.get("/experiments")
def get_model_experiments(db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "clinician"]))):
    experiments = db.query(ModelExperiment).order_by(ModelExperiment.created_at.desc()).all()
    return experiments

@router.get("/evaluations/{disease}")
def get_model_evaluation(disease: str, db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "clinician"]))):
    eval_rec = db.query(ModelEvaluation).filter(ModelEvaluation.disease == disease).order_by(ModelEvaluation.evaluated_at.desc()).first()
    if not eval_rec:
        raise HTTPException(status_code=444, detail=f"No evaluation records found for disease '{disease}'. Run model training first.")
    return eval_rec
