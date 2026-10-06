import pytest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.data_validation_service import DataValidationService
from app.services.model_training_service import ModelTrainingService
from app.services.explanation_service import ExplanationService

def test_shap_explainer_selection_and_local_explanation():
    X_tr, y_tr, X_va, y_va, _, _, meta = DataValidationService.validate_dataset_artifacts("ckd")
    rf_model = ModelTrainingService.train_random_forest(X_tr, y_tr, n_estimators=20)
    
    bundle = {
        "model": rf_model,
        "model_version": "ckd_rf_test_v1",
        "feature_names": X_tr.columns.tolist()
    }

    # Generate local explanation for patient 0
    X_patient = X_va.iloc[[0]]
    explanation = ExplanationService.generate_local_explanation("ckd", bundle, X_patient, X_va, top_k=5)

    assert explanation["disease"] == "CKD"
    assert explanation["explainer_type"] == "TreeExplainer"
    assert "base_value" in explanation
    assert len(explanation["top_risk_factors"]) <= 5

    top1 = explanation["top_risk_factors"][0]
    assert "feature_name" in top1
    assert "patient_value" in top1
    assert "shap_value" in top1
    assert top1["direction"] in ["RISK_INCREASING", "RISK_DECREASING"]
    assert top1["modifiable_status"] in ["Modifiable", "Non-Modifiable", "Potentially Modifiable"]

def test_global_shap_feature_importance():
    X_tr, y_tr, X_va, y_va, _, _, _ = DataValidationService.validate_dataset_artifacts("ckd")
    rf_model = ModelTrainingService.train_random_forest(X_tr, y_tr, n_estimators=20)

    bundle = {
        "model": rf_model,
        "model_version": "ckd_rf_test_v1",
        "feature_names": X_tr.columns.tolist()
    }

    global_exp = ExplanationService.generate_global_explanation("ckd", bundle, X_va)
    assert global_exp["disease"] == "CKD"
    assert len(global_exp["global_feature_importance"]) == len(X_tr.columns)
    assert global_exp["global_feature_importance"][0]["rank"] == 1

def test_module4_handoff_payload_formatting():
    X_tr, y_tr, X_va, _, _, _, _ = DataValidationService.validate_dataset_artifacts("diabetes")
    xgb_model = ModelTrainingService.train_xgboost(X_tr, y_tr, n_estimators=20)

    bundle = {
        "model": xgb_model,
        "model_version": "diabetes_xgb_test_v1",
        "feature_names": X_tr.columns.tolist()
    }

    local_exp = ExplanationService.generate_local_explanation("diabetes", bundle, X_va.iloc[[0]], X_va, top_k=5)
    
    assert "top_risk_factors" in local_exp
    assert "all_contributions" in local_exp
    assert local_exp["consistency_valid"] is True
