import os
import joblib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.models import ModelRegistry, ModelExperiment, ModelEvaluation

class ModelRegistryService:

    @classmethod
    def save_model_artifact(
        cls,
        disease: str,
        model_name: str,
        version: str,
        model: Any,
        feature_names: List[str],
        threshold: float,
        calibration_method: str,
        metrics: Dict[str, Any]
    ) -> str:
        disease_dir = os.path.join(settings.BASE_DIR, "models", disease)
        os.makedirs(disease_dir, exist_ok=True)

        artifact_path = os.path.join(disease_dir, f"{version}.joblib")
        best_path = os.path.join(disease_dir, f"{disease}_best_model.joblib")

        bundle = {
            "disease": disease,
            "model_name": model_name,
            "model_version": version,
            "model": model,
            "feature_names": feature_names,
            "threshold": threshold,
            "calibration_method": calibration_method,
            "metrics": metrics,
            "saved_at": datetime.utcnow().isoformat()
        }

        joblib.dump(bundle, artifact_path)
        joblib.dump(bundle, best_path)

        return artifact_path

    @classmethod
    def register_model_in_db(
        cls,
        db: Session,
        disease: str,
        model_name: str,
        version: str,
        framework: str,
        artifact_path: str,
        metrics: Dict[str, Any]
    ) -> ModelRegistry:
        # Deactivate old active models for this disease
        db.query(ModelRegistry).filter(ModelRegistry.disease == disease).update({"status": "INACTIVE"})
        
        reg = db.query(ModelRegistry).filter(ModelRegistry.model_version == version).first()
        if reg:
            reg.model_name = model_name
            reg.disease = disease
            reg.framework = framework
            reg.artifact_path = artifact_path
            reg.status = "ACTIVE"
            reg.performance_metrics = metrics
        else:
            reg = ModelRegistry(
                model_name=model_name,
                disease=disease,
                model_version=version,
                framework=framework,
                training_dataset_version="v1.0.0",
                preprocessing_version="v1.0.0",
                artifact_path=artifact_path,
                status="ACTIVE",
                performance_metrics=metrics
            )
            db.add(reg)
            
        db.commit()
        db.refresh(reg)
        return reg


    @classmethod
    def log_evaluation_in_db(
        cls,
        db: Session,
        model_version: str,
        disease: str,
        test_metrics: Dict[str, Any]
    ) -> ModelEvaluation:
        eval_record = ModelEvaluation(
            model_version=model_version,
            disease=disease,
            accuracy=test_metrics.get("accuracy", 0.0),
            precision=test_metrics.get("precision", 0.0),
            recall=test_metrics.get("recall", 0.0),
            f1_score=test_metrics.get("f1_score", 0.0),
            roc_auc=test_metrics.get("roc_auc", 0.0),
            pr_auc=test_metrics.get("pr_auc", 0.0),
            brier_score=test_metrics.get("brier_score", 0.0),
            confusion_matrix=test_metrics.get("confusion_matrix"),
            calibration_details=test_metrics.get("calibration_curve")
        )
        db.add(eval_record)
        db.commit()
        db.refresh(eval_record)
        return eval_record
