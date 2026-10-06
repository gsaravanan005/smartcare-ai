import pytest
import os
import sys
import joblib
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.preprocessing_pipeline_service import PreprocessingPipelineService

def test_pipeline_execution():
    res = PreprocessingPipelineService.run_pipeline(
        dataset_name="ckd",
        imputation_method="median",
        outlier_strategy="iqr_capping",
        encoding_strategy="onehot",
        scaling_strategy="standard",
        feature_selection_method="select_k_best",
        k_features=10,
        class_imbalance_method="smote"
    )

    assert res["status"] == "SUCCESS"
    assert res["train_shape"][0] > 0
    assert len(res["selected_features"]) == 10
    assert len(res["artifacts_exported"]) > 0

def test_pipeline_deserialization_and_single_patient_transform():
    patient_input = {
        "age": 45,
        "ap_hi": 130,
        "ap_lo": 85,
        "glucose": 110,
        "serum_creatinine": 1.1,
        "blood_urea": 32.0,
        "hemoglobin": 13.5,
        "high_bp": 1,
        "smoker": 0
    }

    transformed = PreprocessingPipelineService.transform_single_patient_input("ckd", patient_input)
    assert isinstance(transformed, dict)
    assert len(transformed) == 10, "Transformed single patient output should match selected feature count."
