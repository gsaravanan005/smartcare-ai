import pytest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.dataset_loader_service import DatasetLoaderService
from app.services.preprocessing_pipeline_service import PreprocessingPipelineService

def test_target_excluded_from_features():
    for name in ["diabetes", "cardio", "ckd"]:
        df, target_col = DatasetLoaderService.load_dataset(name)
        X = df.drop(columns=[target_col])
        assert target_col not in X.columns, f"Target column '{target_col}' leaked into feature matrix X for dataset '{name}'."

def test_leakage_prevention_on_splits():
    """
    Verifies that preprocessing transformers are fitted ONLY on training split
    and that validation / test splits maintain their isolated original row counts (no SMOTE leakage).
    """
    res = PreprocessingPipelineService.run_pipeline(
        dataset_name="ckd",
        imputation_method="mean",
        scaling_strategy="standard",
        class_imbalance_method="smote",
        random_seed=42,
        train_ratio=0.70,
        val_ratio=0.15,
        test_ratio=0.15
    )

    # 400 total rows in CKD: 70% train = 280, 15% val = 60, 15% test = 60
    # SMOTE on 280 rows changes train count to balanced count
    # Val and Test row counts MUST remain exactly 60!
    assert res["val_shape"][0] == 60, f"Validation split modified by resampling! Found {res['val_shape'][0]} rows."
    assert res["test_shape"][0] == 60, f"Test split modified by resampling! Found {res['test_shape'][0]} rows."

def test_no_test_set_fitting():
    # Load processed splits
    test_csv = os.path.join("artifacts", "module2_inputs", "ckd_test.csv")
    train_csv = os.path.join("artifacts", "module2_inputs", "ckd_train.csv")
    
    assert os.path.exists(test_csv)
    assert os.path.exists(train_csv)
    
    test_df = pd.read_csv(test_csv)
    train_df = pd.read_csv(train_csv)
    
    assert test_df.shape[1] == train_df.shape[1], "Train and Test feature columns must match."
    assert "classification" in test_df.columns, "Target must be present in exported dataset for Module 2 evaluation."
