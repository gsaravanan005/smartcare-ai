import os
import sys
import json
import logging
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..core.config import settings
if settings.BASE_DIR not in sys.path:
    sys.path.insert(0, settings.BASE_DIR)
from .preprocessing_pipeline_service import PreprocessingPipelineService
from .explanation_service import ExplanationService

logger = logging.getLogger(__name__)

class PredictionService:

    @classmethod
    def predict_multi_disease_risk(cls, patient_input: Dict[str, Any], patient_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes multi-disease risk assessment across Diabetes (T2D), Cardiovascular Disease (CVD),
        and Chronic Kidney Disease (CKD) using the trained Multi-Task Learning (MTL) Shared Encoder Network.
        Maintains complete backward compatibility with existing API formats, dashboards, and reports.
        """
        mtl_model_path = os.path.join(settings.BASE_DIR, "models", "multitask", "smartcare_mtl_model.joblib")
        
        # If MTL model is available, use genuine Multi-Task Learning prediction engine
        if os.path.exists(mtl_model_path):
            return cls._predict_with_mtl_model(patient_input, patient_id=patient_id, model_path=mtl_model_path)

        # Fallback to independent models if MTL artifact is not found
        return cls._predict_with_independent_models(patient_input, patient_id=patient_id)

    @classmethod
    def _predict_with_mtl_model(cls, patient_input: Dict[str, Any], patient_id: Optional[int], model_path: str) -> Dict[str, Any]:
        """Runs inference and SHAP explainability through the shared representation MTL model."""
        from ml.multitask.dataset import MTLDatasetManager
        from ml.multitask.calibration import MultiTaskCalibrator

        bundle = joblib.load(model_path)
        model = bundle["model"]
        feature_names = bundle.get("feature_names", [])

        # Load Scaler & Preprocessing
        prep_path = os.path.join(settings.BASE_DIR, "models", "multitask", "preprocessing.pkl")
        data_mgr = MTLDatasetManager()
        if os.path.exists(prep_path):
            prep_data = joblib.load(prep_path)
            data_mgr.scaler = prep_data.get("scaler")
            data_mgr.imputer = prep_data.get("imputer")

        # Load Thresholds
        th_path = os.path.join(settings.BASE_DIR, "models", "multitask", "thresholds.json")
        thresholds = {"t2d": 0.40, "cvd": 0.35, "ckd": 0.35}
        if os.path.exists(th_path):
            try:
                with open(th_path, "r") as f:
                    th_info = json.load(f)
                    thresholds.update(th_info.get("thresholds", {}))
            except Exception as e:
                logger.warning(f"Error loading thresholds.json: {e}")

        # Load Calibrators
        calibrators = {}
        for task in ["t2d", "cvd", "ckd"]:
            cal_file = os.path.join(settings.BASE_DIR, "models", "multitask", f"calibration_{task}.pkl")
            if os.path.exists(cal_file):
                calibrators[task] = joblib.load(cal_file)

        # 1. Harmonize and scale input features into shared feature vector
        df_patient = data_mgr.harmonize_patient_input(patient_input)
        if feature_names:
            df_patient = df_patient[feature_names]

        # 2. Joint forward pass on single shared encoder
        raw_probs_dict, Z = model.forward(df_patient, training=False)

        results = {}
        features_transformed = {}
        shap_explanations = {}

        task_mapping = {
            "diabetes": "t2d",
            "cardio": "cvd",
            "ckd": "ckd"
        }

        # Background data for SHAP
        try:
            background_df = pd.read_csv(os.path.join(settings.ARTIFACTS_DIR, "diabetes_val.csv"))
            bg_harmonized = data_mgr.harmonize_t2d_features(background_df)
            if data_mgr.imputer is not None:
                bg_imp = pd.DataFrame(data_mgr.imputer.transform(bg_harmonized), columns=feature_names)
            else:
                bg_imp = bg_harmonized.fillna(0.0)
            if data_mgr.scaler is not None:
                bg_scaled = pd.DataFrame(data_mgr.scaler.transform(bg_imp), columns=feature_names)
            else:
                bg_scaled = bg_imp
        except Exception:
            bg_scaled = df_patient

        for disease, task_key in task_mapping.items():
            raw_p = float(raw_probs_dict[task_key][0])

            # Apply probability calibration
            if task_key in calibrators and calibrators[task_key].is_fitted:
                calib_p = float(calibrators[task_key].predict_proba(np.array([raw_p]))[0])
            else:
                calib_p = raw_p

            calib_p = min(0.9999, max(0.0001, calib_p))
            prob_round = round(calib_p, 4)
            pct = round(calib_p * 100.0, 1)

            # Assign risk category
            if pct < 30.0:
                risk_cat = "LOW"
            elif pct <= 60.0:
                risk_cat = "MODERATE"
            else:
                risk_cat = "HIGH"

            th = thresholds.get(task_key, 0.40)
            model_ver = "smartcare_mtl_v1"
            calib_ver = "platt_sigmoid"

            results[disease] = {
                "disease": disease.upper(),
                "probability": prob_round,
                "risk_percentage": pct,
                "risk_category": risk_cat,
                "decision_threshold": th,
                "model_version": model_ver,
                "calibration_version": calib_ver,
                "timestamp": datetime.utcnow().isoformat()
            }
            features_transformed[disease] = df_patient.to_dict(orient="records")[0]

            # Generate task-specific SHAP explanation
            try:
                task_wrapper = {
                    "model": model,
                    "model_version": model_ver,
                    "feature_names": feature_names
                }
                # Create a single task predictor for SHAP explainer
                class SingleTaskPredictor:
                    def __init__(self, m, t):
                        self.m = m
                        self.t = t
                    def predict_proba(self, X):
                        if isinstance(X, np.ndarray):
                            X = pd.DataFrame(X, columns=feature_names)
                        p = self.m.forward(X, training=False)[0][self.t]
                        return np.column_stack([1.0 - p, p])
                    def predict(self, X):
                        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

                task_wrapper["model"] = SingleTaskPredictor(model, task_key)
                exp_res = ExplanationService.generate_local_explanation(
                    disease, task_wrapper, df_patient, bg_scaled, top_k=5
                )
                shap_explanations[disease] = exp_res.get("top_risk_factors", [])
            except Exception as e:
                logger.error(f"Error computing MTL SHAP for {disease}: {e}")
                shap_explanations[disease] = []

        module3_handoff = {
            "patient_id": patient_id,
            "prediction_timestamp": datetime.utcnow().isoformat(),
            "disease_risks": results,
            "transformed_features_for_shap": features_transformed,
            "ready_for_explainability": True
        }

        return {
            "patient_id": patient_id,
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": results,
            "shap": shap_explanations,
            "module3_handoff": module3_handoff,
            "disclaimer": "SmartCare AI risk estimates are machine-learning decision-support predictions and must not be interpreted as confirmed medical diagnoses."
        }

    @classmethod
    def _predict_with_independent_models(cls, patient_input: Dict[str, Any], patient_id: Optional[int] = None) -> Dict[str, Any]:
        """Fallback predictor using baseline independent models."""
        results = {}
        features_transformed = {}
        shap_explanations = {}

        for disease in ["diabetes", "cardio", "ckd"]:
            trans_dict = PreprocessingPipelineService.transform_single_patient_input(disease, patient_input)
            features_transformed[disease] = trans_dict
            df_patient = pd.DataFrame([trans_dict])

            model_path = os.path.join(settings.BASE_DIR, "models", disease, f"{disease}_best_model.joblib")
            
            if not os.path.exists(model_path):
                prob = cls._fallback_heuristic_risk(disease, patient_input)
                model_ver = f"{disease}_heuristic_v1"
                calib_ver = "uncalibrated"
                th = 0.5
                shap_explanations[disease] = []
            else:
                bundle = joblib.load(model_path)
                model = bundle["model"]
                th = bundle.get("threshold", 0.5)
                model_ver = bundle.get("model_version", f"{disease}_model_v1")
                calib_ver = bundle.get("calibration_method", "platt_sigmoid")
                
                model_features = bundle.get("feature_names", df_patient.columns.tolist())
                for mf in model_features:
                    if mf not in df_patient.columns:
                        df_patient[mf] = 0.0
                df_patient = df_patient[model_features]

                if hasattr(model, "predict_proba"):
                    prob = float(model.predict_proba(df_patient)[:, 1][0])
                else:
                    prob = float(model.predict(df_patient)[0])

                try:
                    val_df = pd.read_csv(os.path.join(settings.ARTIFACTS_DIR, f"{disease}_val.csv"))
                    target_cols = {"diabetes": "Diabetes_binary", "cardio": "cardio", "ckd": "classification"}
                    X_background = val_df.drop(columns=[target_cols[disease]])
                    if 'id' in X_background.columns:
                        X_background = X_background.drop(columns=['id'])
                    
                    exp_res = ExplanationService.generate_local_explanation(disease, bundle, df_patient, X_background, top_k=5)
                    shap_explanations[disease] = exp_res.get("top_risk_factors", [])
                except Exception as e:
                    logger.error(f"Error computing SHAP for {disease}: {e}")
                    shap_explanations[disease] = []

            prob_round = round(prob, 4)
            pct = round(prob * 100, 1)

            if pct < 30.0:
                risk_cat = "LOW"
            elif pct <= 60.0:
                risk_cat = "MODERATE"
            else:
                risk_cat = "HIGH"

            results[disease] = {
                "disease": disease.upper(),
                "probability": prob_round,
                "risk_percentage": pct,
                "risk_category": risk_cat,
                "decision_threshold": th,
                "model_version": model_ver,
                "calibration_version": calib_ver,
                "timestamp": datetime.utcnow().isoformat()
            }

        module3_handoff = {
            "patient_id": patient_id,
            "prediction_timestamp": datetime.utcnow().isoformat(),
            "disease_risks": results,
            "transformed_features_for_shap": features_transformed,
            "ready_for_explainability": True
        }

        return {
            "patient_id": patient_id,
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": results,
            "shap": shap_explanations,
            "module3_handoff": module3_handoff,
            "disclaimer": "SmartCare AI risk estimates are machine-learning decision-support predictions and must not be interpreted as confirmed medical diagnoses."
        }

    @classmethod
    def _fallback_heuristic_risk(cls, disease: str, patient_input: Dict[str, Any]) -> float:
        """Fallback clinical risk estimation if models not yet compiled."""
        age = patient_input.get("age", 45)
        high_bp = patient_input.get("high_bp", 0)
        high_chol = patient_input.get("high_chol", 0)
        ap_hi = patient_input.get("ap_hi", 120)
        sc = patient_input.get("serum_creatinine", 1.0)
        smoker = patient_input.get("smoker", 0)

        base = 0.10
        if disease == "diabetes":
            base += (0.25 if high_bp else 0.0) + (0.20 if high_chol else 0.0) + (0.15 if age > 50 else 0.0)
        elif disease == "cardio":
            base += (0.30 if ap_hi > 140 else 0.10 if ap_hi > 130 else 0.0) + (0.20 if smoker else 0.0) + (0.15 if age > 55 else 0.0)
        elif disease == "ckd":
            base += (0.35 if sc > 1.4 else 0.15 if sc > 1.2 else 0.0) + (0.20 if high_bp else 0.0) + (0.10 if age > 60 else 0.0)

        return min(0.95, max(0.05, base))
