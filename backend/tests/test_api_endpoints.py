import pytest
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ONLINE"

def test_auth_registration_and_login():
    # Register test patient
    user_payload = {
        "username": "pytest_patient_1",
        "email": "pytest1@smartcare.ai",
        "password": "Password123!",
        "full_name": "PyTest Patient One",
        "role": "patient"
    }
    res = client.post("/api/auth/register", json=user_payload)
    assert res.status_code in [201, 400] # 201 or 400 if already exists

    # Login
    login_payload = {"username": "pytest_patient_1", "password": "Password123!"}
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data

def test_dataset_profiling_api():
    # Login as admin for dataset profiling
    login_payload = {"username": "admin", "password": "admin123"}
    res_login = client.post("/api/auth/login", json=login_payload)
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/datasets/ckd/profile", headers=headers)
    assert res.status_code == 200
    profile = res.json()
    assert profile["dataset_name"] == "ckd"
    assert profile["target_column"] == "classification"

def test_health_data_submit_api():
    # Login mock admin/patient
    login_payload = {"username": "pytest_patient_1", "password": "Password123!"}
    res_login = client.post("/api/auth/login", json=login_payload)
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    health_payload = {
        "age": 52,
        "sex": 1,
        "height_cm": 172,
        "weight_kg": 74,
        "high_bp": 1,
        "high_chol": 0,
        "smoker": 0,
        "phys_activity": 1,
        "ap_hi": 128,
        "ap_lo": 82,
        "glucose": 105,
        "serum_creatinine": 1.1,
        "blood_urea": 34.0,
        "hemoglobin": 14.2
    }
    res_submit = client.post("/api/health-data/submit", json=health_payload, headers=headers)
    assert res_submit.status_code == 200
    data = res_submit.json()
    assert "preprocessed_features" in data
    assert "diabetes" in data["preprocessed_features"]
