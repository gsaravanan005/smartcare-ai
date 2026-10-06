import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, apply_db_migrations, seed_default_users
from app.core.security import hash_password, create_access_token
from app.core.mongo_db import mongo_manager

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_environment():
    apply_db_migrations()
    db = SessionLocal()
    seed_default_users(db)
    db.close()

# 1. PATIENT PORTAL API TESTS
def test_patient_access_own_profile():
    patient_login = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123",
        "target_role": "patient"
    })
    token = patient_login.json()["access_token"]

    profile_res = client.get("/api/patients/profile", headers={"Authorization": f"Bearer {token}"})
    assert profile_res.status_code == 200
    assert profile_res.json()["user_id"] in [3, 100]

def test_patient_denied_admin_apis():
    patient_login = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123"
    })
    token = patient_login.json()["access_token"]

    admin_res = client.get("/api/admin/audit-logs", headers={"Authorization": f"Bearer {token}"})
    assert admin_res.status_code == 403

# 2. DOCTOR PORTAL API TESTS
def test_doctor_access_assigned_patient():
    doctor_login = client.post("/api/auth/login", json={
        "username": "doctor@smartcare.ai",
        "password": "doctor123",
        "target_role": "doctor"
    })
    token = doctor_login.json()["access_token"]

    # Clinician dashboard endpoint
    dash_res = client.get("/api/clinician/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert dash_res.status_code == 200

    # Clinician patient list
    plist_res = client.get("/api/clinician/patients", headers={"Authorization": f"Bearer {token}"})
    assert plist_res.status_code == 200

def test_doctor_denied_admin_apis():
    doctor_login = client.post("/api/auth/login", json={
        "username": "doctor@smartcare.ai",
        "password": "doctor123"
    })
    token = doctor_login.json()["access_token"]

    # Doctor trying to create another admin account
    create_admin_res = client.post("/api/admin/admins", headers={"Authorization": f"Bearer {token}"}, json={
        "username": "unauth_admin",
        "email": "unauth_admin@smartcare.ai",
        "password": "pwd"
    })
    assert create_admin_res.status_code == 403

# 3. ADMIN PORTAL API TESTS
def test_admin_access_analytics_and_audit():
    admin_login = client.post("/api/auth/login", json={
        "username": "admin@smartcare.ai",
        "password": "admin123",
        "target_role": "admin"
    })
    token = admin_login.json()["access_token"]

    analytics_res = client.get("/api/admin/analytics", headers={"Authorization": f"Bearer {token}"})
    assert analytics_res.status_code == 200
    assert "overview" in analytics_res.json()

    audit_res = client.get("/api/admin/audit-logs", headers={"Authorization": f"Bearer {token}"})
    assert audit_res.status_code == 200

def test_admin_doctor_verification():
    admin_login = client.post("/api/auth/login", json={
        "username": "admin@smartcare.ai",
        "password": "admin123"
    })
    token = admin_login.json()["access_token"]

    # Verify doctor endpoint
    verify_res = client.put("/api/admin/doctors/100/verify", headers={"Authorization": f"Bearer {token}"}, json={
        "verification_status": "approved"
    })
    assert verify_res.status_code in [200, 404]

# 4. NOTIFICATION APIS
def test_user_notifications():
    patient_login = client.post("/api/auth/login", json={
        "username": "patient@smartcare.ai",
        "password": "patient123"
    })
    token = patient_login.json()["access_token"]

    notif_res = client.get("/api/notifications", headers={"Authorization": f"Bearer {token}"})
    assert notif_res.status_code == 200
