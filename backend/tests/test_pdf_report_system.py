import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.mongo_db import mongo_manager
from app.core.security import hash_password
from app.services.pdf_report_service import PDFReportService

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_report_test_users():
    """Seed test database with patients, doctors, and predictions for PDF report testing."""
    users_col = mongo_manager.get_collection("users")
    patients_col = mongo_manager.get_collection("patients")
    doctors_col = mongo_manager.get_collection("doctors")
    predictions_col = mongo_manager.get_collection("predictions")
    reports_col = mongo_manager.get_collection("reports")

    test_emails = [
        "patient_report_a@smartcare.ai",
        "patient_report_b@smartcare.ai",
        "doctor_report_rev@smartcare.ai"
    ]

    users_col.delete_many({"email": {"$in": test_emails}})
    patients_col.delete_many({"email": {"$in": test_emails}})
    doctors_col.delete_many({"email": {"$in": test_emails}})
    predictions_col.delete_many({"patient_id": {"$in": [901, 902]}})
    reports_col.delete_many({"patient_id": {"$in": [901, 902]}})

    pwd_hash = hash_password("password123")

    # Patient A (ID 901)
    users_col.insert_one({
        "user_id": 901,
        "username": "patient_report_a",
        "email": "patient_report_a@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Eleanor Health Report A",
        "role": "patient",
        "status": "active"
    })
    patients_col.insert_one({
        "patient_id": 901,
        "user_id": 901,
        "email": "patient_report_a@smartcare.ai",
        "full_name": "Eleanor Health Report A",
        "age": 45,
        "gender": "Female",
        "bmi": 26.5
    })

    # Patient B (ID 902)
    users_col.insert_one({
        "user_id": 902,
        "username": "patient_report_b",
        "email": "patient_report_b@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Marcus Health Report B",
        "role": "patient",
        "status": "active"
    })
    patients_col.insert_one({
        "patient_id": 902,
        "user_id": 902,
        "email": "patient_report_b@smartcare.ai",
        "full_name": "Marcus Health Report B"
    })

    # Doctor (ID 903)
    users_col.insert_one({
        "user_id": 903,
        "username": "doctor_report_rev",
        "email": "doctor_report_rev@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Dr. Sarah Report Reviewer",
        "role": "doctor",
        "status": "active"
    })
    doctors_col.insert_one({
        "doctor_id": 903,
        "user_id": 903,
        "name": "Dr. Sarah Report Reviewer",
        "email": "doctor_report_rev@smartcare.ai",
        "specialty": "Preventive Cardiology",
        "department": "Department of Health Intelligence",
        "verification_status": "approved"
    })

    # Seed Prediction for Patient A
    predictions_col.insert_one({
        "prediction_id": "PRED_TEST_REPORT_901",
        "patient_id": 901,
        "model_name": "SmartCare AI Multi-Disease Ensemble",
        "model_version": "v1.2.0",
        "input_features": {
            "bmi": 26.5,
            "ap_hi": 132.0,
            "ap_lo": 85.0,
            "glucose": 108.0,
            "cholesterol": 210.0
        },
        "prediction": {
            "diabetes": {"probability": 0.22, "risk_category": "MODERATE", "model_version": "v1.2.0"},
            "cardio": {"probability": 0.45, "risk_category": "HIGH", "model_version": "v1.1.0"},
            "ckd": {"probability": 0.05, "risk_category": "LOW", "model_version": "v1.0.0"}
        },
        "risk_score": {"diabetes": 0.22, "cvd": 0.45, "ckd": 0.05},
        "risk_level": {"diabetes": "MODERATE", "cvd": "HIGH", "ckd": "LOW"},
        "created_at": "2026-09-08T12:00:00Z"
    })

    yield

    users_col.delete_many({"email": {"$in": test_emails}})
    patients_col.delete_many({"email": {"$in": test_emails}})
    doctors_col.delete_many({"email": {"$in": test_emails}})
    predictions_col.delete_many({"patient_id": {"$in": [901, 902]}})
    reports_col.delete_many({"patient_id": {"$in": [901, 902]}})

