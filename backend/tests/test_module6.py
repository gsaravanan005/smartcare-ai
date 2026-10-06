import pytest
import os
import sys
import uuid
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.models import User, Patient, HealthRecord, PredictionRecord, ExplanationRecord, FeatureContribution, RecommendationRecord, ClinicalAlert, ChatHistory
from app.services.chat_service import ChatService

client = TestClient(app)


def setup_m6_test_users():
    """Sets up Patient 1, Patient 2, and Clinician users for Module 6 tests. Returns primitive IDs."""
    db = SessionLocal()
    try:
        # Patient 1
        u1 = db.query(User).filter(User.username == "m6_patient1").first()
        if not u1:
            u1 = User(username="m6_patient1", email="p1_m6@test.com", hashed_password=hash_password("pwd123"), role="patient", full_name="John Patient")
            db.add(u1)
            db.commit()
            db.refresh(u1)
            p1 = Patient(user_id=u1.id, age=52, bmi=29.5)
            db.add(p1)
            db.commit()
            db.refresh(p1)
        else:
            u1.hashed_password = hash_password("pwd123")
            u1.role = "patient"
            db.commit()
            p1 = u1.patient_profile
            if not p1:
                p1 = Patient(user_id=u1.id, age=52, bmi=29.5)
                db.add(p1)
                db.commit()
                db.refresh(p1)

        p1_id = p1.id
        u1_id = u1.id

        # Patient 2
        u2 = db.query(User).filter(User.username == "m6_patient2").first()
        if not u2:
            u2 = User(username="m6_patient2", email="p2_m6@test.com", hashed_password=hash_password("pwd123"), role="patient", full_name="Alice Patient")
            db.add(u2)
            db.commit()
            db.refresh(u2)
            p2 = Patient(user_id=u2.id, age=40, bmi=22.0)
            db.add(p2)
            db.commit()
            db.refresh(p2)
        else:
            u2.hashed_password = hash_password("pwd123")
            u2.role = "patient"
            db.commit()
            p2 = u2.patient_profile
            if not p2:
                p2 = Patient(user_id=u2.id, age=40, bmi=22.0)
                db.add(p2)
                db.commit()
                db.refresh(p2)

        p2_id = p2.id
        u2_id = u2.id

        # Clinician
        u_doc = db.query(User).filter(User.username == "m6_clinician").first()
        if not u_doc:
            u_doc = User(username="m6_clinician", email="doc_m6@test.com", hashed_password=hash_password("pwd123"), role="clinician", full_name="Dr. Smith")
            db.add(u_doc)
            db.commit()
            db.refresh(u_doc)
        else:
            u_doc.hashed_password = hash_password("pwd123")
            u_doc.role = "clinician"
            db.commit()

        doc_id = u_doc.id

        return p1_id, u1_id, p2_id, u2_id, doc_id
    finally:
        db.close()


def get_token(username, password="pwd123"):
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    return res.json()["access_token"]


def test_1_dashboard_overview_telemetry():
    """Verify dashboard overview endpoint aggregates prediction, trends, factors, recommendations, and alerts."""
    p1_id, u1_id, _, _, _ = setup_m6_test_users()
    db = SessionLocal()
    try:
        # Create health & prediction records for Patient 1
        hr = HealthRecord(patient_id=p1_id, ap_hi=140, ap_lo=90, glucose=135, cholesterol=220, serum_creatinine=1.1)
        db.add(hr)
        db.commit()
        db.refresh(hr)

        pred_id = f"PRED-M6-{uuid.uuid4().hex[:6]}"
        pr = PredictionRecord(
            prediction_id=pred_id,
            patient_id=p1_id,
            diabetes_probability=0.68,
            diabetes_risk_category="HIGH",
            cvd_probability=0.55,
            cvd_risk_category="MODERATE",
            ckd_probability=0.20,
            ckd_risk_category="LOW",
            model_version="1.0"
        )
        db.add(pr)
        db.commit()

        # SHAP feature contributions
        exp_id = f"EXP-M6-{uuid.uuid4().hex[:6]}"
        exp = ExplanationRecord(
            explanation_id=exp_id,
            prediction_id=pred_id,
            patient_id=p1_id,
            disease="MULTI-DISEASE",
            model_version="1.0",
            base_value=0.50
        )
        db.add(exp)
        db.commit()

        fc = FeatureContribution(
            explanation_id=exp_id,
            feature_name="systolic_bp",
            patient_value=140.0,
            shap_value=0.25,
            abs_shap_value=0.25,
            direction="RISK_INCREASING",
            rank=1,
            modifiable_status="Modifiable",
            human_explanation="Systolic blood pressure is elevated."
        )
        db.add(fc)
        db.commit()

        # Recommendation record
        rec = RecommendationRecord(
            patient_id=p1_id,
            prediction_id=pred_id,
            assessment_id=pred_id,
            language="en",
            disease="CARDIO",
            risk_factor="systolic_bp",
            category="Cardiovascular Wellness",
            recommendation_text="Maintain a sodium-restricted diet and engage in moderate exercise.",
            reason="Systolic blood pressure is elevated.",
            priority="High"
        )
        db.add(rec)
        db.commit()

        # Clinical Alert
        alert = ClinicalAlert(
            patient_id=p1_id,
            assessment_id=pred_id,
            alert_type="HIGH_RISK",
            severity="Clinical Review",
            message="Elevated risk score detected for DIABETES.",
            reason="Diabetes risk exceeded 60%.",
            status="OPEN"
        )
        db.add(alert)
        db.commit()

    finally:
        db.close()

    # Authenticate as Patient 1
    token1 = get_token("m6_patient1")
    headers1 = {"Authorization": f"Bearer {token1}"}

    res = client.get("/api/dashboard/overview", headers=headers1)
    assert res.status_code == 200
    d = res.json()

    assert d["patient_id"] == p1_id
    assert d["patient_name"] == "John Patient"
    assert d["disease_risks"]["diabetes"]["percentage"] == 68.0
    assert d["disease_risks"]["diabetes"]["category"] == "HIGH"
    assert len(d["top_risk_factors"]) >= 1
    assert d["top_risk_factors"][0]["feature"] == "systolic_bp"
    assert d["wellness_preview"]["category"] == "Cardiovascular Wellness"
    assert len(d["open_alerts"]) >= 1
    assert d["open_alerts"][0]["type"] == "HIGH_RISK"


