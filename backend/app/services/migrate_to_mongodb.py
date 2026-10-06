"""
SmartCare AI - SQLite to MongoDB Migration Utility
Reads existing SQLite database tables and migrates records seamlessly into MongoDB collections.
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..core.mongo_db import mongo_manager
from ..models.models import (
    User, Patient, HealthRecord, PredictionRecord, 
    ExplanationRecord, FeatureContribution, RecommendationRecord, 
    ClinicalAlert, ClinicianFeedback, ChatHistory
)

def run_migration():
    print("[Migration] Starting SQLite to MongoDB migration...")
    db: Session = SessionLocal()

    try:
        # 1. Migrate Users
        users_col = mongo_manager.get_collection("users")
        sql_users = db.query(User).all()
        user_count = 0
        for u in sql_users:
            if not users_col.find_one({"email": u.email}):
                now_iso = u.created_at.isoformat() if u.created_at else datetime.now(timezone.utc).isoformat()
                users_col.insert_one({
                    "user_id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "password_hash": u.hashed_password,
                    "hashed_password": u.hashed_password,
                    "full_name": u.full_name or u.username,
                    "role": u.role or "patient",
                    "status": getattr(u, "status", "active") or "active",
                    "phone": "",
                    "created_at": now_iso,
                    "updated_at": now_iso,
                    "last_login": now_iso
                })
                user_count += 1
        print(f"[Migration] Migrated {user_count} users to MongoDB 'users' collection.")

        # 2. Migrate Patients
        patients_col = mongo_manager.get_collection("patients")
        sql_patients = db.query(Patient).all()
        patient_count = 0
        for p in sql_patients:
            if not patients_col.find_one({"patient_id": p.id}):
                now_iso = p.created_at.isoformat() if p.created_at else datetime.now(timezone.utc).isoformat()
                patients_col.insert_one({
                    "patient_id": p.id,
                    "user_id": p.user_id,
                    "date_of_birth": None,
                    "gender": "Male" if p.sex == 1 else "Female" if p.sex == 0 else None,
                    "height": p.height_cm,
                    "height_cm": p.height_cm,
                    "weight": p.weight_kg,
                    "weight_kg": p.weight_kg,
                    "bmi": p.bmi,
                    "blood_pressure": None,
                    "blood_glucose": None,
                    "cholesterol": None,
                    "smoking_status": 0,
                    "physical_activity": 1,
                    "family_history": [],
                    "existing_conditions": [],
                    "medications": [],
                    "education_level": p.education_level,
                    "income_level": p.income_level,
                    "created_at": now_iso,
                    "updated_at": p.updated_at.isoformat() if p.updated_at else now_iso
                })
                patient_count += 1
        print(f"[Migration] Migrated {patient_count} patients to MongoDB 'patients' collection.")

        # 3. Migrate Health Records
        hr_col = mongo_manager.get_collection("health_records")
        sql_hrs = db.query(HealthRecord).all()
        hr_count = 0
        for hr in sql_hrs:
            if not hr_col.find_one({"record_id": hr.id}):
                now_iso = hr.created_at.isoformat() if hr.created_at else datetime.now(timezone.utc).isoformat()
                hr_col.insert_one({
                    "record_id": hr.id,
                    "patient_id": hr.patient_id,
                    "record_type": "vitals_input",
                    "health_data": {
                        "high_bp": hr.high_bp,
                        "high_chol": hr.high_chol,
                        "smoker": hr.smoker,
                        "phys_activity": hr.phys_activity,
                        "ap_hi": hr.ap_hi,
                        "ap_lo": hr.ap_lo,
                        "glucose": hr.glucose,
                        "serum_creatinine": hr.serum_creatinine,
                        "blood_urea": hr.blood_urea,
                        "hemoglobin": hr.hemoglobin
                    },
                    "record_date": now_iso,
                    "created_at": now_iso,
                    "updated_at": now_iso
                })
                hr_count += 1
        print(f"[Migration] Migrated {hr_count} health records to MongoDB 'health_records' collection.")

        # 4. Migrate Prediction Records
        preds_col = mongo_manager.get_collection("predictions")
        sql_preds = db.query(PredictionRecord).all()
        pred_count = 0
        for pr in sql_preds:
            if not preds_col.find_one({"prediction_id": pr.prediction_id}):
                now_iso = pr.created_at.isoformat() if pr.created_at else datetime.now(timezone.utc).isoformat()
                preds_col.insert_one({
                    "prediction_id": pr.prediction_id,
                    "patient_id": pr.patient_id,
                    "model_name": "SmartCare AI Multi-Disease Ensemble",
                    "model_version": pr.model_version,
                    "input_features": pr.module3_handoff_payload.get("input_features", {}) if pr.module3_handoff_payload else {},
                    "prediction": {
                        "diabetes": {"probability": pr.diabetes_probability, "risk_category": pr.diabetes_risk_category},
                        "cvd": {"probability": pr.cvd_probability, "risk_category": pr.cvd_risk_category},
                        "ckd": {"probability": pr.ckd_probability, "risk_category": pr.ckd_risk_category}
                    },
                    "risk_score": {
                        "diabetes": pr.diabetes_probability,
                        "cvd": pr.cvd_probability,
                        "ckd": pr.ckd_probability
                    },
                    "risk_level": {
                        "diabetes": pr.diabetes_risk_category,
                        "cvd": pr.cvd_risk_category,
                        "ckd": pr.ckd_risk_category
                    },
                    "diabetes_probability": pr.diabetes_probability,
                    "diabetes_risk_category": pr.diabetes_risk_category,
                    "cvd_probability": pr.cvd_probability,
                    "cvd_risk_category": pr.cvd_risk_category,
                    "ckd_probability": pr.ckd_probability,
                    "ckd_risk_category": pr.ckd_risk_category,
                    "prediction_date": now_iso,
                    "created_at": now_iso,
                    "module3_handoff_payload": pr.module3_handoff_payload
                })
                pred_count += 1
        print(f"[Migration] Migrated {pred_count} prediction records to MongoDB 'predictions' collection.")

        # 5. Migrate SHAP Explanations
        exp_col = mongo_manager.get_collection("explanations")
        sql_exps = db.query(ExplanationRecord).all()
        exp_count = 0
        for ex in sql_exps:
            if not exp_col.find_one({"explanation_id": ex.explanation_id}):
                now_iso = ex.created_at.isoformat() if ex.created_at else datetime.now(timezone.utc).isoformat()
                factors = db.query(FeatureContribution).filter(FeatureContribution.explanation_id == ex.explanation_id).all()
                top_feats = [
                    {
                        "feature_name": f.feature_name,
                        "patient_value": f.patient_value,
                        "shap_value": f.shap_value,
                        "abs_shap_value": f.abs_shap_value,
                        "direction": f.direction,
                        "rank": f.rank,
                        "human_explanation": f.human_explanation
                    } for f in factors
                ]
                feat_imp = {f.feature_name: f.shap_value for f in factors}

                exp_col.insert_one({
                    "explanation_id": ex.explanation_id,
                    "prediction_id": ex.prediction_id,
                    "patient_id": ex.patient_id,
                    "disease": ex.disease,
                    "model_version": ex.model_version,
                    "explainer_type": ex.explainer_type,
                    "base_value": ex.base_value,
                    "feature_importance": feat_imp,
                    "top_features": top_feats,
                    "explanation_summary": f"SHAP explanation for {ex.disease.upper()}",
                    "created_at": now_iso,
                    "module4_handoff": ex.module4_handoff_payload
                })
                exp_count += 1
        print(f"[Migration] Migrated {exp_count} SHAP explanation records to MongoDB 'explanations' collection.")

        # 6. Migrate Wellness Plans
        plans_col = mongo_manager.get_collection("wellness_plans")
        sql_recs = db.query(RecommendationRecord).all()
        rec_count = 0
        for r in sql_recs:
            if not plans_col.find_one({"prediction_id": r.prediction_id}):
                now_iso = r.created_at.isoformat() if r.created_at else datetime.now(timezone.utc).isoformat()
                plans_col.insert_one({
                    "plan_id": f"PLAN_{r.id}",
                    "patient_id": r.patient_id,
                    "prediction_id": r.prediction_id,
                    "risk_level": r.disease,
                    "recommendations": [{
                        "category": r.category,
                        "risk_factor": r.risk_factor,
                        "recommendation": r.recommendation_text,
                        "reason": r.reason,
                        "priority": r.priority,
                        "safety_note": r.safety_note
                    }],
                    "diet_guidance": r.daily_food_plan,
                    "exercise_guidance": r.exercise_plan,
                    "lifestyle_guidance": r.daily_habits,
                    "herbal_guidance": r.herbal_wellness,
                    "generated_by": "SmartCare AI Rule Engine",
                    "created_at": now_iso,
                    "updated_at": now_iso
                })
                rec_count += 1
        print(f"[Migration] Migrated {rec_count} recommendation plans to MongoDB 'wellness_plans' collection.")

        # 7. Migrate Chat History
        chat_sess_col = mongo_manager.get_collection("chat_sessions")
        chat_msg_col = mongo_manager.get_collection("chat_messages")
        sql_chats = db.query(ChatHistory).all()
        chat_count = 0
        for ch in sql_chats:
            now_iso = ch.created_at.isoformat() if ch.created_at else datetime.now(timezone.utc).isoformat()
            if not chat_sess_col.find_one({"session_id": ch.session_id, "user_id": ch.user_id}):
                chat_sess_col.insert_one({
                    "session_id": ch.session_id,
                    "user_id": ch.user_id,
                    "patient_id": None,
                    "created_at": now_iso,
                    "updated_at": now_iso
                })
            
            chat_msg_col.insert_one({
                "message_id": f"MSG_{ch.id}",
                "session_id": ch.session_id,
                "user_id": ch.user_id,
                "sender": ch.role,
                "role": ch.role,
                "message": ch.message,
                "intent": ch.intent,
                "language": "en",
                "timestamp": now_iso,
                "created_at": now_iso
            })
            chat_count += 1
        print(f"[Migration] Migrated {chat_count} chat messages to MongoDB 'chat_messages' collection.")

        print("[Migration] SQLite to MongoDB data migration completed successfully!")
    except Exception as e:
        print(f"[Migration Warning] Migration encounter: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
