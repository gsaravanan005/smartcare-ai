"""
SmartCare AI - Module 4 Recommendation Service
Orchestrates prediction/SHAP inputs from Modules 1-3, applies transparent wellness,
food, exercise, habit, and herbal rules, persists recommendation records in the database,
and localizes payloads into 6 supported languages.
"""

import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from ..models.models import Patient, HealthRecord, PredictionRecord, ExplanationRecord, FeatureContribution, RecommendationRecord
from ..rules.wellness_rules import WellnessRulesEngine
from ..services.prediction_service import PredictionService
from ..services.daily_plan_service import DailyPlanService
from ..localization.recommendation_translator import RecommendationTranslator

logger = logging.getLogger(__name__)

class RecommendationService:

    @classmethod
    def generate_recommendation_plan(
        cls,
        db: Session,
        patient_id: Optional[int] = None,
        prediction_id: Optional[str] = None,
        health_input: Optional[Dict[str, Any]] = None,
        language: Optional[str] = "en"
    ) -> Dict[str, Any]:
        """
        Generates or retrieves personalized wellness recommendations, daily food plans,
        exercise plans, daily habits, and herbal guidance using actual prediction scores
        and SHAP risk factors.
        """
        if not language or language.lower() not in RecommendationTranslator.SUPPORTED_LANGUAGES:
            language = "en"
        else:
            language = language.lower()

        pred_rec = None
        patient_health_data = {}
        disease_risks = {}
        top_shap_factors = []

        # 1. Locate Prediction Record and Patient Data
        if prediction_id:
            pred_rec = db.query(PredictionRecord).filter(PredictionRecord.prediction_id == prediction_id).first()

        if not pred_rec and patient_id:
            pred_rec = db.query(PredictionRecord).filter(
                PredictionRecord.patient_id == patient_id
            ).order_by(PredictionRecord.created_at.desc()).first()

        # Extract patient health data from latest HealthRecord
        if patient_id:
            latest_hr = db.query(HealthRecord).filter(
                HealthRecord.patient_id == patient_id
            ).order_by(HealthRecord.created_at.desc()).first()
            
            if latest_hr:
                patient_health_data = {
                    "high_bp": latest_hr.high_bp or 0.0,
                    "high_chol": latest_hr.high_chol or 0.0,
                    "smoker": latest_hr.smoker or 0.0,
                    "phys_activity": latest_hr.phys_activity or 1.0,
                    "ap_hi": latest_hr.ap_hi or 120.0,
                    "ap_lo": latest_hr.ap_lo or 80.0,
                    "glucose": latest_hr.glucose or 100.0,
                    "cholesterol": latest_hr.cholesterol or 1.0,
                    "serum_creatinine": latest_hr.serum_creatinine or 1.0,
                    "blood_urea": latest_hr.blood_urea or 30.0,
                    "hemoglobin": latest_hr.hemoglobin or 14.0
                }
                
                patient_obj = db.query(Patient).filter(Patient.id == patient_id).first()
                if patient_obj:
                    patient_health_data["age"] = patient_obj.age or 45.0
                    patient_health_data["sex"] = patient_obj.sex or 1
                    patient_health_data["height_cm"] = patient_obj.height_cm or 170.0
                    patient_health_data["weight_kg"] = patient_obj.weight_kg or 70.0
                    patient_health_data["bmi"] = patient_obj.bmi

        if health_input:
            patient_health_data.update({k: v for k, v in health_input.items() if v is not None})

        # 2. On-the-fly prediction if record missing
        if not pred_rec:
            if not patient_health_data:
                patient_health_data = {
                    "age": 50, "sex": 1, "height_cm": 170, "weight_kg": 75,
                    "high_bp": 0, "high_chol": 0, "smoker": 0, "phys_activity": 1,
                    "ap_hi": 120, "ap_lo": 80, "glucose": 100, "serum_creatinine": 1.0, "blood_urea": 30
                }

            pred_res = PredictionService.predict_multi_disease_risk(patient_health_data, patient_id=patient_id)
            disease_risks = pred_res["predictions"]
            
            for dis, factor_list in pred_res.get("shap", {}).items():
                top_shap_factors.extend(factor_list)

            target_pred_id = pred_res.get("prediction_id", f"PRED_GEN_{uuid.uuid4().hex[:8].upper()}")
        else:
            target_pred_id = pred_rec.prediction_id
            if not patient_id and pred_rec.patient_id:
                patient_id = pred_rec.patient_id

            disease_risks = {
                "diabetes": {
                    "disease": "DIABETES",
                    "probability": pred_rec.diabetes_probability,
                    "risk_percentage": round(pred_rec.diabetes_probability * 100, 1),
                    "risk_category": pred_rec.diabetes_risk_category
                },
                "cardio": {
                    "disease": "CARDIO",
                    "probability": pred_rec.cvd_probability,
                    "risk_percentage": round(pred_rec.cvd_probability * 100, 1),
                    "risk_category": pred_rec.cvd_risk_category
                },
                "ckd": {
                    "disease": "CKD",
                    "probability": pred_rec.ckd_probability,
                    "risk_percentage": round(pred_rec.ckd_probability * 100, 1),
                    "risk_category": pred_rec.ckd_risk_category
                }
            }

            exp_records = db.query(ExplanationRecord).filter(
                ExplanationRecord.prediction_id == pred_rec.prediction_id
            ).all()

            for exp in exp_records:
                fc_list = db.query(FeatureContribution).filter(
                    FeatureContribution.explanation_id == exp.explanation_id
                ).order_by(FeatureContribution.rank).all()

                for fc in fc_list:
                    top_shap_factors.append({
                        "feature_name": fc.feature_name,
                        "patient_value": fc.patient_value,
                        "shap_value": fc.shap_value,
                        "abs_shap_value": fc.abs_shap_value,
                        "direction": fc.direction,
                        "rank": fc.rank,
                        "modifiable_status": fc.modifiable_status,
                        "human_explanation": fc.human_explanation
                    })

        top_shap_factors.sort(key=lambda x: x.get("abs_shap_value", 0.0), reverse=True)

        # 3. Apply Base Wellness Rules Engine
        rule_eval_res = WellnessRulesEngine.evaluate_wellness_rules(
            patient_data=patient_health_data,
            disease_risks=disease_risks,
            top_shap_factors=top_shap_factors
        )

        # 4. Generate Enhanced Daily Plans (Food, Exercise, Habits, Herbal)
        daily_plans = DailyPlanService.generate_all_daily_plans(
            patient_data=patient_health_data,
            disease_risks=disease_risks,
            top_shap_factors=top_shap_factors
        )

        recommendation_items = rule_eval_res["recommendations"]
        monitoring_items = rule_eval_res["monitoring"]
        clinical_followup_required = rule_eval_res["clinical_followup_required"]
        follow_up_message = rule_eval_res["follow_up_message"]

        # 5. Persist Record to Database
        if patient_id or target_pred_id:
            if patient_id:
                db.query(RecommendationRecord).filter(
                    RecommendationRecord.patient_id == patient_id,
                    RecommendationRecord.status == "ACTIVE"
                ).update({"status": "ARCHIVED"})
            elif target_pred_id:
                db.query(RecommendationRecord).filter(
                    RecommendationRecord.prediction_id == target_pred_id,
                    RecommendationRecord.status == "ACTIVE"
                ).update({"status": "ARCHIVED"})

            db.commit()

            assessment_id = f"ASSESS_{uuid.uuid4().hex[:8].upper()}"

            db_records = []
            for item in recommendation_items:
                rec_db = RecommendationRecord(
                    patient_id=patient_id,
                    prediction_id=target_pred_id,
                    assessment_id=assessment_id,
                    language=language,
                    disease=item.get("related_disease", "MULTI-DISEASE"),
                    risk_factor=item.get("risk_factor", "General"),
                    category=item.get("category", "Lifestyle"),
                    recommendation_text=item.get("recommendation", ""),
                    reason=item.get("reason", ""),
                    priority=item.get("priority", "Medium"),
                    safety_note=item.get("safety_note", ""),
                    daily_food_plan=daily_plans["daily_food_plan"],
                    exercise_plan=daily_plans["exercise_plan"],
                    daily_habits=daily_plans["daily_habits"],
                    herbal_wellness=daily_plans["herbal_wellness"],
                    monitoring_guidance=monitoring_items,
                    clinical_followup_required=clinical_followup_required,
                    clinical_followup_message=follow_up_message,
                    status="ACTIVE"
                )
                db.add(rec_db)
                db_records.append(rec_db)

            db.commit()

            for idx, rec_db in enumerate(db_records):
                recommendation_items[idx]["id"] = rec_db.id

        # 6. Extract Unique Modifiable Key Factors
        key_modifiable_factors = []
        seen_factors = set()
        modifiable_names = {"ap_hi", "ap_lo", "glucose", "high_bp", "high_chol", "smoker", "phys_activity", "bmi", "serum_creatinine", "blood_urea", "cholesterol"}
        
        for sf in top_shap_factors:
            fn = sf.get("feature_name", "")
            fn_lower = fn.lower()
            m_status = sf.get("modifiable_status")
            is_mod = (m_status in ["Modifiable", "Potentially Modifiable"]) or (fn_lower in modifiable_names)
            
            if is_mod and fn_lower not in seen_factors:
                key_modifiable_factors.append({
                    "feature_name": fn,
                    "direction": sf.get("direction", "RISK_INCREASING"),
                    "rank": sf.get("rank", len(key_modifiable_factors) + 1),
                    "abs_shap_value": sf.get("abs_shap_value", abs(sf.get("shap_value", 0.0))),
                    "modifiable_status": m_status or "Modifiable"
                })
                seen_factors.add(fn_lower)
                if len(key_modifiable_factors) >= 5:
                    break

        response_payload = {
            "patient_id": patient_id,
            "prediction_id": target_pred_id,
            "assessment_id": target_pred_id,
            "language": language,
            "risk_summary": disease_risks,
            "modifiable_factors": key_modifiable_factors,
            "recommendations": recommendation_items,
            "daily_food_plan": daily_plans["daily_food_plan"],
            "exercise_plan": daily_plans["exercise_plan"],
            "daily_habits": daily_plans["daily_habits"],
            "herbal_wellness": daily_plans["herbal_wellness"],
            "monitoring_guidance": monitoring_items,
            "clinical_followup_required": clinical_followup_required,
            "clinical_followup_message": follow_up_message,
            "disclaimer": rule_eval_res["disclaimer"],
            "timestamp": datetime.utcnow().isoformat()
        }

        # MongoDB Persistence
        try:
            from ..core.mongo_db import mongo_manager
            wellness_col = mongo_manager.get_collection("wellness_plans")
            now_iso = datetime.utcnow().isoformat()
            plan_doc = {
                "plan_id": f"PLAN_{uuid.uuid4().hex[:8].upper()}",
                "patient_id": patient_id,
                "prediction_id": target_pred_id,
                "risk_level": disease_risks,
                "recommendations": recommendation_items,
                "diet_guidance": daily_plans["daily_food_plan"],
                "exercise_guidance": daily_plans["exercise_plan"],
                "lifestyle_guidance": daily_plans["daily_habits"],
                "herbal_guidance": daily_plans["herbal_wellness"],
                "generated_by": "SmartCare AI Rule Engine & Clinical Expert Rules",
                "created_at": now_iso,
                "updated_at": now_iso
            }
            wellness_col.insert_one(plan_doc)
        except Exception as err:
            print(f"[MongoDB Wellness Persistence Note] {err}")

        # 7. Apply Multilingual Translator
        translated_payload = RecommendationTranslator.translate_plan(response_payload, language)
        return translated_payload

    @classmethod
    def get_recommendations_by_patient(cls, db: Session, patient_id: int) -> List[RecommendationRecord]:
        return db.query(RecommendationRecord).filter(
            RecommendationRecord.patient_id == patient_id,
            RecommendationRecord.status == "ACTIVE"
        ).order_by(RecommendationRecord.created_at.desc()).all()

    @classmethod
    def get_recommendations_by_prediction(cls, db: Session, prediction_id: str) -> List[RecommendationRecord]:
        return db.query(RecommendationRecord).filter(
            RecommendationRecord.prediction_id == prediction_id
        ).order_by(RecommendationRecord.created_at.desc()).all()
