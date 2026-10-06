import pytest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.data_validation_service import DataValidationService
from app.services.model_training_service import ModelTrainingService
from app.services.calibration_service import CalibrationService
from app.services.prediction_service import PredictionService
from app.services.experiment_comparison_service import ExperimentComparisonService

def test_data_validation_service():
    X_tr, y_tr, X_va, y_va, X_te, y_te, meta = DataValidationService.validate_dataset_artifacts("ckd")
    assert not X_tr.empty
    assert len(y_tr) == len(X_tr)
    assert meta["target_col"] == "classification"
    assert X_tr.isnull().sum().sum() == 0, "No NaN values allowed in validated training features."

def test_model_training_and_probability_predictions():
    X_tr, y_tr, X_va, y_va, _, _, _ = DataValidationService.validate_dataset_artifacts("ckd")
    
    # Train Logistic Regression
    lr = ModelTrainingService.train_logistic_regression(X_tr, y_tr, C=1.0)
    probs = lr.predict_proba(X_va)[:, 1]
    assert len(probs) == len(X_va)
    assert (probs >= 0.0).all() and (probs <= 1.0).all(), "Probabilities must be bounded in [0.0, 1.0]."

    # Train Random Forest
    rf = ModelTrainingService.train_random_forest(X_tr, y_tr, n_estimators=20)
    rf_probs = rf.predict_proba(X_va)[:, 1]
    assert len(rf_probs) == len(X_va)

    # Train XGBoost
    xgb_m = ModelTrainingService.train_xgboost(X_tr, y_tr, n_estimators=20)
    xgb_probs = xgb_m.predict_proba(X_va)[:, 1]
    assert len(xgb_probs) == len(X_va)

def test_calibration_service():
    X_tr, y_tr, X_va, y_va, _, _, _ = DataValidationService.validate_dataset_artifacts("ckd")
    rf = ModelTrainingService.train_random_forest(X_tr, y_tr, n_estimators=20)
    
    calib_model, metrics = CalibrationService.calibrate_model(rf, X_val=X_va, y_val=y_va, method="sigmoid")
    assert "calibrated_brier_score" in metrics
    assert 0.0 <= metrics["calibrated_brier_score"] <= 1.0

    th_info = CalibrationService.find_optimal_threshold(calib_model, X_va, y_val=y_va, min_recall_target=0.80)
    assert "threshold" in th_info
    assert th_info["recall"] >= 0.70

def test_prediction_service_and_module3_handoff():
    sample_input = {
        "age": 50,
        "ap_hi": 130,
        "ap_lo": 85,
        "glucose": 110,
        "serum_creatinine": 1.1,
        "blood_urea": 32.0,
        "hemoglobin": 13.5,
        "high_bp": 1,
        "smoker": 0
    }

    res = PredictionService.predict_multi_disease_risk(sample_input, patient_id=101)
    assert "predictions" in res
    assert "diabetes" in res["predictions"]
    assert "cardio" in res["predictions"]
    assert "ckd" in res["predictions"]

    # Test Module 3 SHAP Handoff payload structure
    handoff = res["module3_handoff"]
    assert handoff["patient_id"] == 101
    assert "transformed_features_for_shap" in handoff
    assert handoff["ready_for_explainability"] is True
    assert "diabetes" in handoff["transformed_features_for_shap"]
