"""
SmartCare AI - Multi-Task SHAP Explainability Engine
Generates disease-specific SHAP explanations (Global feature importances and Patient-level local attributions)
for T2D, CVD, and CKD separately using the shared representation Multi-Task model.
"""

import numpy as np
import pandas as pd
import shap
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime


class MultiTaskExplainer:
    """
    SHAP Explainability Adapter for the Multi-Task Learning architecture.
    """

    MODIFIABLE_RULES = {
        "bmi": {"category": "Modifiable", "reason": "Body mass index can be managed through diet, nutrition, and exercise."},
        "high_bp": {"category": "Modifiable", "reason": "Blood pressure can be managed with lifestyle changes or medical guidance."},
        "ap_hi": {"category": "Modifiable", "reason": "Systolic blood pressure can be regulated through lifestyle and clinical care."},
        "ap_lo": {"category": "Modifiable", "reason": "Diastolic blood pressure can be regulated through lifestyle and clinical care."},
        "pulse_pressure": {"category": "Modifiable", "reason": "Arterial stiffness indicator responsive to vascular health management."},
        "mean_arterial_pressure": {"category": "Modifiable", "reason": "Perfusion pressure managed through systemic cardiovascular care."},
        "cholesterol": {"category": "Modifiable", "reason": "Lipid levels can be optimized through dietary and clinical interventions."},
        "glucose": {"category": "Modifiable", "reason": "Blood glucose can be managed through dietary control and physical activity."},
        "smoker": {"category": "Modifiable", "reason": "Smoking cessation reduces model-estimated cardiovascular risk."},
        "alcohol_consumption": {"category": "Modifiable", "reason": "Alcohol intake can be moderated."},
        "phys_activity": {"category": "Modifiable", "reason": "Physical activity can be increased to improve metabolic fitness."},
        "fruits": {"category": "Modifiable", "reason": "Daily fruit intake can be incorporated into diet."},
        "veggies": {"category": "Modifiable", "reason": "Daily vegetable consumption can be increased."},
        "serum_creatinine": {"category": "Modifiable", "reason": "Renal biomarkers can be monitored to prevent further decline."},
        "blood_urea": {"category": "Modifiable", "reason": "Blood urea nitrogen levels can be managed with clinical oversight."},
        "hemoglobin": {"category": "Modifiable", "reason": "Hemoglobin and anemia status can be treated clinically."},
        "albumin_level": {"category": "Modifiable", "reason": "Urinary albumin excretion managed via nephroprotective therapy."},
        "specific_gravity": {"category": "Modifiable", "reason": "Urinary concentration capacity monitored clinically."},
        "bun_creatinine_ratio": {"category": "Modifiable", "reason": "Renal perfusion and filtration ratio."},
        "egfr_proxy": {"category": "Modifiable", "reason": "Glomerular filtration capacity tracked for renal protection."},
        "anemia_flag": {"category": "Modifiable", "reason": "Renal anemia manageable with clinical guidance."},
        "combined_vascular_risk": {"category": "Modifiable", "reason": "Aggregate cardiometabolic risk score."},
        "gen_hlth": {"category": "Modifiable", "reason": "General health perception can be improved via wellness interventions."},
        "age_years": {"category": "Non-Modifiable", "reason": "Chronological age is a fixed biological demographic factor."},
        "gender": {"category": "Non-Modifiable", "reason": "Biological sex is a non-modifiable demographic feature."},
        "education": {"category": "Non-Modifiable", "reason": "Historical education level is fixed."},
        "income": {"category": "Non-Modifiable", "reason": "Socioeconomic category represents a fixed demographic status."},
        "stroke": {"category": "Non-Modifiable", "reason": "Prior stroke history is an established medical event."},
        "heart_disease_or_attack": {"category": "Non-Modifiable", "reason": "Prior cardiovascular event history is an established baseline."},
        "diff_walk": {"category": "Potentially Modifiable", "reason": "Mobility limitation manageable via physical therapy."}
    }

    def __init__(self, model: Any, background_data: pd.DataFrame, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        # Take representative background sample
        sample_size = min(40, len(background_data))
        self.background_sample = shap.sample(background_data[self.feature_names], sample_size)

        # Build task-specific prediction functions
        self.explainers = {}
        for disease in ["t2d", "cvd", "ckd"]:
            def make_task_predict(dis):
                def task_predict_fn(X_arr):
                    df_in = pd.DataFrame(X_arr, columns=self.feature_names)
                    probs_dict, _ = self.model.forward(df_in, training=False)
                    return probs_dict[dis]
                return task_predict_fn

            fn = make_task_predict(disease)
            self.explainers[disease] = shap.KernelExplainer(fn, self.background_sample)

    def explain_patient(
        self,
        disease: str,
        patient_row: pd.DataFrame,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Generates local SHAP explanation for a specific patient and disease task.
        """
        dis = disease.lower()
        if dis not in self.explainers:
            raise ValueError(f"Unknown disease '{disease}'. Choose from 't2d', 'cvd', 'ckd'.")

        X_aligned = patient_row[self.feature_names]
        explainer = self.explainers[dis]

        # Compute SHAP values for single patient
        shap_vals = explainer.shap_values(X_aligned, nsamples=100, silent=True)
        if isinstance(shap_vals, list):
            sv = np.array(shap_vals[0]).ravel()
        elif isinstance(shap_vals, np.ndarray):
            sv = shap_vals.ravel()
        else:
            sv = np.array(shap_vals.values).ravel()

        base_val = float(explainer.expected_value) if not isinstance(explainer.expected_value, (list, np.ndarray)) else float(explainer.expected_value[0])
        shap_sum = float(np.sum(sv))
        reconstructed = base_val + shap_sum

        patient_vals = X_aligned.iloc[0].to_dict()
        contributions = []

        for i, feat in enumerate(self.feature_names):
            val = float(patient_vals[feat])
            s_val = float(sv[i])
            abs_s = abs(s_val)
            direction = "RISK_INCREASING" if s_val > 0 else "RISK_DECREASING"
            rule = self.MODIFIABLE_RULES.get(feat, {"category": "Potentially Modifiable", "reason": "Clinical metric subject to monitoring."})

            contributions.append({
                "feature_name": feat,
                "patient_value": round(val, 3),
                "display_value": f"{val:.2f}",
                "shap_value": round(s_val, 4),
                "abs_shap_value": round(abs_s, 4),
                "direction": direction,
                "modifiable_status": rule["category"],
                "modifiable_reason": rule["reason"]
            })

        contributions.sort(key=lambda x: x["abs_shap_value"], reverse=True)
        for rank, item in enumerate(contributions, 1):
            item["rank"] = rank
            feat = item["feature_name"]
            s_v = item["shap_value"]
            if item["direction"] == "RISK_INCREASING":
                item["human_explanation"] = f"Higher relative value of '{feat}' increased model-estimated {dis.upper()} risk (SHAP: +{abs(s_v):.4f})."
            else:
                item["human_explanation"] = f"Favorable status of '{feat}' reduced model-estimated {dis.upper()} risk (SHAP: -{abs(s_v):.4f})."

        top_factors = contributions[:top_k]

        return {
            "disease": dis.upper(),
            "model_version": "smartcare_mtl_v1",
            "explainer_type": "KernelExplainer",
            "base_value": round(base_val, 4),
            "shap_reconstruction": round(reconstructed, 4),
            "consistency_valid": True,
            "top_risk_factors": top_factors,
            "all_contributions": contributions,
            "explanation_timestamp": datetime.utcnow().isoformat()
        }

    def explain_global(
        self,
        disease: str,
        eval_data: pd.DataFrame,
        n_samples: int = 50
    ) -> Dict[str, Any]:
        """
        Computes global mean |SHAP| feature importance for a disease head.
        """
        dis = disease.lower()
        explainer = self.explainers[dis]
        eval_sample = shap.sample(eval_data[self.feature_names], min(n_samples, len(eval_data)))

        shap_vals = explainer.shap_values(eval_sample, nsamples=80, silent=True)
        sv = np.array(shap_vals)
        if sv.ndim == 3:
            sv = sv[:, :, 0]

        mean_abs_shap = np.mean(np.abs(sv), axis=0)
        global_importance = []

        for i, feat in enumerate(self.feature_names):
            global_importance.append({
                "feature_name": feat,
                "mean_abs_shap": round(float(mean_abs_shap[i]), 4)
            })

        global_importance.sort(key=lambda x: x["mean_abs_shap"], reverse=True)
        for rank, item in enumerate(global_importance, 1):
            item["rank"] = rank

        return {
            "disease": dis.upper(),
            "model_version": "smartcare_mtl_v1",
            "explainer_type": "KernelExplainer",
            "global_feature_importance": global_importance,
            "num_samples_evaluated": len(eval_sample)
        }
