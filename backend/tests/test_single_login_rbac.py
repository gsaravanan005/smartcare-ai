import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.mongo_db import mongo_manager
from app.core.security import hash_password

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_users():
    """Seed test database with known users for single login RBAC testing."""
    users_col = mongo_manager.get_collection("users")
    patients_col = mongo_manager.get_collection("patients")
    doctors_col = mongo_manager.get_collection("doctors")
    staff_col = mongo_manager.get_collection("staff")
    admins_col = mongo_manager.get_collection("admins")

    # Clean up test accounts
    test_emails = [
        "test_patient_single@smartcare.ai",
        "test_doctor_single@smartcare.ai",
        "test_staff_single@smartcare.ai",
        "test_admin_single@smartcare.ai",
        "new_doctor_created@smartcare.ai",
        "new_staff_created@smartcare.ai",
        "privilege_hacker@smartcare.ai",
        "privilege_hacker_2@smartcare.ai"
    ]
    users_col.delete_many({"email": {"$in": test_emails}})
    patients_col.delete_many({"email": {"$in": test_emails}})
    doctors_col.delete_many({"email": {"$in": test_emails}})
    staff_col.delete_many({"email": {"$in": test_emails}})
    admins_col.delete_many({"email": {"$in": test_emails}})

    pwd_hash = hash_password("password123")

    # Seed Patient (ID 801)
    users_col.insert_one({
        "user_id": 801,
        "username": "test_patient_single",
        "email": "test_patient_single@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Test Single Patient",
        "role": "patient",
        "status": "active"
    })
    patients_col.insert_one({
        "patient_id": 801,
        "user_id": 801,
        "email": "test_patient_single@smartcare.ai",
        "full_name": "Test Single Patient"
    })

    # Seed Doctor (ID 802)
    users_col.insert_one({
        "user_id": 802,
        "username": "test_doctor_single",
        "email": "test_doctor_single@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Dr. Single Test",
        "role": "doctor",
        "status": "active"
    })
    doctors_col.insert_one({
        "doctor_id": 802,
        "user_id": 802,
        "name": "Dr. Single Test",
        "email": "test_doctor_single@smartcare.ai",
        "verification_status": "approved"
    })

    # Seed Staff (ID 803)
    users_col.insert_one({
        "user_id": 803,
        "username": "test_staff_single",
        "email": "test_staff_single@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Staff Single Test",
        "role": "staff",
        "status": "active"
    })
    staff_col.insert_one({
        "staff_id": "STF_803",
        "user_id": 803,
        "name": "Staff Single Test",
        "email": "test_staff_single@smartcare.ai"
    })

    # Seed Admin (ID 804)
    users_col.insert_one({
        "user_id": 804,
        "username": "test_admin_single",
        "email": "test_admin_single@smartcare.ai",
        "password_hash": pwd_hash,
        "hashed_password": pwd_hash,
        "full_name": "Admin Single Test",
        "role": "admin",
        "status": "active"
    })

    yield

    users_col.delete_many({"email": {"$in": test_emails}})
    patients_col.delete_many({"email": {"$in": test_emails}})
    doctors_col.delete_many({"email": {"$in": test_emails}})
    staff_col.delete_many({"email": {"$in": test_emails}})
    admins_col.delete_many({"email": {"$in": test_emails}})

def helper_login(username, password="password123"):
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed for {username}: {res.text}"
    return res.json()["access_token"]

# --- 13 RBAC & Single Login Test Cases ---

def test_1_public_registration_forces_patient_role():
    """Verify public registration forcibly sets role = 'patient' even if payload specifies 'admin'."""
    res = client.post("/api/auth/register", json={
        "username": "privilege_hacker",
        "email": "privilege_hacker@smartcare.ai",
        "password": "password123",
        "full_name": "Hacker Attempt",
        "role": "admin" # Attacker trying to register as admin
    })
    assert res.status_code in [200, 201, 403]
    if res.status_code in [200, 201]:
        user_data = res.json()
        assert user_data["role"] == "patient", "Public registration MUST ignore caller role and assign 'patient'"

def test_2_public_registration_creates_patient_profile():
    """Verify patient profile record is created in MongoDB upon public registration."""
    res = client.post("/api/auth/register", json={
        "username": "privilege_hacker_2",
        "email": "privilege_hacker_2@smartcare.ai",
        "password": "password123",
        "full_name": "Hacker Attempt 2"
    })
    assert res.status_code in [200, 201]
    patients_col = mongo_manager.get_collection("patients")
    p_doc = patients_col.find_one({"email": "privilege_hacker_2@smartcare.ai"})
    assert p_doc is not None, "Patient document should exist in patients collection"

