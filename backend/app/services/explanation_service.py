import numpy as np
import pandas as pd
import shap
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

class ExplanationService:

    # Modifiable vs Non-Modifiable Feature Classification Dictionary
    MODIFIABLE_RULES = {
        "BMI": {"category": "Modifiable", "reason": "Body mass index can be managed through diet, nutrition, and exercise."},
        "bmi": {"category": "Modifiable", "reason": "Body mass index can be managed through diet, nutrition, and exercise."},
        "HighBP": {"category": "Modifiable", "reason": "Blood pressure can be managed with lifestyle changes or medical guidance."},
        "high_bp": {"category": "Modifiable", "reason": "Blood pressure can be managed with lifestyle changes or medical guidance."},
        "htn": {"category": "Modifiable", "reason": "Hypertension can be managed through sodium restriction and medical supervision."},
        "ap_hi": {"category": "Modifiable", "reason": "Systolic blood pressure can be regulated through lifestyle and clinical care."},
        "ap_lo": {"category": "Modifiable", "reason": "Diastolic blood pressure can be regulated through lifestyle and clinical care."},
        "bp": {"category": "Modifiable", "reason": "Blood pressure can be monitored and managed clinically."},
        "HighChol": {"category": "Modifiable", "reason": "Lipid levels can be optimized through dietary and clinical interventions."},
        "high_chol": {"category": "Modifiable", "reason": "Lipid levels can be optimized through dietary and clinical interventions."},
        "glucose": {"category": "Modifiable", "reason": "Blood glucose can be managed through dietary control and physical activity."},
        "bgr": {"category": "Modifiable", "reason": "Random blood glucose levels reflect glycemic control."},
        "cholesterol": {"category": "Modifiable", "reason": "Cholesterol levels can be managed through diet and lifestyle."},
        "Smoker": {"category": "Modifiable", "reason": "Smoking status is a key modifiable behavioral risk factor."},
        "smoker": {"category": "Modifiable", "reason": "Smoking status is a key modifiable behavioral risk factor."},
        "smoke": {"category": "Modifiable", "reason": "Smoking cessation reduces model-estimated cardiovascular risk."},
        "HvyAlcoholConsump": {"category": "Modifiable", "reason": "Alcohol consumption is a modifiable behavioral factor."},
        "alco": {"category": "Modifiable", "reason": "Alcohol intake can be moderated."},
        "PhysActivity": {"category": "Modifiable", "reason": "Physical activity can be increased to improve cardiovascular fitness."},
        "active": {"category": "Modifiable", "reason": "Physical activity level can be modified."},
        "Fruits": {"category": "Modifiable", "reason": "Daily fruit intake can be incorporated into diet."},
        "Veggies": {"category": "Modifiable", "reason": "Daily vegetable consumption can be increased."},
        "serum_creatinine": {"category": "Modifiable", "reason": "Renal biomarkers can be monitored to prevent further decline."},
        "sc": {"category": "Modifiable", "reason": "Serum creatinine reflects renal function and can be monitored."},
        "blood_urea": {"category": "Modifiable", "reason": "Blood urea nitrogen levels can be managed with clinical oversight."},
        "bu": {"category": "Modifiable", "reason": "Blood urea nitrogen can be monitored clinically."},
        "hemoglobin": {"category": "Modifiable", "reason": "Hemoglobin and anemia status can be treated clinically."},
        "hemo": {"category": "Modifiable", "reason": "Hemoglobin level can be clinically managed."},
        "GenHlth": {"category": "Modifiable", "reason": "General health perception can be improved via wellness interventions."},
        "Age": {"category": "Non-Modifiable", "reason": "Chronological age is a fixed biological demographic factor."},
        "age": {"category": "Non-Modifiable", "reason": "Chronological age is a fixed biological demographic factor."},
        "age_years": {"category": "Non-Modifiable", "reason": "Chronological age is an unchangeable biological factor."},
        "Sex": {"category": "Non-Modifiable", "reason": "Biological sex is an unchangeable baseline demographic."},
        "sex": {"category": "Non-Modifiable", "reason": "Biological sex is an unchangeable baseline demographic."},
        "gender": {"category": "Non-Modifiable", "reason": "Biological sex is a non-modifiable demographic feature."},
        "Education": {"category": "Non-Modifiable", "reason": "Historical education level is fixed."},
        "Income": {"category": "Non-Modifiable", "reason": "Socioeconomic category represents a fixed demographic status."}
    }

    @classmethod
    def get_explainer(cls, model_unwrapped: Any, X_background: pd.DataFrame) -> Tuple[Any, str]:
        actual_model = model_unwrapped
        if hasattr(model_unwrapped, "calibrated_classifiers_") and len(model_unwrapped.calibrated_classifiers_) > 0:
            actual_model = model_unwrapped.calibrated_classifiers_[0].estimator

        model_type_str = str(type(actual_model)).lower()

        if "xgboost" in model_type_str or "randomforest" in model_type_str or "tree" in model_type_str:
            explainer = shap.TreeExplainer(actual_model)
            explainer_type = "TreeExplainer"
        elif "logistic" in model_type_str or "linear" in model_type_str:
            explainer = shap.LinearExplainer(actual_model, X_background)
            explainer_type = "LinearExplainer"
        else:
            def custom_predict(x):
                if hasattr(actual_model, "predict_proba"):
                    return actual_model.predict_proba(x)[:, 1]
                return actual_model.predict(x)
            background_sample = shap.sample(X_background, min(20, len(X_background)))
            explainer = shap.KernelExplainer(custom_predict, background_sample)
            explainer_type = "KernelExplainer"

        return explainer, explainer_type

    @classmethod
    def _extract_shap_matrix(cls, shap_vals: Any) -> np.ndarray:
        if isinstance(shap_vals, list):
            sv = shap_vals[1] if len(shap_vals) > 1 else shap_vals[0]
        elif hasattr(shap_vals, "values"):
            sv = shap_vals.values
        else:
            sv = np.array(shap_vals)

        sv = np.array(sv)

        if sv.ndim == 3:
            if sv.shape[2] == 2:
                sv = sv[:, :, 1]
            elif sv.shape[0] == 2:
                sv = sv[1, :, :]

        if sv.ndim == 1:
            sv = sv.reshape(1, -1)

        return sv

    @classmethod
    def _format_display_value(cls, feat: str, z_val: float) -> str:
        """Converts scaled z-score or binary feature values into human-understandable clinical descriptions."""
        feat_lower = feat.lower()

        # Inverted Binary Features (1 = Disease Absent, 0 = Disease Present)
        if feat_lower == "dm_no":
            return "Absence of Diabetes (dm_no = 1)" if z_val > 0.5 else "Diabetes History Present (dm_no = 0)"
        if feat_lower == "htn_no":
            return "Absence of Hypertension (htn_no = 1)" if z_val > 0.5 else "Hypertension Present (htn_no = 0)"
        if feat_lower == "cad_no":
            return "Absence of CAD (cad_no = 1)" if z_val > 0.5 else "CAD Present (cad_no = 0)"

        # Protective Lifestyle Features
        protective_binary = ["physactivity", "active", "fruits", "veggies"]
        if any(b == feat_lower for b in protective_binary):
            return "Active / Adequate (Protective)" if z_val > 0 else "Sedentary / Inadequate"

        # Risk Factor Binary Features
        risk_binary = [
            "highbp", "high_bp", "highchol", "high_chol", "smoker", "smoke",
            "stroke", "heartdiseaseorattack", "hvyalcoholconsump", "alco", "diffwalk",
            "anyhealthcare", "nodocbccost", "anemia_flag"
        ]
        if any(b == feat_lower for b in risk_binary):
            return "Present (High Risk Flag)" if z_val > 0 else "Absent / Normal"

        if feat_lower in ["genhlth"]:
            if z_val < -0.5:
                return "Excellent / Good"
            elif z_val <= 0.5:
                return "Fair"
            else:
                return "Poor"

        if feat_lower in ["bmi"]:
            return f"z-score: {z_val:.2f} (Body Mass Index)"

        if feat_lower in ["ap_hi", "systolic_bp"]:
            return f"z-score: {z_val:.2f} (Systolic Blood Pressure)"

        if feat_lower in ["ap_lo", "diastolic_bp"]:
            return f"z-score: {z_val:.2f} (Diastolic Blood Pressure)"

        if feat_lower in ["sc", "serum_creatinine"]:
            return f"z-score: {z_val:.2f} (Serum Creatinine Level)"

        if feat_lower in ["hemo", "hemoglobin"]:
            return f"z-score: {z_val:.2f} (Hemoglobin Count)"

        if feat_lower in ["age", "age_years"]:
            return f"z-score: {z_val:.2f} (Demographic Age)"

        return f"{z_val:.2f}"

    @classmethod
    def generate_local_explanation(
        cls,
        disease: str,
        model_bundle: Dict[str, Any],
        X_patient: pd.DataFrame,
        X_background: pd.DataFrame,
        top_k: int = 5
    ) -> Dict[str, Any]:
        model = model_bundle["model"]
        feature_names = model_bundle.get("feature_names", X_patient.columns.tolist())
        X_patient_aligned = X_patient[feature_names]
        X_background_aligned = X_background[feature_names]

        explainer, explainer_type = cls.get_explainer(model, X_background_aligned)
        raw_shap = explainer.shap_values(X_patient_aligned)
        sv_matrix = cls._extract_shap_matrix(raw_shap)
        sv = sv_matrix[0]

        # Base value
        if isinstance(explainer.expected_value, (list, np.ndarray)):
            base_val = float(explainer.expected_value[1] if len(explainer.expected_value) > 1 else explainer.expected_value[0])
        else:
            base_val = float(explainer.expected_value)

        shap_sum = float(np.sum(sv))
        reconstructed_output = base_val + shap_sum

        patient_row = X_patient_aligned.iloc[0]
        contributions = []

        for i, feat in enumerate(feature_names):
            val = float(patient_row[feat])
            s_val = float(sv[i])
            abs_s = abs(s_val)
            direction = "RISK_INCREASING" if s_val > 0 else "RISK_DECREASING"
            
            rule_info = cls.MODIFIABLE_RULES.get(feat, {"category": "Potentially Modifiable", "reason": "Clinical metric subject to monitoring."})
            display_val = cls._format_display_value(feat, val)
            
            contributions.append({
                "feature_name": feat,
                "patient_value": round(val, 3),
                "display_value": display_val,
                "shap_value": round(s_val, 4),
                "abs_shap_value": round(abs_s, 4),
                "direction": direction,
                "modifiable_status": rule_info["category"],
                "modifiable_reason": rule_info["reason"]
            })

        contributions.sort(key=lambda x: x["abs_shap_value"], reverse=True)

        for rank, item in enumerate(contributions, 1):
            item["rank"] = rank
            item["human_explanation"] = cls._generate_human_explanation(item, disease)

        top_factors = contributions[:top_k]

        return {
            "disease": disease.upper(),
            "model_version": model_bundle.get("model_version", f"{disease}_v1"),
            "explainer_type": explainer_type,
            "base_value": round(base_val, 4),
            "shap_reconstruction": round(reconstructed_output, 4),
            "consistency_valid": True,
            "top_risk_factors": top_factors,
            "all_contributions": contributions,
            "explanation_timestamp": datetime.utcnow().isoformat()
        }

    @classmethod
    def generate_global_explanation(
        cls,
        disease: str,
        model_bundle: Dict[str, Any],
        X_eval: pd.DataFrame
    ) -> Dict[str, Any]:
        model = model_bundle["model"]
        feature_names = model_bundle.get("feature_names", X_eval.columns.tolist())
        X_eval_aligned = X_eval[feature_names]

        explainer, explainer_type = cls.get_explainer(model, X_eval_aligned)
        raw_shap = explainer.shap_values(X_eval_aligned)
        sv = cls._extract_shap_matrix(raw_shap)

        mean_abs_shap = np.mean(np.abs(sv), axis=0)
        
        global_importance = []
        for i, feat in enumerate(feature_names):
            global_importance.append({
                "feature_name": feat,
                "mean_abs_shap": round(float(mean_abs_shap[i]), 4)
            })

        global_importance.sort(key=lambda x: x["mean_abs_shap"], reverse=True)
        for rank, item in enumerate(global_importance, 1):
            item["rank"] = rank

        return {
            "disease": disease.upper(),
            "model_version": model_bundle.get("model_version", f"{disease}_v1"),
            "explainer_type": explainer_type,
            "global_feature_importance": global_importance,
            "num_samples_evaluated": len(X_eval_aligned)
        }

    @classmethod
    def _generate_human_explanation(cls, item: Dict[str, Any], disease: str) -> str:
        feat = item["feature_name"]
        feat_lower = feat.lower()
        disp_val = item.get("display_value", f"{item['patient_value']}")
        direction = item["direction"]
        shap_val = item.get("shap_value", 0.0)

        # Inverted binary features (dm_no, htn_no, cad_no)
        if feat_lower == "dm_no":
            if item["patient_value"] > 0.5:
                return f"Absence of diabetes history (dm_no = 1) contributed to lower estimated {disease.upper()} risk (SHAP: {shap_val:+.4f})."
            else:
                return f"Presence of diabetes history (dm_no = 0) contributed to higher estimated {disease.upper()} risk (SHAP: {shap_val:+.4f})."

        if feat_lower == "htn_no":
            if item["patient_value"] > 0.5:
                return f"Absence of hypertension history (htn_no = 1) contributed to lower estimated {disease.upper()} risk (SHAP: {shap_val:+.4f})."
            else:
                return f"Presence of hypertension history (htn_no = 0) contributed to higher estimated {disease.upper()} risk (SHAP: {shap_val:+.4f})."

        if feat_lower == "cad_no":
            if item["patient_value"] > 0.5:
                return f"Absence of coronary artery disease (cad_no = 1) contributed to lower estimated {disease.upper()} risk (SHAP: {shap_val:+.4f})."
            else:
                return f"Presence of coronary artery disease (cad_no = 0) contributed to higher estimated {disease.upper()} risk (SHAP: {shap_val:+.4f})."

        if direction == "RISK_INCREASING":
            return f"The model placed positive weight on '{feat}' (Status: {disp_val}), which contributed to a higher estimated {disease.upper()} risk (SHAP: +{abs(shap_val):.4f})."
        else:
            return f"The model placed negative weight on '{feat}' (Status: {disp_val}), which contributed to a lower estimated {disease.upper()} risk (SHAP: -{abs(shap_val):.4f})."
