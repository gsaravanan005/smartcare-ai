"""
SmartCare AI - Module 4 Wellness Rules Engine
Provides transparent, rule-based mapping from patient health data and SHAP explanations
to personalized, safe, conservative wellness guidance with explicit traceability attributes.
"""

from typing import Dict, Any, List, Optional

class WellnessRulesEngine:

    # Standard Disclaimer
    DISCLAIMER = (
        "SmartCare AI wellness recommendations provide general lifestyle guidance based on machine "
        "learning risk assessments and SHAP risk factor analysis. They do NOT constitute medical diagnosis, "
        "treatment plans, or medication prescriptions."
    )

    # Safe High-Risk Follow-up Alert Message
    HIGH_RISK_ALERT_MESSAGE = (
        "Professional medical evaluation is recommended. One or more evaluated disease risk scores "
        "indicated elevated risk (>60%). Please discuss your results with a qualified healthcare professional."
    )

    FACTOR_RULE_MAPPINGS = {
        "bmi": {
            "category": "Weight Management",
            "risk_factor": "Body Mass Index (BMI)",
            "unit": "kg/m²",
            "recommendation": "Adopt sustainable, nutrient-dense dietary habits and engage in regular physical activity as appropriate for your overall health.",
            "reason": "Body Mass Index (BMI) was identified as an important modifiable risk-increasing factor.",
            "related_disease": "Diabetes / CVD",
            "safety_note": "Focus on gradual, sustainable lifestyle changes rather than extreme diets."
        },
        "high_bp": {
            "category": "Cardiovascular Wellness",
            "risk_factor": "Blood Pressure Indicator",
            "unit": "",
            "recommendation": "Monitor blood pressure regularly and consider low-sodium, heart-healthy dietary choices alongside regular physical activity.",
            "reason": "Blood pressure was identified as a significant modifiable contributor to your cardiovascular risk.",
            "related_disease": "CVD / Diabetes",
            "safety_note": "Discuss abnormal blood pressure readings with a healthcare professional."
        },
        "ap_hi": {
            "category": "Cardiovascular Wellness",
            "risk_factor": "Systolic Blood Pressure",
            "unit": "mmHg",
            "recommendation": "Maintain routine blood pressure tracking and adopt dietary approaches (such as reduced sodium intake) that promote healthy arterial pressure.",
            "reason": "Systolic blood pressure was highlighted as a top risk-contributing metric by SHAP analysis.",
            "related_disease": "CVD",
            "safety_note": "Seek medical evaluation if blood pressure consistently exceeds recommended thresholds."
        },
        "ap_lo": {
            "category": "Cardiovascular Wellness",
            "risk_factor": "Diastolic Blood Pressure",
            "unit": "mmHg",
            "recommendation": "Keep track of resting diastolic pressure and support vascular health with stress management and moderate daily exercise.",
            "reason": "Diastolic blood pressure was identified as a key modifiable risk factor.",
            "related_disease": "CVD",
            "safety_note": "Seek professional medical evaluation for persistent hypertension."
        },
        "phys_activity": {
            "category": "Physical Activity",
            "risk_factor": "Low Physical Activity",
            "unit": "",
            "recommendation": "Gradually increase regular physical activity (such as 30 minutes of brisk walking most days) as appropriate for your current fitness level.",
            "reason": "Physical activity level was identified as an important modifiable factor.",
            "related_disease": "CVD / Diabetes",
            "safety_note": "Consult your doctor before starting a new exercise program."
        },
        "active": {
            "category": "Physical Activity",
            "risk_factor": "Physical Activity Level",
            "unit": "",
            "recommendation": "Aim for consistent daily movement and reduce prolonged sedentary periods where appropriate.",
            "reason": "Low physical activity contributed positively to estimated model risk.",
            "related_disease": "CVD / Diabetes",
            "safety_note": "Pace physical activities according to your comfort and health status."
        },
        "smoker": {
            "category": "Behavioral Health",
            "risk_factor": "Smoking Status",
            "unit": "",
            "recommendation": "Consider exploring structured smoking-cessation guidance and discussing evidence-based cessation programs with a clinician.",
            "reason": "Smoking status was identified as a major modifiable risk factor affecting vascular and general health.",
            "related_disease": "CVD",
            "safety_note": "Professional support significantly increases long-term smoking cessation success."
        },
        "smoke": {
            "category": "Behavioral Health",
            "risk_factor": "Tobacco Use",
            "unit": "",
            "recommendation": "Seek professional cessation support resources to help reduce cardiovascular and respiratory risks.",
            "reason": "Tobacco use was identified as a top risk-increasing behavioral factor.",
            "related_disease": "CVD",
            "safety_note": "Consult a healthcare provider for safe cessation strategy options."
        },
        "glucose": {
            "category": "Metabolic Health",
            "risk_factor": "Blood Glucose Level",
            "unit": "mg/dL",
            "recommendation": "Focus on balanced carbohydrate distribution, fiber-rich meals, and routine blood glucose monitoring to support glycemic stability.",
            "reason": "Blood glucose level was identified as an important metabolic risk factor.",
            "related_disease": "Diabetes",
            "safety_note": "Regular glucose monitoring helps evaluate dietary adjustments."
        },
        "high_chol": {
            "category": "Lipid Management",
            "risk_factor": "Blood Cholesterol Indicator",
            "unit": "",
            "recommendation": "Incorporate heart-healthy unsaturated fats, soluble fiber, and regular exercise into daily habits to support healthy lipid levels.",
            "reason": "Elevated cholesterol levels were identified as a modifiable risk factor.",
            "related_disease": "CVD / Diabetes",
            "safety_note": "Review full lipid panel results with your healthcare provider."
        },
        "cholesterol": {
            "category": "Lipid Management",
            "risk_factor": "Serum Cholesterol",
            "unit": "mg/dL",
            "recommendation": "Emphasize dietary fiber, lean protein sources, and active living to help manage cholesterol ratios.",
            "reason": "Serum cholesterol contributed to elevated risk predictions.",
            "related_disease": "CVD",
            "safety_note": "Consult a clinician for formal lipid management evaluation."
        },
        "serum_creatinine": {
            "category": "Renal Health",
            "risk_factor": "Serum Creatinine Level",
            "unit": "mg/dL",
            "recommendation": "Ensure proper hydration, avoid excessive use of unprescribed NSAID painkillers, and maintain regular kidney function lab monitoring.",
            "reason": "Serum creatinine was identified as a key renal biomarker requiring ongoing clinical monitoring.",
            "related_disease": "CKD",
            "safety_note": "General kidney wellness guidance only. Do NOT prescribe or modify renal diets or supplements without clinical oversight."
        },
        "blood_urea": {
            "category": "Renal Health",
            "risk_factor": "Blood Urea Level",
            "unit": "mg/dL",
            "recommendation": "Maintain balanced fluid intake and follow routine metabolic panel checks with your clinical team.",
            "reason": "Blood urea nitrogen was highlighted by SHAP analysis for kidney health tracking.",
            "related_disease": "CKD",
            "safety_note": "Discuss kidney lab results with a qualified healthcare professional."
        }
    }

    MONITORING_RULES = [
        {
            "condition": lambda health_input, shap_factors: (
                health_input.get("high_bp", 0) == 1 or 
                health_input.get("ap_hi", 120) > 130 or 
                any(f.get("feature_name", "").lower() in ["high_bp", "ap_hi", "ap_lo", "highbp"] for f in shap_factors)
            ),
            "item": {
                "parameter": "Blood Pressure Tracking",
                "guidance": "Check and log blood pressure 2-3 times per week at home or at a pharmacy.",
                "frequency": "Weekly",
                "related_risk_factor": "Blood Pressure"
            }
        },
        {
            "condition": lambda health_input, shap_factors: (
                health_input.get("glucose", 100) > 100 or 
                health_input.get("high_chol", 0) == 1 or 
                any(f.get("feature_name", "").lower() in ["glucose", "high_chol", "cholesterol"] for f in shap_factors)
            ),
            "item": {
                "parameter": "Fasting Blood Glucose & Lipid Panel",
                "guidance": "Schedule routine blood lab evaluations with your doctor to track blood glucose and cholesterol.",
                "frequency": "Every 3–6 Months",
                "related_risk_factor": "Blood Glucose / Cholesterol"
            }
        },
        {
            "condition": lambda health_input, shap_factors: (
                health_input.get("serum_creatinine", 1.0) > 1.2 or 
                health_input.get("blood_urea", 30) > 40 or 
                any(f.get("feature_name", "").lower() in ["serum_creatinine", "blood_urea", "sc", "bu"] for f in shap_factors)
            ),
            "item": {
                "parameter": "Kidney Function Labs (eGFR & Creatinine)",
                "guidance": "Perform routine kidney biomarker urine and blood tests under clinical supervision.",
                "frequency": "Every 6 Months",
                "related_risk_factor": "Renal Biomarkers"
            }
        }
    ]

    @classmethod
    def _format_patient_value(cls, fname: str, val: Any) -> str:
        if val is None:
            return "N/A"
        
        fname_lower = fname.lower()
        if fname_lower in ["ap_hi", "ap_lo"]:
            return f"{val} mmHg"
        if fname_lower in ["glucose", "cholesterol"]:
            return f"{val} mg/dL"
        if fname_lower in ["serum_creatinine"]:
            return f"{val} mg/dL"
        if fname_lower in ["bmi"]:
            return f"{val:.1f} kg/m²" if isinstance(val, (int, float)) else f"{val} kg/m²"
        if fname_lower in ["high_bp", "high_chol", "smoker", "smoke"]:
            return "Yes (Present)" if val == 1 or val == 1.0 else "No (Absent)"
        if fname_lower in ["phys_activity", "active"]:
            return "Active" if val == 1 or val == 1.0 else "Sedentary (No)"

        return str(val)

    @classmethod
    def evaluate_wellness_rules(
        cls,
        patient_data: Dict[str, Any],
        disease_risks: Dict[str, Dict[str, Any]],
        top_shap_factors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Processes patient data, disease predictions, and SHAP factors to generate
        personalized, transparent wellness recommendations with full traceability.
        """
        recommendations = []
        seen_categories = set()

        # Compute maximum risk severity score across evaluated diseases
        max_prob = max((info.get("probability", 0.0) for info in disease_risks.values()), default=0.0)
        risk_severity_weight = 3.0 if max_prob >= 0.60 else (2.0 if max_prob >= 0.30 else 1.0)

        def is_clinically_elevated(fn: str, p_data: Dict[str, Any]) -> bool:
            fn_low = fn.lower()
            if fn_low in ["high_bp", "highbp"]:
                return p_data.get("high_bp", 0) == 1 or float(p_data.get("ap_hi", 120)) >= 130
            if fn_low in ["smoker", "smoke"]:
                return p_data.get("smoker", 0) == 1 or p_data.get("smoke", 0) == 1
            if fn_low in ["phys_activity", "active"]:
                return p_data.get("phys_activity", 1) == 0 or p_data.get("active", 1) == 0
            if fn_low in ["high_chol", "highchol"]:
                return p_data.get("high_chol", 0) == 1
            if fn_low in ["glucose", "bgr"]:
                return float(p_data.get("glucose", p_data.get("bgr", 100))) > 110
            if fn_low in ["serum_creatinine", "sc"]:
                return float(p_data.get("serum_creatinine", p_data.get("sc", 1.0))) > 1.2
            if fn_low in ["blood_urea", "bu"]:
                return float(p_data.get("blood_urea", p_data.get("bu", 30))) > 40
            if fn_low in ["bmi"]:
                bmi_v = p_data.get("bmi")
                if bmi_v is not None and str(bmi_v) != "":
                    return float(bmi_v) >= 25.0
                if p_data.get("height_cm") and p_data.get("weight_kg"):
                    h = float(p_data["height_cm"]) / 100.0
                    return (float(p_data["weight_kg"]) / (h * h)) >= 25.0
                return False
            if fn_low in ["ap_hi", "systolic_bp"]:
                return float(p_data.get("ap_hi", 120)) >= 130
            if fn_low in ["ap_lo", "diastolic_bp"]:
                return float(p_data.get("ap_lo", 80)) >= 85
            return True

        # 1. Inspect SHAP factors first (Filter ONLY RISK_INCREASING modifiable features that are clinically elevated)
        for sf in top_shap_factors:
            fname = sf.get("feature_name", "").lower()
            m_status = sf.get("modifiable_status", "")
            direction = sf.get("direction", "")
            
            # STRICT REQUIREMENT: Only positive/RISK_INCREASING modifiable features trigger interventions
            if m_status in ["Modifiable", "Potentially Modifiable"] and direction == "RISK_INCREASING":
                if fname in cls.FACTOR_RULE_MAPPINGS and is_clinically_elevated(fname, patient_data):
                    rule = cls.FACTOR_RULE_MAPPINGS[fname]
                    
                    shap_abs = sf.get("abs_shap_value", 0.0)
                    shap_val = sf.get("shap_value", 0.0)
                    patient_val_raw = sf.get("patient_value", patient_data.get(fname))
                    formatted_val = cls._format_patient_value(fname, patient_val_raw)
                    
                    # Transparent Priority Weight Formula
                    # PriorityScore = (Risk Severity Weight) + (abs(SHAP) * 10) + Modifiability Bonus (2.0)
                    priority_score = risk_severity_weight + (shap_abs * 10.0) + 2.0
                    
                    if priority_score >= 5.0 or shap_abs >= 0.15:
                        priority = "High"
                    elif priority_score >= 3.5 or shap_abs >= 0.05:
                        priority = "Medium"
                    else:
                        priority = "Low"

                    custom_reason = (
                        f"Your recorded value for {rule['risk_factor']} ({formatted_val}) was identified "
                        f"by SHAP analysis as a top risk-increasing contributor (SHAP: +{shap_abs:.4f})."
                    )

                    rec_item = {
                        "category": rule["category"],
                        "risk_factor": rule["risk_factor"],
                        "source_feature": fname,
                        "patient_value": formatted_val,
                        "shap_value": round(shap_val, 4),
                        "effect_direction": direction,
                        "recommendation": rule["recommendation"],
                        "reason": custom_reason,
                        "priority": priority,
                        "related_disease": rule["related_disease"],
                        "safety_note": rule["safety_note"]
                    }
                    
                    if rule["category"] not in seen_categories:
                        recommendations.append(rec_item)
                        seen_categories.add(rule["category"])

        # 2. Inspect raw patient health input flags if SHAP list was empty or produced few items
        if len(recommendations) < 2:
            # Check high BMI
            weight = patient_data.get("weight_kg")
            height = patient_data.get("height_cm")
            bmi_val = patient_data.get("bmi")
            if not bmi_val and weight and height:
                bmi_val = weight / ((height / 100) ** 2)

            if (bmi_val and bmi_val >= 25.0) and "Weight Management" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["bmi"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "bmi",
                    "patient_value": f"{bmi_val:.1f} kg/m²",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": f"Your recorded BMI of {bmi_val:.1f} kg/m² indicates opportunity for healthy body mass management.",
                    "priority": "High" if (bmi_val and bmi_val >= 30.0) else "Medium",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Weight Management")

            # Check High BP
            high_bp = patient_data.get("high_bp", 0)
            ap_hi = patient_data.get("ap_hi", 120)
            if (high_bp == 1 or ap_hi > 130) and "Cardiovascular Wellness" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["high_bp"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "ap_hi",
                    "patient_value": f"{ap_hi} mmHg",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": f"Your recorded blood pressure metric (Systolic: {ap_hi} mmHg) suggests cardiovascular wellness focus.",
                    "priority": "High" if ap_hi > 140 else "Medium",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Cardiovascular Wellness")

            # Check Low Physical Activity
            phys = patient_data.get("phys_activity", 1)
            if phys == 0 and "Physical Activity" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["phys_activity"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "phys_activity",
                    "patient_value": "Sedentary (No)",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": "A sedentary physical activity level was recorded in your health data.",
                    "priority": "Medium",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Physical Activity")

            # Check Smoking
            smoker = patient_data.get("smoker", 0)
            if smoker == 1 and "Behavioral Health" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["smoker"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "smoker",
                    "patient_value": "Active Smoker (Yes)",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": "Active smoking status was identified in your behavioral health profile.",
                    "priority": "High",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Behavioral Health")

            # Check High Glucose
            glucose = patient_data.get("glucose", 100)
            if glucose > 100 and "Metabolic Health" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["glucose"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "glucose",
                    "patient_value": f"{glucose} mg/dL",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": f"Elevated blood glucose metric of {glucose} mg/dL was identified.",
                    "priority": "High" if glucose > 126 else "Medium",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Metabolic Health")

            # Check High Cholesterol
            high_chol = patient_data.get("high_chol", 0)
            if high_chol == 1 and "Lipid Management" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["high_chol"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "high_chol",
                    "patient_value": "Present (Yes)",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": "An elevated cholesterol indicator was recorded in your health record.",
                    "priority": "Medium",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Lipid Management")

            # Check Serum Creatinine / CKD
            sc = patient_data.get("serum_creatinine", 1.0)
            if sc > 1.2 and "Renal Health" not in seen_categories:
                rule = cls.FACTOR_RULE_MAPPINGS["serum_creatinine"]
                recommendations.append({
                    "category": rule["category"],
                    "risk_factor": rule["risk_factor"],
                    "source_feature": "serum_creatinine",
                    "patient_value": f"{sc} mg/dL",
                    "shap_value": 0.0,
                    "effect_direction": "RISK_INCREASING",
                    "recommendation": rule["recommendation"],
                    "reason": f"Serum creatinine level of {sc} mg/dL indicates renal function tracking priority.",
                    "priority": "High" if sc > 1.5 else "Medium",
                    "related_disease": rule["related_disease"],
                    "safety_note": rule["safety_note"]
                })
                seen_categories.add("Renal Health")

        # 3. PATIENT G REQUIREMENT: If no specific modifiable factors were identified
        if len(recommendations) == 0:
            recommendations.append({
                "category": "Assessment Status",
                "risk_factor": "No Modifiable Risk Factors Identified",
                "source_feature": "baseline",
                "patient_value": "Normal Range",
                "shap_value": 0.0,
                "effect_direction": "NEUTRAL",
                "recommendation": "Maintain your existing healthy lifestyle, balanced nutrition, regular hydration, and routine preventive health checkups.",
                "reason": "No specific modifiable risk factors were identified from your current assessment.",
                "priority": "Low",
                "related_disease": "Multi-Disease",
                "safety_note": "Routine annual health examinations remain recommended."
            })

        # Sort recommendations by Priority: High > Medium > Low
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        recommendations.sort(key=lambda x: priority_map.get(x["priority"], 99))

        # 4. Filter Monitoring Rules based on active factors
        monitoring = []
        for m_rule in cls.MONITORING_RULES:
            if m_rule["condition"](patient_data, top_shap_factors):
                monitoring.append(m_rule["item"])

        # 5. Check High Risk Clinical Safety Trigger (risk > 60%)
        clinical_followup_required = False
        elevated_diseases = []
        for dis, info in disease_risks.items():
            prob = info.get("probability", 0.0)
            cat = info.get("risk_category", "")
            if prob >= 0.60 or cat == "HIGH":
                clinical_followup_required = True
                elevated_diseases.append(dis.upper())

        follow_up_msg = None
        if clinical_followup_required:
            dis_str = ", ".join(elevated_diseases) if elevated_diseases else "disease"
            follow_up_msg = (
                f"Professional medical evaluation is recommended. Evaluated risk score for {dis_str} indicated elevated risk (>60%). "
                "Please discuss your assessment results with a qualified healthcare professional."
            )

        return {
            "recommendations": recommendations,
            "monitoring": monitoring,
            "clinical_followup_required": clinical_followup_required,
            "follow_up_message": follow_up_msg,
            "disclaimer": cls.DISCLAIMER
        }