def test_3_single_login_patient_success():
    """Patient single login succeeds without specifying target_role."""
    res = client.post("/api/auth/login", json={
        "username": "test_patient_single@smartcare.ai",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "patient"
    assert "access_token" in data

def test_4_single_login_doctor_success():
    """Doctor single login succeeds and returns role = 'doctor' automatically."""
    res = client.post("/api/auth/login", json={
        "username": "test_doctor_single@smartcare.ai",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "doctor"

def test_5_single_login_staff_success():
    """Staff single login succeeds and returns role = 'staff' automatically."""
    res = client.post("/api/auth/login", json={
        "username": "test_staff_single@smartcare.ai",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "staff"

def test_6_single_login_admin_success():
    """Admin single login succeeds and returns role = 'admin' automatically."""
    res = client.post("/api/auth/login", json={
        "username": "test_admin_single@smartcare.ai",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "admin"

def test_7_invalid_credentials_returns_401():
    """Invalid password or non-existent user returns HTTP 401 Unauthorized."""
    res = client.post("/api/auth/login", json={
        "username": "test_patient_single@smartcare.ai",
        "password": "wrongpassword"
    })
    assert res.status_code == 401

def test_8_admin_can_create_doctor_account():
    """Admin provisions DOCTOR account via POST /api/admin/users."""
    admin_token = helper_login("test_admin_single@smartcare.ai")
    res = client.post(
        "/api/admin/users",
        json={
            "name": "Dr. Created Doctor",
            "email": "new_doctor_created@smartcare.ai",
            "phone": "+1-555-9988",
            "department": "Neurology",
            "designation": "Neurologist",
            "role": "DOCTOR",
            "password": "smartcare123"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "doctor"
    assert data["email"] == "new_doctor_created@smartcare.ai"

    doctors_col = mongo_manager.get_collection("doctors")
    doc = doctors_col.find_one({"email": "new_doctor_created@smartcare.ai"})
    assert doc is not None

def test_9_admin_can_create_staff_account():
    """Admin provisions STAFF account via POST /api/admin/users."""
    admin_token = helper_login("test_admin_single@smartcare.ai")
    res = client.post(
        "/api/admin/users",
        json={
            "name": "New Operations Staff",
            "email": "new_staff_created@smartcare.ai",
            "phone": "+1-555-8877",
            "staff_id": "STF_9901",
            "department": "Patient Services",
            "designation": "Staff Coordinator",
            "role": "STAFF",
            "password": "smartcare123"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] in ["staff", "doctor"]

    doctors_col = mongo_manager.get_collection("doctors")
    doc = doctors_col.find_one({"email": "new_staff_created@smartcare.ai"}) or mongo_manager.get_collection("staff").find_one({"email": "new_staff_created@smartcare.ai"})
    assert doc is not None

def test_10_non_admin_cannot_create_staff_account():
    """Patient calling POST /api/admin/users is denied with HTTP 403 Forbidden."""
    patient_token = helper_login("test_patient_single@smartcare.ai")
    res = client.post(
        "/api/admin/users",
        json={
            "name": "Illegal Staff",
            "email": "illegal@smartcare.ai",
            "role": "STAFF"
        },
        headers={"Authorization": f"Bearer {patient_token}"}
    )
    assert res.status_code == 403

def test_11_admin_cannot_create_invalid_role():
    """Admin attempting to create user with an invalid role string receives 400 Bad Request."""
    admin_token = helper_login("test_admin_single@smartcare.ai")
    res = client.post(
        "/api/admin/users",
        json={
            "name": "Invalid Role User",
            "email": "invalid_role@smartcare.ai",
            "role": "INVALID_SYSTEM_ROLE"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 400

def test_12_doctor_cannot_access_admin_endpoints():
    """Doctor attempting to access Admin endpoints gets HTTP 403 Forbidden."""
    doctor_token = helper_login("test_doctor_single@smartcare.ai")
    res = client.get("/api/admin/patients", headers={"Authorization": f"Bearer {doctor_token}"})
    assert res.status_code == 403

def test_13_patient_cannot_access_clinician_or_admin_endpoints():
    """Patient attempting to access Clinician or Admin endpoints gets HTTP 403 Forbidden."""
    patient_token = helper_login("test_patient_single@smartcare.ai")
    res_admin = client.get("/api/admin/doctors", headers={"Authorization": f"Bearer {patient_token}"})
    assert res_admin.status_code == 403
    res_clinician = client.get("/api/clinician/patients", headers={"Authorization": f"Bearer {patient_token}"})
    assert res_clinician.status_code == 403
