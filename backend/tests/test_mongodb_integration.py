import pytest
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.mongo_db import mongo_manager
from app.core.security import hash_password, verify_password

client = TestClient(app)

def test_1_password_hashing_and_verification():
    raw_pwd = "SecurePassword2026!"
    hashed = hash_password(raw_pwd)
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_2_mongodb_collection_indexing():
    users_col = mongo_manager.get_collection("users")
    patients_col = mongo_manager.get_collection("patients")
    doctors_col = mongo_manager.get_collection("doctors")
    admins_col = mongo_manager.get_collection("admins")
    preds_col = mongo_manager.get_collection("predictions")

    assert users_col is not None
    assert patients_col is not None
    assert doctors_col is not None
    assert admins_col is not None
    assert preds_col is not None

def test_3_patient_registration_and_login_flow():
    reg_payload = {
        "username": "mongo_test_patient",
        "email": "mongo_patient@smartcare.ai",
        "password": "PatientPassword123!",
        "full_name": "MongoDB Patient User",
        "role": "patient"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code in [201, 400]

    login_payload = {
        "username": "mongo_patient@smartcare.ai",
        "password": "PatientPassword123!"
    }
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["role"] == "patient"

def test_4_doctor_registration_and_login_flow():
    reg_payload = {
        "username": "mongo_test_doctor",
        "email": "mongo_doctor@smartcare.ai",
        "password": "DoctorPassword123!",
        "full_name": "Dr. MongoDB Test Doctor",
        "role": "doctor"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code in [201, 400]

    login_payload = {
        "username": "mongo_doctor@smartcare.ai",
        "password": "DoctorPassword123!"
    }
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["role"] == "doctor"

def test_5_public_admin_registration_blocked():
    reg_payload = {
        "username": "public_hacker_admin",
        "email": "hacker@smartcare.ai",
        "password": "HackerPassword123!",
        "full_name": "Public Admin Attempt",
        "role": "admin"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code == 403
    assert "restricted" in res_reg.json()["detail"].lower()

def test_6_invalid_credentials_denied():
    bad_login = {"username": "admin@smartcare.ai", "password": "WrongPassword123!"}
    res = client.post("/api/auth/login", json=bad_login)
    assert res.status_code == 401

def test_7_prediction_and_shap_mongo_persistence():
    # Login patient
    login_res = client.post("/api/auth/login", json={"username": "patient@smartcare.ai", "password": "patient123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Predict risk
    health_payload = {
        "age": 55,
        "sex": 1,
        "height_cm": 178,
        "weight_kg": 82,
        "high_bp": 1,
        "high_chol": 1,
        "smoker": 0,
        "phys_activity": 1,
        "ap_hi": 135,
        "ap_lo": 88,
        "glucose": 110,
        "serum_creatinine": 1.2,
        "blood_urea": 36.0,
        "hemoglobin": 14.0
    }
    res_pred = client.post("/api/predictions", json=health_payload, headers=headers)
    assert res_pred.status_code == 200
    pred_data = res_pred.json()
    pred_id = pred_data["prediction_id"]

    # Verify MongoDB persistence in predictions collection
    preds_col = mongo_manager.get_collection("predictions")
    doc = preds_col.find_one({"prediction_id": pred_id})
    assert doc is not None
    assert doc["model_name"] == "SmartCare AI Multi-Disease Ensemble"

    # Generate SHAP explanation
    res_shap = client.post(f"/api/explanations?prediction_id={pred_id}&disease=diabetes", headers=headers)
    assert res_shap.status_code == 200
    exp_data = res_shap.json()
    exp_id = exp_data["explanation_id"]

    # Verify MongoDB persistence in explanations collection
    exp_col = mongo_manager.get_collection("explanations")
    exp_doc = exp_col.find_one({"explanation_id": exp_id})
    assert exp_doc is not None
    assert "top_features" in exp_doc

def test_8_wellness_plan_mongo_persistence():
    login_res = client.post("/api/auth/login", json={"username": "patient@smartcare.ai", "password": "patient123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res_plan = client.post("/api/recommendations/generate", json={"language": "en"}, headers=headers)
    assert res_plan.status_code == 200
    plan_data = res_plan.json()
    assert "recommendations" in plan_data

    wellness_col = mongo_manager.get_collection("wellness_plans")
    plans = list(wellness_col.find())
    assert len(plans) > 0

def test_9_chatbot_session_and_messages_mongo_persistence():
    login_res = client.post("/api/auth/login", json={"username": "patient@smartcare.ai", "password": "patient123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    chat_payload = {"message": "What are my current risk scores?", "session_id": "test_mongo_session"}
    res_chat = client.post("/api/chat", json=chat_payload, headers=headers)
    assert res_chat.status_code == 200
    chat_data = res_chat.json()
    assert "assistant_message" in chat_data

    # Check MongoDB collections
    sess_col = mongo_manager.get_collection("chat_sessions")
    msg_col = mongo_manager.get_collection("chat_messages")
    
    assert sess_col.find_one({"session_id": "test_mongo_session"}) is not None
    assert msg_col.count_documents({"session_id": "test_mongo_session"}) >= 2

def test_10_admin_doctor_verification_workflow():
    # Login admin
    login_res = client.post("/api/auth/login", json={"username": "admin@smartcare.ai", "password": "admin123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get doctors list
    res_docs = client.get("/api/admin/doctors", headers=headers)
    assert res_docs.status_code == 200
    docs_list = res_docs.json()
    assert len(docs_list) > 0

    doc_id = docs_list[0]["doctor_id"]

    # Verify doctor
    verify_payload = {"verification_status": "approved", "notes": "Verified board license."}
    res_verify = client.put(f"/api/admin/doctors/{doc_id}/verify", json=verify_payload, headers=headers)
    assert res_verify.status_code == 200
    assert res_verify.json()["verification_status"] == "approved"

def test_11_audit_logs_and_notifications():
    login_res = client.post("/api/auth/login", json={"username": "admin@smartcare.ai", "password": "admin123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res_audit = client.get("/api/admin/audit-logs", headers=headers)
    assert res_audit.status_code == 200
    logs = res_audit.json()
    assert len(logs) > 0

    # Ensure passwords are not exposed in metadata
    for log in logs:
        meta = log.get("metadata", {})
        for k in meta:
            assert "password" not in k.lower() or meta[k] == "[REDACTED]"
