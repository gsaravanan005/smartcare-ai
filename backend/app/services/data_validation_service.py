import os
import json
import joblib
import pandas as pd
from typing import Dict, Any, Tuple
from ..core.config import settings

class DataValidationService:

    TARGET_MAP = {
        "diabetes": "Diabetes_binary",
        "cardio": "cardio",
        "ckd": "classification"
    }

    @classmethod
    def validate_dataset_artifacts(cls, dataset_name: str) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, Dict[str, Any]]:
        target_col = cls.TARGET_MAP.get(dataset_name)
        if not target_col:
            raise ValueError(f"Unknown dataset '{dataset_name}'. Available: {list(cls.TARGET_MAP.keys())}")

        train_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_train.csv")
        val_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_val.csv")
        test_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_test.csv")
        pipeline_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_pipeline.joblib")

        # 1. File existence checks
        for p in [train_path, val_path, test_path, pipeline_path]:
            if not os.path.exists(p):
                raise FileNotFoundError(f"Required Module 1 artifact missing: '{p}'. Run Module 1 pipeline first.")

        # 2. Read datasets
        df_train = pd.read_csv(train_path)
        df_val = pd.read_csv(val_path)
        df_test = pd.read_csv(test_path)
        pipeline = joblib.load(pipeline_path)

        # 3. Target existence checks
        for name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
            if target_col not in df.columns:
                raise KeyError(f"Target column '{target_col}' missing from {name} split.")

        # 4. Target separation
        X_train = df_train.drop(columns=[target_col])
        y_train = df_train[target_col]

        X_val = df_val.drop(columns=[target_col])
        y_val = df_val[target_col]

        X_test = df_test.drop(columns=[target_col])
        y_test = df_test[target_col]

        # 5. Feature alignment & ordering verification
        expected_features = pipeline.get("selected_features", X_train.columns.tolist())
        
        for name, X_df in [("X_train", X_train), ("X_val", X_val), ("X_test", X_test)]:
            if list(X_df.columns) != expected_features:
                # Re-order if features present
                missing_feats = [f for f in expected_features if f not in X_df.columns]
                if missing_feats:
                    raise ValueError(f"Feature mismatch in {name}. Missing expected features: {missing_feats}")

        X_train = X_train[expected_features]
        X_val = X_val[expected_features]
        X_test = X_test[expected_features]

        # 6. Null checks
        for name, X_df in [("X_train", X_train), ("X_val", X_val), ("X_test", X_test)]:
            if X_df.isnull().sum().sum() > 0:
                raise ValueError(f"Unexpected NaN values found in processed split '{name}'. Imputation step incomplete.")

        meta = {
            "dataset_name": dataset_name,
            "target_col": target_col,
            "feature_names": expected_features,
            "num_features": len(expected_features),
            "train_size": len(X_train),
            "val_size": len(X_val),
            "test_size": len(X_test),
            "pipeline_config": pipeline.get("config", {})
        }

        return X_train, y_train, X_val, y_val, X_test, y_test, meta
