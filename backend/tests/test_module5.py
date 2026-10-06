import pytest
import os
import sys
import uuid
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.models import User, Patient, HealthRecord, PredictionRecord, ClinicalAlert, ClinicianFeedback
from app.services.risk_monitoring_service import RiskMonitoringService

client = TestClient(app)


def setup_test_users():
    """Helper to set up test patient and clinician users in DB. Returns (p1_id, p2_id, doc_user_id)."""
    db = SessionLocal()
    try:
        # Patient 1
        p1_user = db.query(User).filter(User.username == "m5_test_patient1").first()
        if not p1_user:
            p1_user = User(username="m5_test_patient1", email="p1_m5@test.com", hashed_password=hash_password("password123"), role="patient")
            db.add(p1_user)
            db.commit()
            db.refresh(p1_user)
            p1 = Patient(user_id=p1_user.id)
            db.add(p1)
            db.commit()
            db.refresh(p1)
        else:
            p1_user.hashed_password = hash_password("password123")
            p1_user.role = "patient"
            db.commit()
            p1 = p1_user.patient_profile
            if not p1:
                p1 = Patient(user_id=p1_user.id)
                db.add(p1)
                db.commit()
                db.refresh(p1)

        p1_id = p1.id

        # Patient 2
        p2_user = db.query(User).filter(User.username == "m5_test_patient2").first()
        if not p2_user:
            p2_user = User(username="m5_test_patient2", email="p2_m5@test.com", hashed_password=hash_password("password123"), role="patient")
            db.add(p2_user)
            db.commit()
            db.refresh(p2_user)
            p2 = Patient(user_id=p2_user.id)
            db.add(p2)
            db.commit()
            db.refresh(p2)
        else:
            p2_user.hashed_password = hash_password("password123")
            p2_user.role = "patient"
            db.commit()
            p2 = p2_user.patient_profile
            if not p2:
                p2 = Patient(user_id=p2_user.id)
                db.add(p2)
                db.commit()
                db.refresh(p2)

        p2_id = p2.id

        # Clinician User
        doc_user = db.query(User).filter(User.username == "m5_test_clinician").first()
        if not doc_user:
            doc_user = User(username="m5_test_clinician", email="doc_m5@test.com", hashed_password=hash_password("password123"), role="clinician", full_name="Dr. Test Specialist")
            db.add(doc_user)
            db.commit()
            db.refresh(doc_user)
        else:
            doc_user.hashed_password = hash_password("password123")
            doc_user.role = "clinician"
            db.commit()

        doc_id = doc_user.id

        return p1_id, p2_id, doc_id
    finally:
        db.close()


def get_auth_token(username, password="password123"):
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed for {username}: {res.json()}"
    return res.json()["access_token"]


def test_1_risk_trend_calculation():
    """Verify longitudinal trend calculation logic and safe clinical wording."""
    p1_id, _, _ = setup_test_users()
    db = SessionLocal()
    try:
        # Create two sequential health & prediction records
        hr1 = HealthRecord(patient_id=p1_id, ap_hi=130, ap_lo=85, glucose=110, cholesterol=200, serum_creatinine=1.0)
        db.add(hr1)
        db.commit()
        db.refresh(hr1)

        pr1 = PredictionRecord(
            prediction_id=f"PRED-{uuid.uuid4().hex[:8]}",
            patient_id=p1_id,
            diabetes_probability=0.35,
            diabetes_risk_category="LOW",
            cvd_probability=0.25,
            cvd_risk_category="LOW",
            ckd_probability=0.10,
            ckd_risk_category="LOW",
            model_version="1.0"
        )
        db.add(pr1)
        db.commit()

        hr2 = HealthRecord(patient_id=p1_id, ap_hi=145, ap_lo=95, glucose=140, cholesterol=240, serum_creatinine=1.4)
        db.add(hr2)
        db.commit()
        db.refresh(hr2)

        pr2 = PredictionRecord(
            prediction_id=f"PRED-{uuid.uuid4().hex[:8]}",
            patient_id=p1_id,
            diabetes_probability=0.65,
            diabetes_risk_category="HIGH",
            cvd_probability=0.50,
            cvd_risk_category="MODERATE",
            ckd_probability=0.25,
            ckd_risk_category="LOW",
            model_version="1.0"
        )
        db.add(pr2)
        db.commit()

        # Calculate trends
        trends = RiskMonitoringService.calculate_risk_trends(db, p1_id)

        assert trends["patient_id"] == p1_id
        assert "trends" in trends

        # Check diabetes trend (35.0% -> 65.0%: diff +30.0%)
        diabetes_trend = trends["trends"]["diabetes"]
        assert diabetes_trend["percentage_point_difference"] == pytest.approx(30.0, abs=0.5)
        assert diabetes_trend["trend_status"] == "Increasing"
        assert "increased" in diabetes_trend["safe_clinical_wording"].lower()
        # Verify safe clinical wording does NOT state definite disease progression
        assert "definite disease progression" not in diabetes_trend["safe_clinical_wording"].lower()
        assert "medical diagnosis" not in diabetes_trend["safe_clinical_wording"].lower()

    finally:
        db.close()


