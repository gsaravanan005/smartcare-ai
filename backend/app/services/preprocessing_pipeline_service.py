import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from sklearn.model_selection import train_test_split

from ..core.config import settings
from .dataset_loader_service import DatasetLoaderService
from .dataset_profiler_service import DatasetProfilerService
from .missing_value_service import MissingValueService
from .outlier_service import OutlierService
from .encoding_scaling_service import EncodingScalingService
from .feature_engineering_service import FeatureEngineeringService
from .feature_selection_service import FeatureSelectionService
from .imbalance_service import ImbalanceService
from .feature_mapping_service import FeatureMappingService

class PreprocessingPipelineService:

    @classmethod
    def run_pipeline(
        cls,
        dataset_name: str,
        imputation_method: str = "median",
        outlier_strategy: str = "iqr_capping",
        encoding_strategy: str = "onehot",
        scaling_strategy: str = "standard",
        feature_selection_method: str = "select_k_best",
        k_features: int = 15,
        class_imbalance_method: str = "smote",
        missingness_injection_scenario: Optional[str] = None,
        missingness_injection_rate: float = 0.0,
        random_seed: int = 42,
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15
    ) -> Dict[str, Any]:
        """
        Executes a complete, leakage-free reproducible preprocessing pipeline.
        Strict Guarantee: Preprocessing parameters are fitted ONLY on the Training split.
        """
        # 1. Load Dataset & Separate Target
        df_raw, target_col = DatasetLoaderService.load_dataset(dataset_name)
        
        # Controlled missingness injection for research experiments if requested
        injection_info = {}
        if missingness_injection_scenario and missingness_injection_rate > 0:
            df_raw, injection_info = MissingValueService.inject_controlled_missingness(
                df_raw, scenario=missingness_injection_scenario, rate=missingness_injection_rate, random_seed=random_seed
            )

        X = df_raw.drop(columns=[target_col])
        if 'id' in X.columns:
            X = X.drop(columns=['id'])
        y = df_raw[target_col]

        # 2. Stratified Train / Validation / Test Split (Strict Leakage Prevention Step 1)
        val_test_ratio = val_ratio + test_ratio
        val_relative_ratio = val_ratio / val_test_ratio

        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=val_test_ratio, random_state=random_seed, stratify=y
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=(1.0 - val_relative_ratio), random_state=random_seed, stratify=y_temp
        )

        pipeline_artifacts = {
            "dataset_name": dataset_name,
            "target_col": target_col,
            "random_seed": random_seed,
            "config": {
                "imputation_method": imputation_method,
                "outlier_strategy": outlier_strategy,
                "encoding_strategy": encoding_strategy,
                "scaling_strategy": scaling_strategy,
                "feature_selection_method": feature_selection_method,
                "k_features": k_features,
                "class_imbalance_method": class_imbalance_method
            }
        }

        # 3. Step A: Feature Engineering (Applied per partition)
        X_train_eng, eng_docs = FeatureEngineeringService.apply_feature_engineering(dataset_name, X_train)
        X_val_eng, _ = FeatureEngineeringService.apply_feature_engineering(dataset_name, X_val)
        X_test_eng, _ = FeatureEngineeringService.apply_feature_engineering(dataset_name, X_test)
        pipeline_artifacts["engineered_features_docs"] = eng_docs

        # 4. Step B: Fit Imputer ONLY on X_train_eng
        imputer, num_cols, cat_cols = MissingValueService.fit_imputer(X_train_eng, method=imputation_method)
        pipeline_artifacts["imputer"] = imputer
        pipeline_artifacts["numeric_cols"] = num_cols
        pipeline_artifacts["categorical_cols"] = cat_cols

        X_train_imp = MissingValueService.transform_imputation(imputer, X_train_eng, num_cols, cat_cols)
        X_val_imp = MissingValueService.transform_imputation(imputer, X_val_eng, num_cols, cat_cols)
        X_test_imp = MissingValueService.transform_imputation(imputer, X_test_eng, num_cols, cat_cols)

        # 5. Step C: Fit Outlier Bounds ONLY on X_train_imp
        outlier_bounds = OutlierService.fit_outlier_bounds(X_train_imp, method="iqr")
        pipeline_artifacts["outlier_bounds"] = outlier_bounds

        X_train_out, train_outliers = OutlierService.apply_outlier_treatment(X_train_imp, outlier_bounds, strategy=outlier_strategy)
        X_val_out, _ = OutlierService.apply_outlier_treatment(X_val_imp, outlier_bounds, strategy=outlier_strategy)
        X_test_out, _ = OutlierService.apply_outlier_treatment(X_test_imp, outlier_bounds, strategy=outlier_strategy)
        pipeline_artifacts["outlier_counts"] = train_outliers

        # 6. Step D: Fit Encoders & Scalers ONLY on X_train_out
        enc_scale_artifacts, num_cols_out, cat_cols_out = EncodingScalingService.fit_encoders_and_scalers(
            X_train_out, encoding_strategy=encoding_strategy, scaling_strategy=scaling_strategy
        )
        pipeline_artifacts.update(enc_scale_artifacts)

        X_train_trans = EncodingScalingService.transform_features(X_train_out, enc_scale_artifacts, num_cols_out, cat_cols_out)
        X_val_trans = EncodingScalingService.transform_features(X_val_out, enc_scale_artifacts, num_cols_out, cat_cols_out)
        X_test_trans = EncodingScalingService.transform_features(X_test_out, enc_scale_artifacts, num_cols_out, cat_cols_out)

        # 7. Step E: Feature Selection ONLY on X_train_trans, y_train
        selector_info = FeatureSelectionService.fit_feature_selector(
            X_train_trans, y_train, method=feature_selection_method, k=k_features
        )
        pipeline_artifacts["feature_selector"] = selector_info

        X_train_sel = FeatureSelectionService.transform_features(X_train_trans, selector_info)
        X_val_sel = FeatureSelectionService.transform_features(X_val_trans, selector_info)
        X_test_sel = FeatureSelectionService.transform_features(X_test_trans, selector_info)

        # 8. Step F: Class Imbalance Resampling ONLY on X_train_sel, y_train
        X_train_final, y_train_final, imbalance_info = ImbalanceService.apply_imbalance_handling(
            X_train_sel, y_train, method=class_imbalance_method, random_seed=random_seed
        )
        pipeline_artifacts["imbalance_info"] = imbalance_info

        # Note: Validation and Test splits are NOT resampled!
        X_val_final, y_val_final = X_val_sel.copy(), y_val.copy()
        X_test_final, y_test_final = X_test_sel.copy(), y_test.copy()

        # 9. Compute VIF on final training features
        vif_summary = DatasetProfilerService.calculate_vif(X_train_final, X_train_final.columns.tolist())

        # 10. Save Processed Datasets & Module 2 Artifacts
        version_str = f"v1_{dataset_name}_{random_seed}"
        exported_files = cls._export_artifacts(
            dataset_name, version_str,
            X_train_final, y_train_final,
            X_val_final, y_val_final,
            X_test_final, y_test_final,
            pipeline_artifacts,
            vif_summary
        )

        return {
            "status": "SUCCESS",
            "experiment_id": f"EXP_{dataset_name.upper()}_{random_seed}",
            "dataset_name": dataset_name,
            "pipeline_version": version_str,
            "train_shape": [int(X_train_final.shape[0]), int(X_train_final.shape[1])],
            "val_shape": [int(X_val_final.shape[0]), int(X_val_final.shape[1])],
            "test_shape": [int(X_test_final.shape[0]), int(X_test_final.shape[1])],
            "selected_features": X_train_final.columns.tolist(),
            "vif_summary": vif_summary,
            "injection_info": injection_info,
            "artifacts_exported": exported_files,
            "message": f"Successfully executed leakage-free pipeline for dataset '{dataset_name}'."
        }

    @classmethod
    def _export_artifacts(
        cls,
        dataset_name: str,
        version: str,
        X_train: pd.DataFrame, y_train: pd.Series,
        X_val: pd.DataFrame, y_val: pd.Series,
        X_test: pd.DataFrame, y_test: pd.Series,
        pipeline_artifacts: Dict[str, Any],
        vif_summary: Dict[str, float]
    ) -> List[str]:
        os.makedirs(settings.PROCESSED_DATA_DIR, exist_ok=True)
        os.makedirs(settings.ARTIFACTS_DIR, exist_ok=True)

        # 1. Export Parquet / CSV splits to processed data directory
        train_df = pd.concat([X_train, y_train], axis=1)
        val_df = pd.concat([X_val, y_val], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)

        train_path = os.path.join(settings.PROCESSED_DATA_DIR, f"{dataset_name}_train.csv")
        val_path = os.path.join(settings.PROCESSED_DATA_DIR, f"{dataset_name}_val.csv")
        test_path = os.path.join(settings.PROCESSED_DATA_DIR, f"{dataset_name}_test.csv")

        train_df.to_csv(train_path, index=False)
        val_df.to_csv(val_path, index=False)
        test_df.to_csv(test_path, index=False)

        # Also save copies into Module 2 input folder
        m2_train_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_train.csv")
        m2_val_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_val.csv")
        m2_test_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_test.csv")

        train_df.to_csv(m2_train_path, index=False)
        val_df.to_csv(m2_val_path, index=False)
        test_df.to_csv(m2_test_path, index=False)

        # 2. Serialize Fitted Pipeline Artifact
        pipeline_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_pipeline.joblib")
        # Save picklable subset
        saveable_pipeline = {
            "dataset_name": dataset_name,
            "target_col": pipeline_artifacts["target_col"],
            "config": pipeline_artifacts["config"],
            "numeric_cols": pipeline_artifacts.get("numeric_cols", []),
            "categorical_cols": pipeline_artifacts.get("categorical_cols", []),
            "imputer": pipeline_artifacts.get("imputer"),
            "outlier_bounds": pipeline_artifacts.get("outlier_bounds"),
            "scaler": pipeline_artifacts.get("scaler"),
            "encoder": pipeline_artifacts.get("encoder"),
            "feature_selector": pipeline_artifacts.get("feature_selector"),
            "selected_features": X_train.columns.tolist()
        }
        joblib.dump(saveable_pipeline, pipeline_path)

        # 3. Export Metadata JSON files for Module 2 handoff
        target_path = os.path.join(settings.ARTIFACTS_DIR, "target_definitions.json")
        targets = {
            "diabetes": {"col": "Diabetes_binary", "type": "binary"},
            "cardio": {"col": "cardio", "type": "binary"},
            "ckd": {"col": "classification", "type": "binary"}
        }
        with open(target_path, "w") as f:
            json.dump(targets, f, indent=2)

        mapping_path = os.path.join(settings.ARTIFACTS_DIR, "feature_mapping.json")
        with open(mapping_path, "w") as f:
            json.dump(FeatureMappingService.get_common_feature_schema(), f, indent=2)

        meta_path = os.path.join(settings.ARTIFACTS_DIR, "experiment_metadata.json")
        meta = {
            "dataset_name": dataset_name,
            "version": version,
            "selected_features": X_train.columns.tolist(),
            "vif_summary": vif_summary,
            "train_size": len(train_df),
            "val_size": len(val_df),
            "test_size": len(test_df)
        }
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        return [m2_train_path, m2_val_path, m2_test_path, pipeline_path, target_path, mapping_path, meta_path]

    @classmethod
    def transform_single_patient_input(cls, dataset_name: str, patient_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies a fitted saved pipeline to a new patient's health-data submission.
        """
        pipeline_path = os.path.join(settings.ARTIFACTS_DIR, f"{dataset_name}_pipeline.joblib")
        if not os.path.exists(pipeline_path):
            # Run default pipeline once if not pre-built
            cls.run_pipeline(dataset_name)

        pipeline = joblib.load(pipeline_path)
        
        # 1. Map patient input to original feature dictionary
        mapped_dict = FeatureMappingService.map_patient_input_to_features(patient_input, dataset_name)
        df_patient = pd.DataFrame([mapped_dict])

        # 2. Feature Engineering
        df_eng, _ = FeatureEngineeringService.apply_feature_engineering(dataset_name, df_patient)

        # 3. Imputation
        num_cols = pipeline.get("numeric_cols", [])
        cat_cols = pipeline.get("categorical_cols", [])
        imputer = pipeline.get("imputer")
        if imputer:
            df_imp = MissingValueService.transform_imputation(imputer, df_eng, num_cols, cat_cols)
        else:
            df_imp = df_eng

        # 4. Outlier Treatment
        bounds = pipeline.get("outlier_bounds", {})
        df_out, _ = OutlierService.apply_outlier_treatment(df_imp, bounds, strategy=pipeline["config"]["outlier_strategy"])

        # 5. Encoding & Scaling
        artifacts = {}
        if pipeline.get("scaler"): artifacts["scaler"] = pipeline["scaler"]
        if pipeline.get("encoder"): artifacts["encoder"] = pipeline["encoder"]
        artifacts["encoding_strategy"] = pipeline["config"]["encoding_strategy"]

        df_trans = EncodingScalingService.transform_features(df_out, artifacts, num_cols, cat_cols)

        # 6. Feature Subset Selection
        selected_features = pipeline.get("selected_features", [])
        for sf in selected_features:
            if sf not in df_trans.columns:
                df_trans[sf] = 0.0

        final_df = df_trans[selected_features]
        return final_df.to_dict(orient="records")[0]
