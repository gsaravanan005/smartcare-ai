from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import os
import joblib
import pandas as pd
import numpy as np
import uuid

from ..core.config import settings
from ..core.database import get_db
from ..core.mongo_db import mongo_manager
from ..core.security import get_current_user, verify_patient_access
from ..models.models import User, Patient, PredictionRecord, ExplanationRecord, FeatureContribution
from ..schemas.schemas import HealthRecordCreate
from ..services.explanation_service import ExplanationService
from ..services.dataset_loader_service import DatasetLoaderService
from ..services.preprocessing_pipeline_service import PreprocessingPipelineService
from ..services.audit_service import AuditLoggerService

router = APIRouter(prefix="/explanations", tags=["Explainable AI & SHAP Analysis"])

@router.post("", response_model=Dict[str, Any])
def generate_prediction_explanation(
    prediction_id: Optional[str] = None,
    health_input: Optional[HealthRecordCreate] = None,
    disease: str = "diabetes",
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = getattr(current_user, "id", getattr(current_user, "user_id", None))
    patients_col = mongo_manager.get_collection("patients")
    patient_doc = patients_col.find_one({"user_id": user_id})
    patient_id = patient_doc.get("patient_id") if patient_doc else None

    mtl_path = os.path.join(settings.BASE_DIR, "models", "multitask", "smartcare_mtl_model.joblib")
    task_map = {"diabetes": "t2d", "cardio": "cvd", "ckd": "ckd"}
    task_key = task_map.get(disease.lower(), "t2d")

    # 1. Load Model Bundle (prefer MTL model if available)
    if os.path.exists(mtl_path):
        bundle = joblib.load(mtl_path)
        mtl_model = bundle["model"]
        feature_names = bundle.get("feature_names", [])

        class SingleTaskWrapper:
            def __init__(self, m, t, feats):
                self.m = m
                self.t = t
                self.feats = feats
            def predict_proba(self, X):
                if isinstance(X, np.ndarray):
                    X = pd.DataFrame(X, columns=self.feats)
                p = self.m.forward(X, training=False)[0][self.t]
                return np.column_stack([1.0 - p, p])
            def predict(self, X):
                return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

        model_bundle = {
            "model": SingleTaskWrapper(mtl_model, task_key, feature_names),
            "model_version": "smartcare_mtl_v1",
            "feature_names": feature_names
        }

        # Background split
        from ml.multitask.dataset import MTLDatasetManager
        data_mgr = MTLDatasetManager()
        prep_path = os.path.join(settings.BASE_DIR, "models", "multitask", "preprocessing.pkl")
        if os.path.exists(prep_path):
            prep_data = joblib.load(prep_path)
            data_mgr.scaler = prep_data.get("scaler")
            data_mgr.imputer = prep_data.get("imputer")

        try:
            val_df = pd.read_csv(os.path.join(settings.ARTIFACTS_DIR, f"{disease}_val.csv"))
            bg_harm = data_mgr.harmonize_t2d_features(val_df) if disease == "diabetes" else (data_mgr.harmonize_cvd_features(val_df) if disease == "cardio" else data_mgr.harmonize_ckd_features(val_df))
            if data_mgr.imputer is not None:
                bg_imp = pd.DataFrame(data_mgr.imputer.transform(bg_harm), columns=feature_names)
            else:
                bg_imp = bg_harm.fillna(0.0)
            if data_mgr.scaler is not None:
                X_background = pd.DataFrame(data_mgr.scaler.transform(bg_imp), columns=feature_names)
            else:
                X_background = bg_imp
        except Exception:
            X_background = pd.DataFrame(columns=feature_names)

    else:
        model_path = os.path.join(settings.BASE_DIR, "models", disease, f"{disease}_best_model.joblib")
        if not os.path.exists(model_path):
            raise HTTPException(status_code=400, detail=f"No trained model artifact found for disease '{disease}'. Run Module 2 training first.")

        model_bundle = joblib.load(model_path)
        feature_names = model_bundle.get("feature_names", [])

        try:
            val_df = pd.read_csv(os.path.join(settings.ARTIFACTS_DIR, f"{disease}_val.csv"))
            target_col = DatasetLoaderService.TARGET_COLUMNS[disease]
            X_background = val_df.drop(columns=[target_col])
            if 'id' in X_background.columns:
                X_background = X_background.drop(columns=['id'])
        except Exception:
            X_background = pd.DataFrame(columns=feature_names)

    # 2. Extract transformed patient feature vector
    if prediction_id:
        predictions_col = mongo_manager.get_collection("predictions")
        pred_doc = predictions_col.find_one({"prediction_id": prediction_id})
        
        if pred_doc and pred_doc.get("module3_handoff_payload"):
            trans_features = pred_doc["module3_handoff_payload"].get("transformed_features_for_shap", {}).get(disease, {})
            X_patient = pd.DataFrame([trans_features])
        else:
            pred_rec = db.query(PredictionRecord).filter(PredictionRecord.prediction_id == prediction_id).first()
            if not pred_rec or not pred_rec.module3_handoff_payload:
                raise HTTPException(status_code=404, detail=f"Prediction record '{prediction_id}' not found.")
            trans_features = pred_rec.module3_handoff_payload.get("transformed_features_for_shap", {}).get(disease, {})
            X_patient = pd.DataFrame([trans_features])
    elif health_input:
        if os.path.exists(mtl_path):
            from ml.multitask.dataset import MTLDatasetManager
            data_mgr = MTLDatasetManager()
            prep_path = os.path.join(settings.BASE_DIR, "models", "multitask", "preprocessing.pkl")
            if os.path.exists(prep_path):
                prep_data = joblib.load(prep_path)
                data_mgr.scaler = prep_data.get("scaler")
                data_mgr.imputer = prep_data.get("imputer")
            X_patient = data_mgr.harmonize_patient_input(health_input.dict())
        else:
            trans_dict = PreprocessingPipelineService.transform_single_patient_input(disease, health_input.dict())
            X_patient = pd.DataFrame([trans_dict])
    else:
        raise HTTPException(status_code=400, detail="Provide either prediction_id or health_input.")

    # Align columns
    for mf in feature_names:
        if mf not in X_patient.columns:
            X_patient[mf] = 0.0
    X_patient = X_patient[feature_names]

    # Generate SHAP explanation
    explanation_res = ExplanationService.generate_local_explanation(disease, model_bundle, X_patient, X_background, top_k=5)

    exp_id = f"EXP_SHAP_{uuid.uuid4().hex[:8].upper()}"
    explanation_res["explanation_id"] = exp_id
    now_iso = datetime.now(timezone.utc).isoformat()

    # Format feature importance dict for MongoDB document
    feat_importance_dict = {
        fc["feature_name"]: fc["shap_value"] for fc in explanation_res["top_risk_factors"]
    }

    # Format Module 4 Handoff Package
    module4_handoff = {
        "prediction_id": prediction_id or exp_id,
        "patient_id": patient_id,
        "disease": disease.upper(),
        "model_version": explanation_res["model_version"],
        "preprocessing_version": "v1.0.0",
        "shap_base_value": explanation_res["base_value"],
        "top_risk_factors": explanation_res["top_risk_factors"],
        "all_contributions": explanation_res["all_contributions"],
        "explanation_version": "v1.0.0",
        "explanation_timestamp": explanation_res["explanation_timestamp"]
    }
    explanation_res["module4_handoff"] = module4_handoff

    # Save to MongoDB explanations collection
    explanations_col = mongo_manager.get_collection("explanations")
    mongo_exp_doc = {
        "explanation_id": exp_id,
        "prediction_id": prediction_id or exp_id,
        "patient_id": patient_id,
        "disease": disease,
        "model_version": explanation_res["model_version"],
        "explainer_type": explanation_res["explainer_type"],
        "base_value": explanation_res["base_value"],
        "feature_importance": feat_importance_dict,
        "top_features": explanation_res["top_risk_factors"],
        "explanation_summary": f"Top risk factor for {disease.upper()} is {explanation_res['top_risk_factors'][0]['feature_name'] if explanation_res['top_risk_factors'] else 'baseline'}.",
        "created_at": now_iso,
        "module4_handoff": module4_handoff
    }
    explanations_col.insert_one(mongo_exp_doc)

    AuditLoggerService.log_event(
        user_id=user_id,
        role=getattr(current_user, "role", "patient"),
        action="GENERATE_SHAP_EXPLANATION",
        resource="explanations",
        resource_id=exp_id,
        result="SUCCESS",
        metadata={"disease": disease, "prediction_id": prediction_id}
    )

    return explanation_res


@router.get("/{prediction_id}")
def get_explanation_by_prediction_id(prediction_id: str, db: Session = Depends(get_db), current_user: Any = Depends(get_current_user)):
    explanations_col = mongo_manager.get_collection("explanations")
    exp_doc = explanations_col.find_one({"prediction_id": prediction_id})

    if exp_doc:
        if exp_doc.get("patient_id"):
            verify_patient_access(current_user, exp_doc["patient_id"], db)
        return {
            "explanation_id": exp_doc.get("explanation_id"),
            "prediction_id": exp_doc.get("prediction_id"),
            "disease": exp_doc.get("disease"),
            "model_version": exp_doc.get("model_version"),
            "explainer_type": exp_doc.get("explainer_type"),
            "base_value": exp_doc.get("base_value"),
            "feature_importance": exp_doc.get("feature_importance"),
            "top_risk_factors": exp_doc.get("top_features"),
            "explanation_summary": exp_doc.get("explanation_summary"),
            "module4_handoff": exp_doc.get("module4_handoff")
        }

    # Fallback to SQLite query
    exp_record = db.query(ExplanationRecord).filter(ExplanationRecord.prediction_id == prediction_id).first()
    if not exp_record:
        raise HTTPException(status_code=404, detail=f"Explanation for prediction '{prediction_id}' not found.")
    
    if exp_record.patient_id:
        verify_patient_access(current_user, exp_record.patient_id, db)

    factors = db.query(FeatureContribution).filter(FeatureContribution.explanation_id == exp_record.explanation_id).order_by(FeatureContribution.rank).all()
    return {
        "explanation_id": exp_record.explanation_id,
        "prediction_id": exp_record.prediction_id,
        "disease": exp_record.disease,
        "model_version": exp_record.model_version,
        "explainer_type": exp_record.explainer_type,
        "base_value": exp_record.base_value,
        "top_risk_factors": factors,
        "module4_handoff": exp_record.module4_handoff_payload
    }