def test_2_automated_alert_generation():
    """Verify automated alert creation for high risk (>0.60) and significant risk increase (>0.15)."""
    p1_id, _, _ = setup_test_users()
    db = SessionLocal()
    try:
        latest_pred = db.query(PredictionRecord).filter(PredictionRecord.patient_id == p1_id).order_by(PredictionRecord.id.desc()).first()
        assert latest_pred is not None

        # Evaluate alerts for latest prediction
        alerts = RiskMonitoringService.evaluate_and_create_alerts(db, latest_pred.patient_id, latest_pred)
        assert len(alerts) >= 1

        alert_types = [a.alert_type for a in alerts]
        assert "HIGH_RISK" in alert_types or "RISK_INCREASE" in alert_types

        # Verify alerts stored in database
        db_alerts = db.query(ClinicalAlert).filter(ClinicalAlert.patient_id == p1_id, ClinicalAlert.status == "OPEN").all()
        assert len(db_alerts) >= 1
    finally:
        db.close()


def test_3_patient_risk_history_and_isolation():
    """Verify patient can view own risk history, but Patient 1 cannot access Patient 2 history (HTTP 403)."""
    p1_id, p2_id, _ = setup_test_users()

    token1 = get_auth_token("m5_test_patient1")
    token2 = get_auth_token("m5_test_patient2")

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Patient 1 gets own history -> 200 OK
    res_own = client.get(f"/api/risk-history/{p1_id}", headers=headers1)
    assert res_own.status_code == 200
    data_own = res_own.json()
    assert isinstance(data_own, list)

    # Patient 1 gets Patient 2 history -> 403 Forbidden
    res_p2 = client.get(f"/api/risk-history/{p2_id}", headers=headers1)
    assert res_p2.status_code == 403
    assert "Access denied" in res_p2.json()["detail"]

    # Patient 1 gets Patient 2 trends -> 403 Forbidden
    res_p2_trends = client.get(f"/api/risk-history/{p2_id}/trends", headers=headers1)
    assert res_p2_trends.status_code == 403

    # Patient 1 gets Patient 2 alerts -> 403 Forbidden
    res_p2_alerts = client.get(f"/api/alerts/{p2_id}", headers=headers1)
    assert res_p2_alerts.status_code == 403


def test_4_clinician_access_control():
    """Verify patients are denied access to clinician endpoints (403), but clinicians have access (200)."""
    p1_id, _, doc_id = setup_test_users()

    patient_token = get_auth_token("m5_test_patient1")
    clinician_token = get_auth_token("m5_test_clinician")

    p_headers = {"Authorization": f"Bearer {patient_token}"}
    c_headers = {"Authorization": f"Bearer {clinician_token}"}

    # Patient attempts to view clinician dashboard -> 403 Forbidden
    res_p_dash = client.get("/api/clinician/dashboard", headers=p_headers)
    assert res_p_dash.status_code == 403

    # Patient attempts to view patient roster -> 403 Forbidden
    res_p_roster = client.get("/api/clinician/patients", headers=p_headers)
    assert res_p_roster.status_code == 403

    # Clinician views dashboard -> 200 OK
    res_c_dash = client.get("/api/clinician/dashboard", headers=c_headers)
    assert res_c_dash.status_code == 200
    dash_data = res_c_dash.json()
    assert "total_patients" in dash_data
    assert "open_alerts_count" in dash_data

    # Clinician views patient roster -> 200 OK
    res_c_roster = client.get("/api/clinician/patients", headers=c_headers)
    assert res_c_roster.status_code == 200
    roster_data = res_c_roster.json()
    assert isinstance(roster_data, list)


def test_5_clinician_feedback_logging_and_prediction_immutability():
    """Verify clinician feedback is recorded properly and original prediction record remains 100% immutable."""
    p1_id, _, _ = setup_test_users()
    db = SessionLocal()
    try:
        clinician_token = get_auth_token("m5_test_clinician")
        c_headers = {"Authorization": f"Bearer {clinician_token}"}

        # Get latest prediction for Patient 1
        pred = db.query(PredictionRecord).filter(PredictionRecord.patient_id == p1_id).order_by(PredictionRecord.id.desc()).first()
        assert pred is not None

        assessment_id_str = str(pred.prediction_id)
        orig_diabetes_prob = pred.diabetes_probability
        orig_cvd_prob = pred.cvd_probability
        orig_ckd_prob = pred.ckd_probability

        # Clinician submits feedback
        feedback_payload = {
            "assessment_id": assessment_id_str,
            "patient_id": p1_id,
            "feedback_text": "Patient exhibits signs of metabolic improvement after lifestyle modification.",
            "clinical_action": "Schedule 30-day follow-up blood panel"
        }

        res_fb = client.post("/api/clinician/feedback", json=feedback_payload, headers=c_headers)
        assert res_fb.status_code == 200
        fb_data = res_fb.json()
        assert fb_data["assessment_id"] == assessment_id_str
        assert fb_data["feedback_text"] == feedback_payload["feedback_text"]

        # Verify feedback in DB
        db_fb = db.query(ClinicianFeedback).filter(ClinicianFeedback.assessment_id == assessment_id_str).first()
        assert db_fb is not None
        assert db_fb.clinical_action == "Schedule 30-day follow-up blood panel"

        # IMMUTABILITY VERIFICATION: Ensure PredictionRecord was NOT modified in any way
        db.refresh(pred)
        assert pred.diabetes_probability == orig_diabetes_prob
        assert pred.cvd_probability == orig_cvd_prob
        assert pred.ckd_probability == orig_ckd_prob

    finally:
        db.close()