def helper_login(username, password="password123"):
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    return res.json()["access_token"]

def test_1_pdf_report_service_generation():
    """Test direct generation of 7-page PDF report file via PDFReportService."""
    res = PDFReportService.generate_patient_pdf_report(patient_id=901, prediction_id="PRED_TEST_REPORT_901")
    assert "report_id" in res
    assert os.path.exists(res["file_path"]), "Generated PDF file must exist on disk"
    assert os.path.getsize(res["file_path"]) > 20000, "PDF report size should be > 20KB"
    assert res["status"] in ["AI Generated — Pending Clinician Review", "Clinician Reviewed"]

def test_2_api_generate_and_download_pdf_report():
    """Test API POST /api/reports/generate/{prediction_id} and GET /api/reports/{report_id}/download."""
    patient_a_token = helper_login("patient_report_a@smartcare.ai")
    
    # 1. Generate Report
    gen_res = client.post(
        "/api/reports/generate/PRED_TEST_REPORT_901",
        headers={"Authorization": f"Bearer {patient_a_token}"}
    )
    assert gen_res.status_code == 200
    report_data = gen_res.json()
    report_id = report_data["report_id"]
    assert report_id.startswith("RPT_")

    # 2. Download Report
    dl_res = client.get(
        f"/api/reports/{report_id}/download",
        headers={"Authorization": f"Bearer {patient_a_token}"}
    )
    assert dl_res.status_code == 200
    assert dl_res.headers["content-type"] == "application/pdf"
    assert len(dl_res.content) > 20000, "Downloaded PDF stream must be non-empty PDF content"

def test_3_doctor_review_updates_report_status():
    """Test Doctor reviewing report via PUT /api/reports/{report_id}/review updates status to 'Clinician Reviewed'."""
    patient_a_token = helper_login("patient_report_a@smartcare.ai")
    gen_res = client.post(
        "/api/reports/generate/PRED_TEST_REPORT_901",
        headers={"Authorization": f"Bearer {patient_a_token}"}
    )
    report_id = gen_res.json()["report_id"]

    doctor_token = helper_login("doctor_report_rev@smartcare.ai")
    rev_res = client.put(
        f"/api/reports/{report_id}/review",
        json={
            "notes": "Reviewed patient telemetry. Blood pressure and CVD risk require lifestyle follow-up.",
            "clinical_action": "Follow-up Recommended"
        },
        headers={"Authorization": f"Bearer {doctor_token}"}
    )
    assert rev_res.status_code == 200
    assert rev_res.json()["status"] == "Clinician Reviewed"

    # Verify report status in view endpoint
    view_res = client.get(
        f"/api/reports/{report_id}/view",
        headers={"Authorization": f"Bearer {patient_a_token}"}
    )
    assert view_res.status_code == 200
    assert view_res.json()["status"] == "Clinician Reviewed"

def test_4_patient_rbac_isolation_on_reports():
    """Verify Patient B cannot view or download Patient A's PDF report (HTTP 403)."""
    patient_a_token = helper_login("patient_report_a@smartcare.ai")
    gen_res = client.post(
        "/api/reports/generate/PRED_TEST_REPORT_901",
        headers={"Authorization": f"Bearer {patient_a_token}"}
    )
    report_id = gen_res.json()["report_id"]

    patient_b_token = helper_login("patient_report_b@smartcare.ai")
    
    # Patient B attempts to view Patient A's report details
    view_b_res = client.get(
        f"/api/reports/{report_id}/view",
        headers={"Authorization": f"Bearer {patient_b_token}"}
    )
    assert view_b_res.status_code == 403

    # Patient B attempts to download Patient A's PDF
    dl_b_res = client.get(
        f"/api/reports/{report_id}/download",
        headers={"Authorization": f"Bearer {patient_b_token}"}
    )
    assert dl_b_res.status_code == 403
