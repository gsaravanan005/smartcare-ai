import re
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from ..core.mongo_db import mongo_manager
from ..models.models import User, Patient, HealthRecord, PredictionRecord, ExplanationRecord, FeatureContribution, RecommendationRecord, ClinicalAlert, ChatHistory
from .risk_monitoring_service import RiskMonitoringService
from .recommendation_service import RecommendationService
from .audit_service import AuditLoggerService

SAFETY_DISCLAIMER = (
    "SmartCare AI provides AI-based health risk intelligence and wellness decision support. "
    "It does not provide medical diagnoses, prescribe medications, or replace professional clinical judgment. "
    "Please consult a qualified healthcare professional for clinical decisions."
)

class ChatService:

    @classmethod
    def detect_intent(cls, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["why", "explain", "shap", "reason"]):
            return "RISK_EXPLANATION"
        elif any(k in msg for k in ["factor", "influence", "top risk", "blood pressure", "glucose", "bmi"]):
            return "RISK_FACTORS"
        elif any(k in msg for k in ["recommend", "wellness", "diet", "food", "exercise", "habit", "focus", "plan"]):
            return "WELLNESS_RECOMMENDATION"
        elif any(k in msg for k in ["change", "previous", "history", "trend", "past", "compared"]):
            return "RISK_HISTORY"
        elif any(k in msg for k in ["alert", "notification", "warning", "review", "flag"]):
            return "ALERT_INFORMATION"
        elif any(k in msg for k in ["risk", "score", "diabetes", "cvd", "cardio", "ckd", "kidney", "current", "assessment", "summary"]):
            return "RISK_SUMMARY"
        else:
            return "GENERAL_WELLNESS"

    @classmethod
    def process_chat_message(cls, db: Session, user: Any, message_text: str, session_id: str = "default") -> Dict[str, Any]:
        user_id = getattr(user, "id", getattr(user, "user_id", 1))
        user_name = getattr(user, "full_name", getattr(user, "username", "Patient"))
        
        patients_col = mongo_manager.get_collection("patients")
        patient_doc = patients_col.find_one({"user_id": user_id})
        patient_id = patient_doc.get("patient_id") if patient_doc else None

        if not patient_id:
            patient_sql = db.query(Patient).filter(Patient.user_id == user_id).first()
            patient_id = patient_sql.id if patient_sql else None

        now_iso = datetime.now(timezone.utc).isoformat()

        # MongoDB Chat Session Management
        sessions_col = mongo_manager.get_collection("chat_sessions")
        session_doc = sessions_col.find_one({"session_id": session_id, "patient_id": patient_id})
        if not session_doc:
            session_doc = {
                "session_id": session_id,
                "patient_id": patient_id,
                "user_id": user_id,
                "created_at": now_iso,
                "updated_at": now_iso
            }
            sessions_col.insert_one(session_doc)

        # 1. Save user message to MongoDB chat_messages
        messages_col = mongo_manager.get_collection("chat_messages")
        user_msg_id = f"MSG_{uuid.uuid4().hex[:8].upper()}"
        user_msg_doc = {
            "id": user_msg_id,
            "message_id": user_msg_id,
            "session_id": session_id,
            "user_id": user_id,
            "patient_id": patient_id,
            "sender": "user",
            "role": "user",
            "message": message_text,
            "language": "en",
            "timestamp": now_iso,
            "created_at": now_iso
        }
        messages_col.insert_one(user_msg_doc)

        # 2. Detect Intent
        intent = cls.detect_intent(message_text)

        # 3. Retrieve Patient Context Data
        patient_context = cls._retrieve_patient_context(db, patient_id) if patient_id else {}

        # 4. Generate Contextual AI Response
        assistant_text = cls._generate_contextual_response(intent, message_text, patient_context, user_name)

        # 5. Save assistant message to MongoDB chat_messages
        assistant_msg_id = f"MSG_{uuid.uuid4().hex[:8].upper()}"
        assistant_msg_doc = {
            "id": assistant_msg_id,
            "message_id": assistant_msg_id,
            "session_id": session_id,
            "user_id": user_id,
            "patient_id": patient_id,
            "sender": "assistant",
            "role": "assistant",
            "message": assistant_text,
            "intent": intent,
            "language": "en",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        messages_col.insert_one(assistant_msg_doc)

        # Sync with SQLite for legacy compatibility
        try:
            u_msg = ChatHistory(user_id=user_id, session_id=session_id, role="user", message=message_text, created_at=datetime.now(timezone.utc))
            a_msg = ChatHistory(user_id=user_id, session_id=session_id, role="assistant", message=assistant_text, intent=intent, created_at=datetime.now(timezone.utc))
            db.add(u_msg)
            db.add(a_msg)
            db.commit()
        except Exception as e:
            print(f"[SQL Sync Chat Warning] {e}")

        AuditLoggerService.log_event(
            user_id=user_id,
            role=getattr(user, "role", "patient"),
            action="CHATBOT_INTERACTION",
            resource="chat_messages",
            resource_id=user_msg_id,
            result="SUCCESS",
            metadata={"intent": intent}
        )

        return {
            "user_message": user_msg_doc,
            "assistant_message": assistant_msg_doc,
            "intent": intent,
            "safety_disclaimer": SAFETY_DISCLAIMER
        }

    @classmethod
    def get_chat_history(cls, db: Session, user_id: int, session_id: str = "default", limit: int = 50) -> List[Dict[str, Any]]:
        messages_col = mongo_manager.get_collection("chat_messages")
        mongo_history = list(messages_col.find(
            {"user_id": user_id, "session_id": session_id},
            sort=[("timestamp", 1)],
            limit=limit
        ))

        if mongo_history:
            for item in mongo_history:
                item["id"] = item.get("id") or item.get("message_id")
            return mongo_history

        # Fallback to SQLite
        sql_history = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id,
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.created_at.asc()).limit(limit).all()

        return [
            {
                "id": h.id,
                "role": h.role,
                "message": h.message,
                "intent": h.intent,
                "created_at": h.created_at.isoformat()
            } for h in sql_history
        ]

    @classmethod
    def _retrieve_patient_context(cls, db: Session, patient_id: int) -> Dict[str, Any]:
        context = {}

        # Query MongoDB predictions collection first
        predictions_col = mongo_manager.get_collection("predictions")
        latest_pred_doc = predictions_col.find_one({"patient_id": patient_id})

        if latest_pred_doc:
            context["latest_prediction"] = {
                "id": latest_pred_doc.get("prediction_id"),
                "date": str(latest_pred_doc.get("prediction_date", ""))[:10],
                "diabetes_prob": round(latest_pred_doc.get("diabetes_probability", 0) * 100, 1),
                "diabetes_cat": latest_pred_doc.get("diabetes_risk_category", "N/A"),
                "cvd_prob": round(latest_pred_doc.get("cvd_probability", 0) * 100, 1),
                "cvd_cat": latest_pred_doc.get("cvd_risk_category", "N/A"),
                "ckd_prob": round(latest_pred_doc.get("ckd_probability", 0) * 100, 1),
                "ckd_cat": latest_pred_doc.get("ckd_risk_category", "N/A")
            }

            explanations_col = mongo_manager.get_collection("explanations")
            exp_doc = explanations_col.find_one({"prediction_id": latest_pred_doc.get("prediction_id")})
            if exp_doc and exp_doc.get("top_features"):
                context["top_factors"] = [
                    {
                        "feature": f.get("feature_name", f.get("feature", "")),
                        "value": f.get("patient_value", f.get("value", "")),
                        "explanation": f.get("human_explanation", f.get("explanation", ""))
                    } for f in exp_doc["top_features"][:5]
                ]
        else:
            # Fallback SQLite query
            latest_pred = db.query(PredictionRecord).filter(
                PredictionRecord.patient_id == patient_id
            ).order_by(PredictionRecord.created_at.desc()).first()

            if latest_pred:
                context["latest_prediction"] = {
                    "id": latest_pred.prediction_id,
                    "date": latest_pred.created_at.strftime("%Y-%m-%d"),
                    "diabetes_prob": round(latest_pred.diabetes_probability * 100, 1),
                    "diabetes_cat": latest_pred.diabetes_risk_category,
                    "cvd_prob": round(latest_pred.cvd_probability * 100, 1),
                    "cvd_cat": latest_pred.cvd_risk_category,
                    "ckd_prob": round(latest_pred.ckd_probability * 100, 1),
                    "ckd_cat": latest_pred.ckd_risk_category
                }

                exp = db.query(ExplanationRecord).filter(
                    ExplanationRecord.prediction_id == latest_pred.prediction_id
                ).first()
                if exp:
                    top_features = db.query(FeatureContribution).filter(
                        FeatureContribution.explanation_id == exp.explanation_id,
                        FeatureContribution.direction == "RISK_INCREASING"
                    ).order_by(FeatureContribution.rank.asc()).limit(5).all()

                    context["top_factors"] = [
                        {
                            "feature": f.feature_name,
                            "value": f.patient_value,
                            "explanation": f.human_explanation or f"{f.feature_name} increases risk attribution."
                        }
                        for f in top_features
                    ]

        # Trends
        try:
            trends_data = RiskMonitoringService.calculate_risk_trends(db, patient_id)
            context["trends"] = trends_data.get("trends", {})
        except Exception:
            context["trends"] = {}

        # Wellness Plans
        wellness_col = mongo_manager.get_collection("wellness_plans")
        plan_doc = wellness_col.find_one({"patient_id": patient_id})
        if plan_doc and plan_doc.get("recommendations"):
            first_rec = plan_doc["recommendations"][0] if plan_doc["recommendations"] else {}
            context["recommendations"] = {
                "risk_factor": first_rec.get("risk_factor", "General"),
                "category": first_rec.get("category", "Lifestyle"),
                "recommendation_text": first_rec.get("recommendation", first_rec.get("recommendation_text", "")),
                "safety_note": first_rec.get("safety_note", "")
            }
        else:
            rec = db.query(RecommendationRecord).filter(
                RecommendationRecord.patient_id == patient_id
            ).order_by(RecommendationRecord.created_at.desc()).first()

            if rec:
                context["recommendations"] = {
                    "risk_factor": rec.risk_factor,
                    "category": rec.category,
                    "recommendation_text": rec.recommendation_text,
                    "safety_note": rec.safety_note
                }

        # Open Alerts
        alerts = db.query(ClinicalAlert).filter(
            ClinicalAlert.patient_id == patient_id,
            ClinicalAlert.status == "OPEN"
        ).all()

        context["alerts"] = [
            {"type": a.alert_type, "severity": a.severity, "message": a.message}
            for a in alerts
        ]

        return context

    @classmethod
    def _generate_contextual_response(cls, intent: str, query: str, ctx: Dict[str, Any], user_name: str) -> str:
        pred = ctx.get("latest_prediction")
        top_factors = ctx.get("top_factors", [])
        trends = ctx.get("trends", {})
        rec = ctx.get("recommendations")
        alerts = ctx.get("alerts", [])
        q_lower = query.lower()

        if intent == "RISK_SUMMARY":
            if not pred:
                return (
                    f"Hello {user_name}, I don't see a completed risk assessment in your record yet. "
                    "You can navigate to the **Risk Assessment** tab to enter your health parameters and generate your first multi-task assessment."
                )

            if any(k in q_lower for k in ["cardio", "cvd", "heart", "cardiovascular"]):
                return (
                    f"Hello {user_name}, your latest estimated **Cardiovascular (CVD) Risk** score is **{pred['cvd_prob']}%** ({pred['cvd_cat']}), assessed on {pred['date']}.\n\n"
                    "Key influencing factors for cardiovascular risk include Blood Pressure (systolic/diastolic), BMI, Pulse Pressure, and Total Cholesterol. "
                    "You can inspect SHAP feature attributions in the **Why This Risk?** tab or view heart-healthy guidance in **Wellness Plan**."
                )
            elif any(k in q_lower for k in ["diabetes", "sugar", "glucose"]):
                return (
                    f"Hello {user_name}, your latest estimated **Diabetes Risk** score is **{pred['diabetes_prob']}%** ({pred['diabetes_cat']}), assessed on {pred['date']}.\n\n"
                    "Key influencing factors for diabetes risk include Fasting Blood Sugar, BMI, Physical Activity, and Age. "
                    "You can view glycemic-conscious food guidance under **Wellness Plan** or inspect feature attributions in **Why This Risk?**."
                )
            elif any(k in q_lower for k in ["ckd", "kidney", "renal", "creatinine", "urea"]):
                return (
                    f"Hello {user_name}, your latest estimated **Chronic Kidney Disease (CKD) Risk** score is **{pred['ckd_prob']}%** ({pred['ckd_cat']}), assessed on {pred['date']}.\n\n"
                    "Key influencing factors for kidney risk include Serum Creatinine, Blood Urea, eGFR Proxy, and Blood Pressure control. "
                    "You can view renal safety guidelines under **Wellness Plan** or inspect feature attributions in **Why This Risk?**."
                )

            return (
                f"Hello {user_name}, here is your overall estimated risk summary (assessed on {pred['date']}):\n\n"
                f"• **Diabetes Risk**: {pred['diabetes_prob']}% ({pred['diabetes_cat']})\n"
                f"• **Cardiovascular (CVD) Risk**: {pred['cvd_prob']}% ({pred['cvd_cat']})\n"
                f"• **Chronic Kidney Disease (CKD) Risk**: {pred['ckd_prob']}% ({pred['ckd_cat']})\n\n"
                "You can view detailed attributions in the **Why This Risk?** laboratory or explore targeted guidance under **Wellness Plan**."
            )

        elif intent == "RISK_EXPLANATION":
            if not top_factors:
                return (
                    f"Based on your latest assessment, the model identified your clinical feature vector. "
                    "For a deep breakdown of SHAP attributions and feature contributions, please visit the **Why This Risk?** tab."
                )

            factor_list = "\n".join([f"{i+1}. **{f['feature']}** (Value: {f['value']}): {f['explanation']}" for i, f in enumerate(top_factors[:3])])
            return (
                f"Here are the primary modifiable factors that contributed most to your risk scores:\n\n"
                f"{factor_list}\n\n"
                "The model highlights these specific features so you and your healthcare provider can focus on targeted modifiable habits."
            )

        elif intent == "RISK_FACTORS":
            if not top_factors:
                return "The model analyzes key indicators including Blood Pressure, Glucose, BMI, Cholesterol, and Serum Creatinine. Complete an assessment to see your personal attributions."
            factor_list = "\n".join([f"• **{f['feature']}**: {f['explanation']}" for f in top_factors])
            return f"Your primary risk-influencing indicators are:\n\n{factor_list}\n\nAddressing these modifiable factors can help improve your overall health trajectory."

        elif intent == "WELLNESS_RECOMMENDATION":
            if rec:
                ans = f"Your highest priority wellness guidance is in **{rec['category']}** regarding {rec['risk_factor']}:\n\n"
                ans += f"\"{rec['recommendation_text']}\"\n\n"
                if rec.get("safety_note"):
                    ans += f"⚠️ **Safety Note**: {rec['safety_note']}\n\n"
                ans += "Check the **Wellness Plan** workspace for your full 5-meal daily food guide, home exercise plan, and habit checklist."
                return ans
            return "Based on your clinical inputs, we recommend staying physically active, maintaining a balanced sodium-conscious diet, and regularly tracking blood pressure and glucose."

        elif intent == "RISK_HISTORY":
            if not trends:
                return "Longitudinal risk trends compare your current assessment against previous evaluations. Complete multiple assessments over time to track your risk trajectory."
            
            trend_str = ""
            for dis, tr in trends.items():
                trend_str += f"• **{dis.upper()}**: {tr['previous_risk_percentage']}% → {tr['current_risk_percentage']}% ({tr['trend_status']}) - *{tr['safe_clinical_wording']}*\n"
            
            return f"Here is how your risk scores have evolved over time:\n\n{trend_str}\nVisit the **Risk History & Trends** tab for complete historical records."

        elif intent == "ALERT_INFORMATION":
            if not alerts:
                return "✅ You currently have no open clinical alerts. Your estimated risk telemetry is within standard parameters."
            alert_str = "\n".join([f"• **[{a['severity']}] {a['type']}**: {a['message']}" for a in alerts])
            return f"⚠️ You currently have active clinical notifications:\n\n{alert_str}\n\nConsider discussing these observations with your healthcare professional."

        else: # GENERAL_WELLNESS
            return (
                f"I am your SmartCare AI Wellness Assistant. I can help answer questions about your estimated risk scores, "
                "SHAP feature attributions, personalized 5-meal wellness plans, and risk history trends.\n\n"
                "What would you like to explore today?"
            )

    @classmethod
    def get_dashboard_overview(cls, db: Session, user: Any) -> Dict[str, Any]:
        user_id = getattr(user, "id", getattr(user, "user_id", 1))
        user_name = getattr(user, "full_name", getattr(user, "username", "Patient"))
        
        patients_col = mongo_manager.get_collection("patients")
        patient_doc = patients_col.find_one({"user_id": user_id})
        patient_id = patient_doc.get("patient_id") if patient_doc else None

        if not patient_id:
            patient_sql = db.query(Patient).filter(Patient.user_id == user_id).first()
            patient_id = patient_sql.id if patient_sql else None

        if not patient_id:
            return {
                "patient_id": 0,
                "patient_name": user_name,
                "latest_assessment_date": None,
                "latest_assessment_id": None,
                "disease_risks": {},
                "risk_trends": None,
                "top_risk_factors": [],
                "wellness_preview": None,
                "open_alerts": [],
                "total_assessments": 0
            }

        ctx = cls._retrieve_patient_context(db, patient_id)
        
        predictions_col = mongo_manager.get_collection("predictions")
        preds_count = predictions_col.count_documents({"patient_id": patient_id})
        latest_pred_doc = predictions_col.find_one({"patient_id": patient_id})

        disease_risks = {}
        if latest_pred_doc:
            disease_risks = {
                "diabetes": {
                    "probability": latest_pred_doc.get("diabetes_probability", 0),
                    "percentage": round(latest_pred_doc.get("diabetes_probability", 0) * 100, 1),
                    "category": latest_pred_doc.get("diabetes_risk_category", "N/A")
                },
                "cvd": {
                    "probability": latest_pred_doc.get("cvd_probability", 0),
                    "percentage": round(latest_pred_doc.get("cvd_probability", 0) * 100, 1),
                    "category": latest_pred_doc.get("cvd_risk_category", "N/A")
                },
                "ckd": {
                    "probability": latest_pred_doc.get("ckd_probability", 0),
                    "percentage": round(latest_pred_doc.get("ckd_probability", 0) * 100, 1),
                    "category": latest_pred_doc.get("ckd_risk_category", "N/A")
                }
            }
        else:
            latest_pred = db.query(PredictionRecord).filter(
                PredictionRecord.patient_id == patient_id
            ).order_by(PredictionRecord.created_at.desc()).first()
            if latest_pred:
                preds_count = db.query(PredictionRecord).filter(PredictionRecord.patient_id == patient_id).count()
                disease_risks = {
                    "diabetes": {
                        "probability": latest_pred.diabetes_probability,
                        "percentage": round(latest_pred.diabetes_probability * 100, 1),
                        "category": latest_pred.diabetes_risk_category
                    },
                    "cvd": {
                        "probability": latest_pred.cvd_probability,
                        "percentage": round(latest_pred.cvd_probability * 100, 1),
                        "category": latest_pred.cvd_risk_category
                    },
                    "ckd": {
                        "probability": latest_pred.ckd_probability,
                        "percentage": round(latest_pred.ckd_probability * 100, 1),
                        "category": latest_pred.ckd_risk_category
                    }
                }

        return {
            "patient_id": patient_id,
            "patient_name": user_name,
            "latest_assessment_date": str(latest_pred_doc.get("prediction_date", ""))[:10] if latest_pred_doc else None,
            "latest_assessment_id": latest_pred_doc.get("prediction_id") if latest_pred_doc else None,
            "disease_risks": disease_risks,
            "risk_trends": ctx.get("trends"),
            "top_risk_factors": ctx.get("top_factors", []),
            "wellness_preview": ctx.get("recommendations"),
            "open_alerts": ctx.get("alerts", []),
            "total_assessments": preds_count
        }