def test_2_chatbot_authentication_and_safety_disclaimer():
    """Verify chat API requires authentication and includes clinical safety disclaimers."""
    # Invalid token request -> 401 Unauthorized
    res_unauth = client.post("/api/chat", json={"message": "What are my risk scores?"}, headers={"Authorization": "Bearer invalid_token_xyz"})
    assert res_unauth.status_code == 401

    token1 = get_token("m6_patient1")
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Authenticated chat request
    res = client.post("/api/chat", json={"message": "What are my current risk scores?"}, headers=headers1)
    assert res.status_code == 200
    turn = res.json()

    assert turn["intent"] == "RISK_SUMMARY"
    assert "68.0%" in turn["assistant_message"]["message"]
    assert "safety_disclaimer" in turn
    assert "does not provide medical diagnoses" in turn["safety_disclaimer"].lower()


def test_3_chatbot_intent_handling_and_contextual_responses():
    """Verify chatbot intent resolution for RISK_EXPLANATION, WELLNESS_RECOMMENDATION, and RISK_HISTORY."""
    token1 = get_token("m6_patient1")
    headers1 = {"Authorization": f"Bearer {token1}"}

    # 1. RISK_EXPLANATION intent
    res_exp = client.post("/api/chat", json={"message": "Why is my risk high?"}, headers=headers1)
    assert res_exp.status_code == 200
    turn_exp = res_exp.json()
    assert turn_exp["intent"] == "RISK_EXPLANATION"
    assert "systolic_bp" in turn_exp["assistant_message"]["message"]

    # 2. WELLNESS_RECOMMENDATION intent
    res_rec = client.post("/api/chat", json={"message": "What wellness recommendations do I have?"}, headers=headers1)
    assert res_rec.status_code == 200
    turn_rec = res_rec.json()
    assert turn_rec["intent"] == "WELLNESS_RECOMMENDATION"
    assert "Cardiovascular Wellness" in turn_rec["assistant_message"]["message"]

    # 3. ALERT_INFORMATION intent
    res_alert = client.post("/api/chat", json={"message": "Do I have any clinical alerts?"}, headers=headers1)
    assert res_alert.status_code == 200
    turn_alert = res_alert.json()
    assert turn_alert["intent"] == "ALERT_INFORMATION"
    assert "HIGH_RISK" in turn_alert["assistant_message"]["message"]


def test_4_chat_history_persistence_and_isolation():
    """Verify chat messages are stored in DB and Patient 1 cannot access Patient 2 chat history."""
    p1_id, u1_id, p2_id, u2_id, _ = setup_m6_test_users()

    token1 = get_token("m6_patient1")
    token2 = get_token("m6_patient2")

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Patient 1 sends message
    client.post("/api/chat", json={"message": "Testing chat history persistence"}, headers=headers1)

    # Patient 1 retrieves history -> 200 OK
    res_h1 = client.get("/api/chat/history", headers=headers1)
    assert res_h1.status_code == 200
    history1 = res_h1.json()
    assert len(history1) >= 2 # at least user + assistant turn
    assert any("Testing chat history persistence" in m["message"] for m in history1)

    # Patient 2 retrieves own history -> Patient 2 has separate history
    res_h2 = client.get("/api/chat/history", headers=headers2)
    assert res_h2.status_code == 200
    history2 = res_h2.json()
    # Patient 2 history must NOT contain Patient 1's messages
    assert not any("Testing chat history persistence" in m["message"] for m in history2)


def test_5_clinician_route_protection():
    """Verify patients cannot access clinician routes and clinicians cannot be impersonated."""
    p1_id, u1_id, p2_id, u2_id, doc_id = setup_m6_test_users()

    patient_token = get_token("m6_patient1")
    clinician_token = get_token("m6_clinician")

    p_headers = {"Authorization": f"Bearer {patient_token}"}
    c_headers = {"Authorization": f"Bearer {clinician_token}"}

    # Patient attempts clinician dashboard -> 403 Forbidden
    res_p_dash = client.get("/api/clinician/dashboard", headers=p_headers)
    assert res_p_dash.status_code == 403

    # Clinician attempts clinician dashboard -> 200 OK
    res_c_dash = client.get("/api/clinician/dashboard", headers=c_headers)
    assert res_c_dash.status_code == 200
