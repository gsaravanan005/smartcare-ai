import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, apply_db_migrations, seed_default_users
from app.core.security import hash_password, create_access_token
from app.core.mongo_db import mongo_manager

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    apply_db_migrations()
    db = SessionLocal()
    seed_default_users(db)
    db.close()

# -------------------------------------------------------------
# 1. PATIENT AUTHENTICATION TESTS
# -------------------------------------------------------------
def test_valid_patient_login():
    response = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123",
        "target_role": "patient"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "patient"
    assert data["status"] == "active"

def test_invalid_patient_password():
    response = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "wrong_password_999",
        "target_role": "patient"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email/ID or password."

def test_inactive_patient_login_blocked():
    # Insert or update inactive patient
    users_col = mongo_manager.get_collection("users")
    users_col.update_one(
        {"email": "inactive_patient@smartcare.ai"},
        {"$set": {
            "user_id": 991,
            "username": "inactive_patient",
            "email": "inactive_patient@smartcare.ai",
            "password_hash": hash_password("patient123"),
            "role": "patient",
            "status": "inactive"
        }},
        upsert=True
    )
    
    response = client.post("/api/auth/login", json={
        "username": "inactive_patient@smartcare.ai",
        "password": "patient123",
        "target_role": "patient"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Your account is currently inactive. Please contact support."

# -------------------------------------------------------------
# 2. DOCTOR AUTHENTICATION TESTS
# -------------------------------------------------------------
def test_valid_doctor_login():
    response = client.post("/api/auth/login", json={
        "username": "doctor@smartcare.ai",
        "password": "doctor123",
        "target_role": "doctor"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] in ["doctor", "clinician"]

def test_invalid_doctor_password():
    response = client.post("/api/auth/login", json={
        "username": "doctor@smartcare.ai",
        "password": "invalid_doctor_password",
        "target_role": "doctor"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email/ID or password."

def test_pending_doctor_login_blocked():
    users_col = mongo_manager.get_collection("users")
    users_col.update_one(
        {"email": "pending_doctor@smartcare.ai"},
        {"$set": {
            "user_id": 992,
            "username": "pending_doctor",
            "email": "pending_doctor@smartcare.ai",
            "password_hash": hash_password("doctor123"),
            "role": "doctor",
            "status": "pending"
        }},
        upsert=True
    )

    response = client.post("/api/auth/login", json={
        "username": "pending_doctor@smartcare.ai",
        "password": "doctor123",
        "target_role": "doctor"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Your account is awaiting verification."

# -------------------------------------------------------------
# 3. ADMIN AUTHENTICATION & PUBLIC REGISTRATION BLOCK TESTS
# -------------------------------------------------------------
def test_valid_admin_login():
    response = client.post("/api/auth/login", json={
        "username": "admin@smartcare.ai",
        "password": "admin123",
        "target_role": "admin"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] in ["admin", "super_admin"]

def test_invalid_admin_password():
    response = client.post("/api/auth/login", json={
        "username": "admin@smartcare.ai",
        "password": "wrongadminpassword",
        "target_role": "admin"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email/ID or password."

def test_public_admin_registration_forbidden():
    response = client.post("/api/auth/register", json={
        "username": "hacker_admin",
        "email": "hacker_admin@smartcare.ai",
        "password": "hackerpassword123",
        "role": "admin"
    })
    assert response.status_code == 403
    assert "Public administrator registration is restricted" in response.json()["detail"]

# -------------------------------------------------------------
# 4. ROLE SECURITY & ACCESS CONTROL TESTS
# -------------------------------------------------------------
def test_patient_portal_role_mismatch():
    # Attempting to log into Patient portal using Doctor credentials
    response = client.post("/api/auth/login", json={
        "username": "doctor@smartcare.ai",
        "password": "doctor123",
        "target_role": "patient"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not authorized to access this portal."

def test_doctor_portal_role_mismatch():
    # Attempting to log into Doctor portal using Patient credentials
    response = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123",
        "target_role": "doctor"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not authorized to access this portal."

def test_patient_cannot_access_clinician_api():
    # Get Patient token
    patient_res = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123"
    })
    token = patient_res.json()["access_token"]

    # Attempt to call clinician dashboard endpoint with Patient token
    response = client.get("/api/clinician/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "authorization required" in response.json()["detail"].lower() or "not authorized" in response.json()["detail"].lower()

def test_doctor_cannot_access_admin_api():
    doctor_res = client.post("/api/auth/login", json={
        "username": "doctor@smartcare.ai",
        "password": "doctor123"
    })
    token = doctor_res.json()["access_token"]

    # Attempt to access admin router endpoint
    response = client.get("/api/admin/audit-logs", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not authorized to access this portal."

def test_unauthenticated_access_denied():
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_logout_endpoint():
    patient_res = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123"
    })
    token = patient_res.json()["access_token"]

    logout_res = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_res.status_code == 200
    assert logout_res.json()["message"] == "Logged out successfully"
