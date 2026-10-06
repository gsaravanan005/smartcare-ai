import pytest
from fastapi.testclient import TestClient
try:
    from app.main import app
    from app.core.database import SessionLocal
    from app.core.security import hash_password
    from app.models.models import User, Patient, PredictionRecord
except ImportError:
    from backend.app.main import app
    from backend.app.core.database import SessionLocal
    from backend.app.core.security import hash_password
    from backend.app.models.models import User, Patient, PredictionRecord

client = TestClient(app)

def test_patient_isolation_unauthorized_access():
    db = SessionLocal()
    
    # 1. Create Patient 1 and Patient 2
    u1 = db.query(User).filter(User.username == "test_isolation_p1").first()
    if not u1:
        u1 = User(username="test_isolation_p1", email="p1@isolation.com", hashed_password=hash_password("pwd"), role="patient")
        db.add(u1)
        db.commit()
        db.refresh(u1)
        p1 = Patient(user_id=u1.id)
        db.add(p1)
        db.commit()
    else:
        u1.hashed_password = hash_password("pwd")
        db.commit()
        p1 = u1.patient_profile

    u2 = db.query(User).filter(User.username == "test_isolation_p2").first()
    if not u2:
        u2 = User(username="test_isolation_p2", email="p2@isolation.com", hashed_password=hash_password("pwd"), role="patient")
        db.add(u2)
        db.commit()
        db.refresh(u2)
        p2 = Patient(user_id=u2.id)
        db.add(p2)
        db.commit()
    else:
        u2.hashed_password = hash_password("pwd")
        db.commit()
        p2 = u2.patient_profile

    # 2. Login as Patient 1
    login_res = client.post("/api/auth/login", json={"username": "test_isolation_p1", "password": "pwd"})
    assert login_res.status_code == 200
    token1 = login_res.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # 3. Patient 1 attempts to query Patient 2's prediction records
    res_pred = client.get(f"/api/predictions/patient/{p2.id}", headers=headers1)
    assert res_pred.status_code == 403
    assert "Access denied" in res_pred.json()["detail"]

    # 4. Patient 1 attempts to query Patient 2's recommendation plan
    res_rec = client.get(f"/api/recommendations/patient/{p2.id}", headers=headers1)
    assert res_rec.status_code == 403
    assert "Access denied" in res_rec.json()["detail"]

    # 5. Patient 1 attempts to query own records (Should succeed)
    res_own = client.get(f"/api/predictions/patient/{p1.id}", headers=headers1)
    assert res_own.status_code == 200
