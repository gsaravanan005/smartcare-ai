import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List

class FeatureEngineeringService:

    FEATURE_DOCS = {
        "cardio": [
            {"name": "bmi", "sources": ["weight", "height"], "transformation": "weight / (height/100)^2", "reason": "Standard Body Mass Index clinical metric for obesity risk."},
            {"name": "pulse_pressure", "sources": ["ap_hi", "ap_lo"], "transformation": "ap_hi - ap_lo", "reason": "Surrogate marker for arterial stiffness and vascular aging."},
            {"name": "mean_arterial_pressure", "sources": ["ap_hi", "ap_lo"], "transformation": "ap_lo + (ap_hi - ap_lo) / 3", "reason": "Average arterial pressure during a cardiac cycle."},
            {"name": "age_years", "sources": ["age"], "transformation": "age / 365.25", "reason": "Standard human readable age in years."}
        ],
        "diabetes": [
            {"name": "combined_risk_index", "sources": ["HighBP", "HighChol", "Smoker", "Stroke", "HeartDiseaseorAttack"], "transformation": "Sum of binary vascular risk flags", "reason": "Aggregate multi-system cardiovascular risk score."},
            {"name": "bmi_category", "sources": ["BMI"], "transformation": "Binned BMI (underweight, normal, overweight, obese)", "reason": "Clinical obesity classification."},
            {"name": "phys_gen_hlth_ratio", "sources": ["PhysHlth", "GenHlth"], "transformation": "PhysHlth / (GenHlth + 1)", "reason": "Proportion of physical ill days relative to overall perceived health status."}
        ],
        "ckd": [
            {"name": "bun_creatinine_ratio", "sources": ["bu", "sc"], "transformation": "bu / sc", "reason": "Differentiates prerenal azotemia from intrinsic renal pathology."},
            {"name": "egfr_proxy", "sources": ["age", "sc", "gender"], "transformation": "Simplified MDRD/CKD-EPI creatinine-based filtration proxy", "reason": "Estimated glomerular filtration rate proxy for kidney clearance capacity."},
            {"name": "anemia_flag", "sources": ["hemo"], "transformation": "hemo < 12.0", "reason": "Clinical cutoff for renal erythropoietin production deficiency."},
            {"name": "electrolyte_balance", "sources": ["sod", "pot"], "transformation": "sod / pot", "reason": "Sodium-to-potassium ratio evaluating tubular electrolyte regulation."}
        ]
    }

    @classmethod
    def apply_feature_engineering(cls, name: str, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, str]]]:
        df_engineered = df.copy()
        engineered_docs = cls.FEATURE_DOCS.get(name, [])

        if name == "cardio":
            # 1. BMI calculation if missing or inaccurate
            if 'height' in df_engineered.columns and 'weight' in df_engineered.columns:
                height_m = df_engineered['height'] / 100.0
                df_engineered['bmi'] = df_engineered['weight'] / (height_m ** 2)

            # 2. Pulse Pressure
            if 'ap_hi' in df_engineered.columns and 'ap_lo' in df_engineered.columns:
                df_engineered['pulse_pressure'] = df_engineered['ap_hi'] - df_engineered['ap_lo']
                df_engineered['mean_arterial_pressure'] = df_engineered['ap_lo'] + (df_engineered['ap_hi'] - df_engineered['ap_lo']) / 3.0

            # 3. Age in years
            if 'age' in df_engineered.columns:
                df_engineered['age_years'] = (df_engineered['age'] / 365.25).round(1)

        elif name == "diabetes":
            # 1. Combined Vascular Risk Index
            risk_cols = [c for c in ['HighBP', 'HighChol', 'Smoker', 'Stroke', 'HeartDiseaseorAttack'] if c in df_engineered.columns]
            if risk_cols:
                df_engineered['combined_risk_index'] = df_engineered[risk_cols].sum(axis=1)

            # 2. BMI Category Bins (1: <18.5, 2: 18.5-24.9, 3: 25-29.9, 4: >=30)
            if 'BMI' in df_engineered.columns:
                df_engineered['bmi_category'] = pd.cut(df_engineered['BMI'], bins=[0, 18.5, 24.9, 29.9, 100], labels=[1, 2, 3, 4]).astype(float).fillna(2.0)

            # 3. PhysHlth / GenHlth Ratio
            if 'PhysHlth' in df_engineered.columns and 'GenHlth' in df_engineered.columns:
                df_engineered['phys_gen_hlth_ratio'] = df_engineered['PhysHlth'] / (df_engineered['GenHlth'] + 1.0)

        elif name == "ckd":
            # 1. BUN to Creatinine Ratio (bu / sc)
            if 'bu' in df_engineered.columns and 'sc' in df_engineered.columns:
                sc_safe = df_engineered['sc'].replace(0, np.nan).fillna(1.0)
                df_engineered['bun_creatinine_ratio'] = (df_engineered['bu'] / sc_safe).round(2)

            # 2. eGFR Proxy Score: 175 * (sc ^ -1.154) * (age ^ -0.203)
            if 'sc' in df_engineered.columns and 'age' in df_engineered.columns:
                sc_safe = df_engineered['sc'].replace(0, np.nan).fillna(1.0)
                age_safe = df_engineered['age'].replace(0, np.nan).fillna(50.0)
                df_engineered['egfr_proxy'] = (175.0 * (sc_safe ** -1.154) * (age_safe ** -0.203)).round(1)

            # 3. Anemia Indicator flag
            if 'hemo' in df_engineered.columns:
                df_engineered['anemia_flag'] = (df_engineered['hemo'] < 12.0).astype(float)

            # 4. Electrolyte ratio
            if 'sod' in df_engineered.columns and 'pot' in df_engineered.columns:
                pot_safe = df_engineered['pot'].replace(0, np.nan).fillna(4.0)
                df_engineered['electrolyte_balance'] = (df_engineered['sod'] / pot_safe).round(2)

        return df_engineered, engineered_docs
