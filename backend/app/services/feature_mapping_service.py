import numpy as np
from typing import Dict, Any, List

class FeatureMappingService:
    """
    Standardized Feature Mapping Layer for SmartCare AI.
    Aligns common features across Diabetes, CVD, and CKD datasets for Module 2.
    """

    FEATURE_MAPPING = [
        # --- Demographics ---
        {"original": "Age", "standardized": "age_years", "type": "numerical", "disease": "diabetes", "transformation": "Ordinal binned / Direct years", "usage": "Common Predictor"},
        {"original": "age", "standardized": "age_years", "type": "numerical", "disease": "cvd", "transformation": "age / 365.25", "usage": "Common Predictor"},
        {"original": "age", "standardized": "age_years", "type": "numerical", "disease": "ckd", "transformation": "Direct years", "usage": "Common Predictor"},
        
        {"original": "Sex", "standardized": "gender", "type": "binary", "disease": "diabetes", "transformation": "1: Male, 0: Female", "usage": "Common Predictor"},
        {"original": "gender", "standardized": "gender", "type": "binary", "disease": "cvd", "transformation": "2: Male, 1: Female -> 1: Male, 0: Female", "usage": "Common Predictor"},
        
        {"original": "BMI", "standardized": "bmi", "type": "numerical", "disease": "diabetes", "transformation": "Direct BMI", "usage": "Common Predictor"},
        {"original": "bmi", "standardized": "bmi", "type": "numerical", "disease": "cvd", "transformation": "weight / (height/100)^2", "usage": "Common Predictor"},

        # --- Cardiovascular Indicators ---
        {"original": "HighBP", "standardized": "high_bp", "type": "binary", "disease": "diabetes", "transformation": "1.0 / 0.0 flag", "usage": "Vascular Risk Indicator"},
        {"original": "ap_hi", "standardized": "systolic_bp", "type": "numerical", "disease": "cvd", "transformation": "mmHg value", "usage": "CVD Specific Predictor"},
        {"original": "ap_lo", "standardized": "diastolic_bp", "type": "numerical", "disease": "cvd", "transformation": "mmHg value", "usage": "CVD Specific Predictor"},
        {"original": "bp", "standardized": "blood_pressure", "type": "numerical", "disease": "ckd", "transformation": "mmHg value", "usage": "CKD Specific Predictor"},
        {"original": "htn", "standardized": "high_bp", "type": "binary", "disease": "ckd", "transformation": "yes/no -> 1/0", "usage": "Vascular Risk Indicator"},

        # --- Metabolic & Cholesterol ---
        {"original": "HighChol", "standardized": "high_cholesterol", "type": "binary", "disease": "diabetes", "transformation": "1.0 / 0.0 flag", "usage": "Metabolic Predictor"},
        {"original": "cholesterol", "standardized": "cholesterol_level", "type": "categorical", "disease": "cvd", "transformation": "1: Normal, 2: Above Normal, 3: High", "usage": "CVD Specific Predictor"},
        {"original": "gluc", "standardized": "glucose_level", "type": "categorical", "disease": "cvd", "transformation": "1: Normal, 2: Above Normal, 3: High", "usage": "Metabolic Predictor"},
        {"original": "dm", "standardized": "diabetes_history", "type": "binary", "disease": "ckd", "transformation": "yes/no -> 1/0", "usage": "Comorbidity Flag"},
        {"original": "bgr", "standardized": "blood_glucose_random", "type": "numerical", "disease": "ckd", "transformation": "mg/dL value", "usage": "CKD Specific Predictor"},

        # --- Lifestyle & Behavioral ---
        {"original": "Smoker", "standardized": "smoking_status", "type": "binary", "disease": "diabetes", "transformation": "1.0 / 0.0 flag", "usage": "Behavioral Predictor"},
        {"original": "smoke", "standardized": "smoking_status", "type": "binary", "disease": "cvd", "transformation": "1 / 0 flag", "usage": "Behavioral Predictor"},
        {"original": "PhysActivity", "standardized": "physical_activity", "type": "binary", "disease": "diabetes", "transformation": "1.0 / 0.0 flag", "usage": "Behavioral Predictor"},
        {"original": "active", "standardized": "physical_activity", "type": "binary", "disease": "cvd", "transformation": "1 / 0 flag", "usage": "Behavioral Predictor"},
        {"original": "HvyAlcoholConsump", "standardized": "alcohol_consumption", "type": "binary", "disease": "diabetes", "transformation": "1.0 / 0.0 flag", "usage": "Behavioral Predictor"},
        {"original": "alco", "standardized": "alcohol_consumption", "type": "binary", "disease": "cvd", "transformation": "1 / 0 flag", "usage": "Behavioral Predictor"},

        # --- CKD Specific Renal Biomarkers ---
        {"original": "sc", "standardized": "serum_creatinine", "type": "numerical", "disease": "ckd", "transformation": "mg/dL value", "usage": "CKD Biomarker"},
        {"original": "bu", "standardized": "blood_urea", "type": "numerical", "disease": "ckd", "transformation": "mg/dL value", "usage": "CKD Biomarker"},
        {"original": "hemo", "standardized": "hemoglobin", "type": "numerical", "disease": "ckd", "transformation": "g/dL value", "usage": "CKD Biomarker"},
        {"original": "al", "standardized": "albumin_level", "type": "categorical", "disease": "ckd", "transformation": "0 to 5 scale", "usage": "CKD Biomarker"},
        {"original": "sg", "standardized": "specific_gravity", "type": "numerical", "disease": "ckd", "transformation": "1.005 - 1.025", "usage": "CKD Biomarker"}
    ]

    @classmethod
    def _val(cls, d: Dict[str, Any], key: str, default: Any) -> Any:
        v = d.get(key)
        return default if v is None else v

    @classmethod
    def get_common_feature_schema(cls) -> List[Dict[str, Any]]:
        return cls.FEATURE_MAPPING

    @classmethod
    def _age_to_brfss_bin(cls, age: float) -> float:
        if age < 25: return 1.0
        elif age < 30: return 2.0
        elif age < 35: return 3.0
        elif age < 40: return 4.0
        elif age < 45: return 5.0
        elif age < 50: return 6.0
        elif age < 55: return 7.0
        elif age < 60: return 8.0
        elif age < 65: return 9.0
        elif age < 70: return 10.0
        elif age < 75: return 11.0
        elif age < 80: return 12.0
        else: return 13.0

    @classmethod
    def map_patient_input_to_features(cls, patient_input: Dict[str, Any], dataset_name: str) -> Dict[str, Any]:
        """
        Maps single patient health form submission to the expected feature schema for a specific disease dataset.
        Handles None values safely.
        """
        mapped = {}
        v = cls._val

        if dataset_name == "diabetes":
            mapped["HighBP"] = float(v(patient_input, "high_bp", 0))
            mapped["HighChol"] = float(v(patient_input, "high_chol", 0))
            mapped["CholCheck"] = float(v(patient_input, "chol_check", 1))

            # Dynamic BMI calculation if height_cm and weight_kg are present
            raw_bmi = patient_input.get("bmi")
            if raw_bmi is not None and str(raw_bmi) != "" and not np.isnan(float(raw_bmi)):
                mapped["BMI"] = float(raw_bmi)
            elif patient_input.get("height_cm") and patient_input.get("weight_kg"):
                h_m = float(patient_input["height_cm"]) / 100.0
                mapped["BMI"] = round(float(patient_input["weight_kg"]) / (h_m ** 2), 1)
            else:
                mapped["BMI"] = 25.0

            mapped["Smoker"] = float(v(patient_input, "smoker", 0))
            mapped["Stroke"] = float(v(patient_input, "stroke", 0))
            mapped["HeartDiseaseorAttack"] = float(v(patient_input, "heart_disease_or_attack", 0))
            mapped["PhysActivity"] = float(v(patient_input, "phys_activity", 1))
            mapped["Fruits"] = float(v(patient_input, "fruits", 1))
            mapped["Veggies"] = float(v(patient_input, "veggies", 1))
            mapped["HvyAlcoholConsump"] = float(v(patient_input, "hvy_alcohol_consump", 0))
            mapped["AnyHealthcare"] = float(v(patient_input, "any_healthcare", 1))
            mapped["NoDocbcCost"] = float(v(patient_input, "no_doc_bc_cost", 0))
            mapped["GenHlth"] = float(v(patient_input, "gen_hlth", 2))
            mapped["MentHlth"] = float(v(patient_input, "ment_hlth", 0))
            mapped["PhysHlth"] = float(v(patient_input, "phys_hlth", 0))
            mapped["DiffWalk"] = float(v(patient_input, "diff_walk", 0))
            mapped["Sex"] = float(v(patient_input, "sex", 1))

            # Dynamic Age Bin calculation
            raw_age_bin = patient_input.get("age_bin")
            if raw_age_bin is not None and str(raw_age_bin) != "":
                mapped["Age"] = float(raw_age_bin)
            elif patient_input.get("age") is not None and str(patient_input.get("age")) != "":
                mapped["Age"] = cls._age_to_brfss_bin(float(patient_input["age"]))
            else:
                mapped["Age"] = 8.0

            mapped["Education"] = float(v(patient_input, "education", 5.0))
            mapped["Income"] = float(v(patient_input, "income", 6.0))

        elif dataset_name == "cardio":
            mapped["age"] = int(v(patient_input, "age", 50) * 365.25)
            mapped["gender"] = 2 if v(patient_input, "sex", 1) == 1 else 1
            mapped["height"] = int(v(patient_input, "height_cm", 170))
            mapped["weight"] = float(v(patient_input, "weight_kg", 70.0))
            mapped["ap_hi"] = int(v(patient_input, "ap_hi", 120))
            mapped["ap_lo"] = int(v(patient_input, "ap_lo", 80))

            # Map high_chol to cholesterol levels (1: Normal, 2: Above Normal, 3: High)
            if patient_input.get("cholesterol") is not None and str(patient_input.get("cholesterol")) != "":
                mapped["cholesterol"] = int(patient_input["cholesterol"])
            else:
                mapped["cholesterol"] = 2 if v(patient_input, "high_chol", 0) == 1 else 1

            # Map glucose to glucose categories (1: Normal <120, 2: Above Normal 120-180, 3: High >180)
            if patient_input.get("glucose_cat") is not None and str(patient_input.get("glucose_cat")) != "":
                mapped["gluc"] = int(patient_input["glucose_cat"])
            else:
                gl = float(v(patient_input, "glucose", 100))
                mapped["gluc"] = 3 if gl > 180 else (2 if gl >= 120 else 1)

            mapped["smoke"] = int(v(patient_input, "smoker", 0))
            mapped["alco"] = int(v(patient_input, "hvy_alcohol_consump", 0))
            mapped["active"] = int(v(patient_input, "phys_activity", 1))

        elif dataset_name == "ckd":
            mapped["age"] = float(v(patient_input, "age", 50.0))
            mapped["bp"] = float(v(patient_input, "ap_hi", 80.0))
            mapped["sg"] = float(v(patient_input, "specific_gravity", 1.020))
            mapped["al"] = float(v(patient_input, "albumin_level", 0.0))
            mapped["su"] = float(v(patient_input, "sugar_level", 0.0))
            mapped["rbc"] = v(patient_input, "rbc", "normal")
            mapped["pc"] = v(patient_input, "pc", "normal")
            mapped["pcc"] = v(patient_input, "pcc", "notpresent")
            mapped["ba"] = v(patient_input, "ba", "notpresent")
            mapped["bgr"] = float(v(patient_input, "glucose", 120.0))
            mapped["bu"] = float(v(patient_input, "blood_urea", 30.0))
            mapped["sc"] = float(v(patient_input, "serum_creatinine", 1.0))
            mapped["sod"] = float(v(patient_input, "sodium", 138.0))
            mapped["pot"] = float(v(patient_input, "potassium", 4.2))
            mapped["hemo"] = float(v(patient_input, "hemoglobin", 14.0))
            mapped["pcv"] = float(v(patient_input, "packed_cell_volume", 40.0))
            mapped["wc"] = float(v(patient_input, "white_blood_cell_count", 7500.0))
            mapped["rc"] = float(v(patient_input, "red_blood_cell_count", 4.8))

            high_bp_flag = v(patient_input, "high_bp", 0) == 1 or float(v(patient_input, "ap_hi", 120)) >= 140
            mapped["htn"] = "yes" if high_bp_flag else "no"

            dm_flag = v(patient_input, "diabetes_flag", 0) == 1 or float(v(patient_input, "glucose", 100)) >= 126
            mapped["dm"] = "yes" if dm_flag else "no"

            mapped["cad"] = "yes" if v(patient_input, "heart_disease_or_attack", 0) == 1 else "no"
            mapped["appet"] = v(patient_input, "appetite", "good")
            mapped["pe"] = v(patient_input, "pedal_edema", "no")

            ane_flag = v(patient_input, "anemia", "no") == "yes" or float(v(patient_input, "hemoglobin", 14.0)) < 11.0
            mapped["ane"] = "yes" if ane_flag else "no"

        return mapped
