"""
SmartCare AI - Module 5 Risk Monitoring & Clinical Decision Support Service
Orchestrates patient risk history tracking, risk trend calculation, automated clinical alert generation,
clinician dashboard aggregation, and clinician feedback logging while preserving original ML predictions.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from ..models.models import User, Patient, PredictionRecord, ExplanationRecord, FeatureContribution, RecommendationRecord, ClinicalAlert, ClinicianFeedback
from ..services.recommendation_service import RecommendationService
from ..core.mongo_db import mongo_manager

logger = logging.getLogger(__name__)

class RiskMonitoringService:

    # Configurable Clinical Decision Support Thresholds
    RISK_HIGH_THRESHOLD = 0.60
    RISK_INCREASE_THRESHOLD = 0.15
    CONFIDENCE_UNCERTAINTY_BOUND = 0.03

    @classmethod
    def evaluate_and_create_alerts(cls, db: Session, patient_id: int, pred_record: PredictionRecord) -> List[ClinicalAlert]:
        """
        Evaluates clinical alert rules on a prediction record and persists generated alerts in the DB.
        """
        created_alerts = []

        # 1. High-Risk Rule (Risk >= 60%)
        elevated_diseases = []
        if pred_record.diabetes_probability >= cls.RISK_HIGH_THRESHOLD:
            elevated_diseases.append("DIABETES")
        if pred_record.cvd_probability >= cls.RISK_HIGH_THRESHOLD:
            elevated_diseases.append("CARDIOVASCULAR DISEASE")
        if pred_record.ckd_probability >= cls.RISK_HIGH_THRESHOLD:
            elevated_diseases.append("CHRONIC KIDNEY DISEASE")

        if elevated_diseases:
            dis_str = ", ".join(elevated_diseases)
            msg = f"Elevated risk score detected for {dis_str}. Clinical review is recommended."
            reason = f"Model probability for {dis_str} exceeded the high-risk threshold ({cls.RISK_HIGH_THRESHOLD * 100:.0f}%)."
            
            existing = db.query(ClinicalAlert).filter(
                ClinicalAlert.patient_id == patient_id,
                ClinicalAlert.assessment_id == pred_record.prediction_id,
                ClinicalAlert.alert_type == "HIGH_RISK"
            ).first()
            if not existing:
                alert = ClinicalAlert(
                    patient_id=patient_id,
                    assessment_id=pred_record.prediction_id,
                    alert_type="HIGH_RISK",
                    severity="Clinical Review",
                    message=msg,
                    reason=reason,
                    status="OPEN"
                )
                db.add(alert)
                created_alerts.append(alert)

        # 2. Risk Increase Trend Rule (Compare with previous prediction)
        prev_pred = db.query(PredictionRecord).filter(
            PredictionRecord.patient_id == patient_id,
            PredictionRecord.prediction_id != pred_record.prediction_id
        ).order_by(PredictionRecord.created_at.desc()).first()

        if prev_pred:
            increased_diseases = []
            if (pred_record.diabetes_probability - prev_pred.diabetes_probability) >= cls.RISK_INCREASE_THRESHOLD:
                increased_diseases.append(f"Diabetes (+{(pred_record.diabetes_probability - prev_pred.diabetes_probability)*100:.1f}%)")
            if (pred_record.cvd_probability - prev_pred.cvd_probability) >= cls.RISK_INCREASE_THRESHOLD:
                increased_diseases.append(f"CVD (+{(pred_record.cvd_probability - prev_pred.cvd_probability)*100:.1f}%)")
            if (pred_record.ckd_probability - prev_pred.ckd_probability) >= cls.RISK_INCREASE_THRESHOLD:
                increased_diseases.append(f"CKD (+{(pred_record.ckd_probability - prev_pred.ckd_probability)*100:.1f}%)")

            if increased_diseases:
                inc_str = ", ".join(increased_diseases)
                msg = f"Your estimated risk score has increased for {inc_str}."
                reason = f"Significant increase in risk prediction between consecutive assessments."
                
                existing = db.query(ClinicalAlert).filter(
                    ClinicalAlert.patient_id == patient_id,
                    ClinicalAlert.assessment_id == pred_record.prediction_id,
                    ClinicalAlert.alert_type == "RISK_INCREASE"
                ).first()
                if not existing:
                    alert = ClinicalAlert(
                        patient_id=patient_id,
                        assessment_id=pred_record.prediction_id,
                        alert_type="RISK_INCREASE",
                        severity="Clinical Review" if any("+" in s for s in increased_diseases) else "Monitor",
                        message=msg,
                        reason=reason,
                        status="OPEN"
                    )
                    db.add(alert)
                    created_alerts.append(alert)

        # 3. Low Model Confidence / Threshold Boundary Rule
        low_conf_diseases = []
        for dis, prob in [("Diabetes", pred_record.diabetes_probability), ("CVD", pred_record.cvd_probability), ("CKD", pred_record.ckd_probability)]:
            if abs(prob - 0.50) <= cls.CONFIDENCE_UNCERTAINTY_BOUND or abs(prob - 0.40) <= cls.CONFIDENCE_UNCERTAINTY_BOUND:
                low_conf_diseases.append(dis)

        if low_conf_diseases:
            dis_str = ", ".join(low_conf_diseases)
            msg = f"Borderline prediction confidence observed for {dis_str}."
            reason = f"Model probability is close to decision threshold boundary. Clinical verification advised."
            
            existing = db.query(ClinicalAlert).filter(
                ClinicalAlert.patient_id == patient_id,
                ClinicalAlert.assessment_id == pred_record.prediction_id,
                ClinicalAlert.alert_type == "LOW_CONFIDENCE"
            ).first()
            if not existing:
                alert = ClinicalAlert(
                    patient_id=patient_id,
                    assessment_id=pred_record.prediction_id,
                    alert_type="LOW_CONFIDENCE",
                    severity="Monitor",
                    message=msg,
                    reason=reason,
                    status="OPEN"
                )
                db.add(alert)
                created_alerts.append(alert)

        db.commit()
        return created_alerts

    @classmethod
    def _resolve_candidate_patient_ids(cls, patient_id: int) -> List[int]:
        candidates = {patient_id}
        try:
            patients_col = mongo_manager.get_collection("patients")
            p_docs = list(patients_col.find({"$or": [{"patient_id": patient_id}, {"user_id": patient_id}, {"id": patient_id}]}))
            for p in p_docs:
                for k in ["patient_id", "user_id", "id"]:
                    if k in p and p[k] is not None:
                        try:
                            candidates.add(int(p[k]))
                        except (ValueError, TypeError):
                            pass
        except Exception:
            pass
        return list(candidates)

    @classmethod
    def get_patient_risk_history(cls, db: Session, patient_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves chronological risk assessment history for a patient from MongoDB & SQLite.
        """
        candidate_ids = cls._resolve_candidate_patient_ids(patient_id)
        history = []
        seen_ids = set()

        # 1. Query MongoDB predictions collection
        try:
            predictions_col = mongo_manager.get_collection("predictions")
            m_preds = list(predictions_col.find(
                {"patient_id": {"$in": candidate_ids}},
                sort=[("created_at", -1), ("prediction_date", -1)]
            ))
            for m in m_preds:
                pid = m.get("prediction_id", str(m.get("_id")))
                if pid in seen_ids:
                    continue
                seen_ids.add(pid)

                created_at_val = m.get("created_at") or m.get("prediction_date") or datetime.now(timezone.utc).isoformat()
                if isinstance(created_at_val, datetime):
                    created_at_val = created_at_val.isoformat()

                d_prob = m.get("diabetes_probability") if m.get("diabetes_probability") is not None else m.get("risk_score", {}).get("diabetes", 0.0)
                cvd_prob = m.get("cvd_probability") if m.get("cvd_probability") is not None else m.get("risk_score", {}).get("cvd", 0.0)
                ckd_prob = m.get("ckd_probability") if m.get("ckd_probability") is not None else m.get("risk_score", {}).get("ckd", 0.0)

                d_cat = m.get("diabetes_risk_category") or m.get("risk_level", {}).get("diabetes", "LOW")
                cvd_cat = m.get("cvd_risk_category") or m.get("risk_level", {}).get("cvd", "LOW")
                ckd_cat = m.get("ckd_risk_category") or m.get("risk_level", {}).get("ckd", "LOW")

                is_critical = (d_prob >= cls.RISK_HIGH_THRESHOLD or cvd_prob >= cls.RISK_HIGH_THRESHOLD or ckd_prob >= cls.RISK_HIGH_THRESHOLD)
                
                history.append({
                    "assessment_id": pid,
                    "patient_id": patient_id,
                    "created_at": created_at_val,
                    "diabetes": {
                        "probability": d_prob,
                        "risk_percentage": round(d_prob * 100, 1),
                        "risk_category": str(d_cat).upper()
                    },
                    "cvd": {
                        "probability": cvd_prob,
                        "risk_percentage": round(cvd_prob * 100, 1),
                        "risk_category": str(cvd_cat).upper()
                    },
                    "ckd": {
                        "probability": ckd_prob,
                        "risk_percentage": round(ckd_prob * 100, 1),
                        "risk_category": str(ckd_cat).upper()
                    },
                    "model_version": m.get("model_version", "v1.0.0"),
                    "alert_status": "Clinical Review" if is_critical else "Normal",
                    "alerts_count": 1 if is_critical else 0
                })
        except Exception as e:
            logger.warning(f"MongoDB risk history query note: {e}")

        # 2. Query SQLite PredictionRecord
        try:
            s_preds = db.query(PredictionRecord).filter(
                PredictionRecord.patient_id.in_(candidate_ids)
            ).order_by(PredictionRecord.created_at.desc()).all()

            for p in s_preds:
                if p.prediction_id in seen_ids:
                    continue
                seen_ids.add(p.prediction_id)

                alerts = db.query(ClinicalAlert).filter(
                    ClinicalAlert.patient_id.in_(candidate_ids),
                    ClinicalAlert.assessment_id == p.prediction_id
                ).all()

                alert_status = "Normal"
                if any(a.severity == "Clinical Review" for a in alerts):
                    alert_status = "Clinical Review"
                elif any(a.severity == "Monitor" for a in alerts):
                    alert_status = "Monitor"

                history.append({
                    "assessment_id": p.prediction_id,
                    "patient_id": patient_id,
                    "created_at": p.created_at.isoformat() if hasattr(p.created_at, "isoformat") else str(p.created_at),
                    "diabetes": {
                        "probability": p.diabetes_probability,
                        "risk_percentage": round(p.diabetes_probability * 100, 1),
                        "risk_category": (p.diabetes_risk_category or "LOW").upper()
                    },
                    "cvd": {
                        "probability": p.cvd_probability,
                        "risk_percentage": round(p.cvd_probability * 100, 1),
                        "risk_category": (p.cvd_risk_category or "LOW").upper()
                    },
                    "ckd": {
                        "probability": p.ckd_probability,
                        "risk_percentage": round(p.ckd_probability * 100, 1),
                        "risk_category": (p.ckd_risk_category or "LOW").upper()
                    },
                    "model_version": p.model_version or "v1.0.0",
                    "alert_status": alert_status,
                    "alerts_count": len(alerts)
                })
        except Exception as e:
            logger.warning(f"SQLite risk history query note: {e}")

        # Sort combined history by created_at descending
        history.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return history

    @classmethod
    def calculate_risk_trends(cls, db: Session, patient_id: int) -> Dict[str, Any]:
        """
        Calculates risk trends between current and previous assessments with safe clinical wording.
        """
        history = cls.get_patient_risk_history(db, patient_id)

        if not history:
            return {
                "patient_id": patient_id,
                "latest_assessment_id": None,
                "previous_assessment_id": None,
                "trends": {},
                "overall_alert_status": "Normal",
                "calculated_at": datetime.now(timezone.utc).isoformat()
            }

        curr = history[0]
        prev = history[1] if len(history) > 1 else None

        trends = {}
        for disease in ["diabetes", "cvd", "ckd"]:
            curr_info = curr.get(disease, {})
            curr_pct = curr_info.get("risk_percentage", 0.0)
            
            if prev and disease in prev:
                prev_pct = prev[disease].get("risk_percentage", curr_pct)
            else:
                prev_pct = curr_pct

            diff_pct = round(curr_pct - prev_pct, 1)

            if diff_pct > 1.0:
                status = "Increasing"
                safe_wording = f"Your estimated risk score for {disease.upper()} has increased by {diff_pct} percentage points."
            elif diff_pct < -1.0:
                status = "Decreasing"
                safe_wording = f"Your estimated risk score for {disease.upper()} has decreased by {abs(diff_pct)} percentage points."
            else:
                status = "Stable"
                safe_wording = f"Your estimated risk score for {disease.upper()} remains stable."

            trends[disease] = {
                "disease": disease.upper(),
                "previous_risk_percentage": prev_pct,
                "current_risk_percentage": curr_pct,
                "percentage_point_difference": diff_pct,
                "trend_status": status,
                "safe_clinical_wording": safe_wording
            }

        overall_status = curr.get("alert_status", "Normal")

        return {
            "patient_id": patient_id,
            "latest_assessment_id": curr.get("assessment_id"),
            "previous_assessment_id": prev.get("assessment_id") if prev else None,
            "trends": trends,
            "overall_alert_status": overall_status,
            "calculated_at": datetime.now(timezone.utc).isoformat()
        }

    @classmethod
    def get_assessment_details(cls, db: Session, assessment_id: str) -> Dict[str, Any]:
        """
        Retrieves complete assessment details including ML predictions, SHAP factors, recommendations, and alerts.
        """
        # 1. Search in MongoDB
        mongo_doc = None
        try:
            predictions_col = mongo_manager.get_collection("predictions")
            mongo_doc = predictions_col.find_one({"prediction_id": assessment_id})
        except Exception:
            pass

        # 2. Search in SQLite
        pred_rec = db.query(PredictionRecord).filter(PredictionRecord.prediction_id == assessment_id).first()

        if not mongo_doc and not pred_rec:
            return {}

        target_patient_id = (mongo_doc.get("patient_id") if mongo_doc else None) or (pred_rec.patient_id if pred_rec else 1)
        created_at_val = (mongo_doc.get("created_at") if mongo_doc else None) or (pred_rec.created_at.isoformat() if pred_rec and hasattr(pred_rec.created_at, "isoformat") else datetime.now(timezone.utc).isoformat())

        d_prob = (mongo_doc.get("diabetes_probability") if mongo_doc and "diabetes_probability" in mongo_doc else None) or (pred_rec.diabetes_probability if pred_rec else 0.0)
        cvd_prob = (mongo_doc.get("cvd_probability") if mongo_doc and "cvd_probability" in mongo_doc else None) or (pred_rec.cvd_probability if pred_rec else 0.0)
        ckd_prob = (mongo_doc.get("ckd_probability") if mongo_doc and "ckd_probability" in mongo_doc else None) or (pred_rec.ckd_probability if pred_rec else 0.0)

        d_cat = (mongo_doc.get("diabetes_risk_category") if mongo_doc else None) or (pred_rec.diabetes_risk_category if pred_rec else "LOW")
        cvd_cat = (mongo_doc.get("cvd_risk_category") if mongo_doc else None) or (pred_rec.cvd_risk_category if pred_rec else "LOW")
        ckd_cat = (mongo_doc.get("ckd_risk_category") if mongo_doc else None) or (pred_rec.ckd_risk_category if pred_rec else "LOW")

        plan = RecommendationService.generate_recommendation_plan(
            db=db,
            patient_id=target_patient_id,
            prediction_id=assessment_id,
            language="en"
        )

        alerts = db.query(ClinicalAlert).filter(ClinicalAlert.assessment_id == assessment_id).all()
        feedbacks = db.query(ClinicianFeedback).filter(ClinicianFeedback.assessment_id == assessment_id).all()

        return {
            "assessment_id": assessment_id,
            "patient_id": target_patient_id,
            "created_at": created_at_val if isinstance(created_at_val, str) else str(created_at_val),
            "prediction": {
                "diabetes": {"probability": d_prob, "risk_category": str(d_cat).upper()},
                "cvd": {"probability": cvd_prob, "risk_category": str(cvd_cat).upper()},
                "ckd": {"probability": ckd_prob, "risk_category": str(ckd_cat).upper()},
                "model_version": (mongo_doc.get("model_version") if mongo_doc else None) or (pred_rec.model_version if pred_rec else "v1.0.0")
            },
            "shap_factors": plan.get("modifiable_factors", []),
            "recommendations": plan.get("recommendations", []),
            "daily_food_plan": plan.get("daily_food_plan"),
            "exercise_plan": plan.get("exercise_plan"),
            "daily_habits": plan.get("daily_habits"),
            "herbal_wellness": plan.get("herbal_wellness"),
            "monitoring_guidance": plan.get("monitoring_guidance"),
            "alerts": [
                {
                    "id": a.id,
                    "alert_type": a.alert_type,
                    "severity": a.severity,
                    "message": a.message,
                    "reason": a.reason,
                    "status": a.status,
                    "created_at": a.created_at.isoformat()
                } for a in alerts
            ],
            "clinician_feedbacks": [
                {
                    "id": f.id,
                    "clinician_id": f.clinician_id,
                    "feedback_text": f.feedback_text,
                    "clinical_action": f.clinical_action,
                    "created_at": f.created_at.isoformat()
                } for f in feedbacks
            ]
        }

    @classmethod
    def get_clinician_dashboard_metrics(cls, db: Session) -> Dict[str, Any]:
        """
        Aggregates clinician dashboard statistics and recent open alerts.
        """
        total_patients = db.query(Patient).count()
        recent_assessments_count = db.query(PredictionRecord).count()
        open_alerts = db.query(ClinicalAlert).filter(ClinicalAlert.status == "OPEN").order_by(ClinicalAlert.created_at.desc()).all()
        
        patients_requiring_review = db.query(ClinicalAlert.patient_id).filter(
            ClinicalAlert.status == "OPEN",
            ClinicalAlert.severity == "Clinical Review"
        ).distinct().count()

        return {
            "total_patients": total_patients,
            "patients_requiring_review": patients_requiring_review,
            "recent_assessments_count": recent_assessments_count,
            "open_alerts_count": len(open_alerts),
            "recent_alerts": open_alerts[:10]
        }

    @classmethod
    def get_clinician_patient_list(cls, db: Session, doctor_id: Optional[int] = None, is_admin: bool = False) -> List[Dict[str, Any]]:
        """
        Returns authorized patient roster with latest risk scores and alert status for clinician view.
        If clinician/doctor, filters only assigned patients.
        """
        patients = db.query(Patient).all()
        roster = []

        # Find assigned patient IDs if doctor_id is provided and not admin
        assigned_pids = None
        if doctor_id and not is_admin:
            rel_col = mongo_manager.get_collection("doctor_patient_relationships")
            assigned_rels = list(rel_col.find({
                "$or": [{"doctor_id": doctor_id}, {"user_id": doctor_id}],
                "relationship_status": {"$in": ["active", "assigned", "ACTIVE", "ASSIGNED"]}
            }))
            assigned_pids = set([r.get("patient_id") for r in assigned_rels])

            # Also check patients collection
            patients_col = mongo_manager.get_collection("patients")
            pat_docs = list(patients_col.find({"doctor_id": doctor_id}))
            for pd in pat_docs:
                assigned_pids.add(pd.get("patient_id", pd.get("id")))

            # Fallback for default demo doctors if no explicit assignments exist
            if not assigned_pids and doctor_id in [1, 2, 100, 101, 802]:
                assigned_pids = set([p.id for p in patients if p.id in [1, 100, 101, 801, 4]])

        for p in patients:
            if assigned_pids is not None and p.id not in assigned_pids and p.user_id not in assigned_pids:
                continue

            latest_pred = db.query(PredictionRecord).filter(
                PredictionRecord.patient_id == p.id
            ).order_by(PredictionRecord.created_at.desc()).first()

            open_alerts = db.query(ClinicalAlert).filter(
                ClinicalAlert.patient_id == p.id,
                ClinicalAlert.status == "OPEN"
            ).all()

            alert_status = "Normal"
            if any(a.severity == "Clinical Review" for a in open_alerts):
                alert_status = "Clinical Review"
            elif any(a.severity == "Monitor" for a in open_alerts):
                alert_status = "Monitor"

            user_obj = db.query(User).filter(User.id == p.user_id).first()
            patient_name = user_obj.full_name or user_obj.username if user_obj else f"Patient #{p.id}"

            roster.append({
                "patient_id": p.id,
                "patient_name": patient_name,
                "age": p.age,
                "sex": "Male" if p.sex == 1 else "Female" if p.sex == 0 else "N/A",
                "last_assessment_date": latest_pred.created_at.isoformat() if latest_pred else None,
                "diabetes_risk_percentage": round(latest_pred.diabetes_probability * 100, 1) if latest_pred else 0.0,
                "cvd_risk_percentage": round(latest_pred.cvd_probability * 100, 1) if latest_pred else 0.0,
                "ckd_risk_percentage": round(latest_pred.ckd_probability * 100, 1) if latest_pred else 0.0,
                "alert_status": alert_status,
                "open_alerts_count": len(open_alerts)
            })

        return roster

    @classmethod
    def add_clinician_feedback(
        cls,
        db: Session,
        clinician_user: User,
        assessment_id: str,
        patient_id: int,
        feedback_text: str,
        clinical_action: str
    ) -> ClinicianFeedback:
        """
        Logs clinician feedback and action for an assessment. Strictly preserves original ML prediction immutability.
        """
        feedback = ClinicianFeedback(
            assessment_id=assessment_id,
            patient_id=patient_id,
            clinician_id=clinician_user.id,
            feedback_text=feedback_text,
            clinical_action=clinical_action or "Reviewed"
        )
        db.add(feedback)

        # Update open alerts for this assessment if action taken
        if clinical_action in ["Reviewed", "Continue Monitoring", "No Further Action"]:
            db.query(ClinicalAlert).filter(
                ClinicalAlert.assessment_id == assessment_id,
                ClinicalAlert.status == "OPEN"
            ).update({
                "status": "REVIEWED",
                "reviewed_at": datetime.now(timezone.utc),
                "reviewed_by": clinician_user.full_name or clinician_user.username
            })

        db.commit()
        db.refresh(feedback)
        return feedback
