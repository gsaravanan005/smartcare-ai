from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import inspect, text

def seed_default_users(db_session):
    from ..models.models import User, Patient
    import hashlib

    def hash_pwd(pwd: str) -> str:
        salt = "smartcare_salt_2026"
        return hashlib.pbkdf2_hmac("sha256", pwd.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

    default_users = [
        {"username": "admin", "email": "admin@smartcare.ai", "password": "admin123", "role": "admin", "status": "active", "full_name": "Dr. System Administrator"},
        {"username": "doctor", "email": "doctor@smartcare.ai", "password": "doctor123", "role": "doctor", "status": "active", "full_name": "Dr. Sarah Jenkins"},
        {"username": "patient", "email": "patient@smartcare.ai", "password": "patient123", "role": "patient", "status": "active", "full_name": "John Doe"},
        {"username": "pending_doctor", "email": "pending_doctor@smartcare.ai", "password": "doctor123", "role": "doctor", "status": "pending", "full_name": "Dr. Alex Rivera"},
        {"username": "inactive_patient", "email": "inactive_patient@smartcare.ai", "password": "patient123", "role": "patient", "status": "inactive", "full_name": "Jane Smith"}
    ]

    for u_data in default_users:
        existing = db_session.query(User).filter((User.username == u_data["username"]) | (User.email == u_data["email"])).first()
        if not existing:
            u = User(
                username=u_data["username"],
                email=u_data["email"],
                hashed_password=hash_pwd(u_data["password"]),
                role=u_data["role"],
                status=u_data.get("status", "active"),
                full_name=u_data["full_name"]
            )
            db_session.add(u)
            db_session.commit()
            db_session.refresh(u)

            if u.role == "patient":
                p = Patient(user_id=u.id, age=45.0, sex=1, height_cm=175.0, weight_kg=78.0, bmi=25.47)
                db_session.add(p)
                db_session.commit()

def apply_db_migrations(target_engine=None):
    if target_engine is None:
        target_engine = engine
    
    try:
        inspector = inspect(target_engine)
        if "recommendations" in inspector.get_table_names():
            existing_cols = {c["name"] for c in inspector.get_columns("recommendations")}
            needed_cols = [
                ("language", "TEXT DEFAULT 'en'"),
                ("daily_food_plan", "JSON"),
                ("exercise_plan", "JSON"),
                ("daily_habits", "JSON"),
                ("herbal_wellness", "JSON"),
                ("monitoring_guidance", "JSON"),
                ("clinical_followup_required", "BOOLEAN DEFAULT 0"),
                ("clinical_followup_message", "TEXT"),
            ]
            
            with target_engine.begin() as conn:
                for col_name, col_type in needed_cols:
                    if col_name not in existing_cols:
                        conn.execute(text(f"ALTER TABLE recommendations ADD COLUMN {col_name} {col_type};"))

        if "users" in inspector.get_table_names():
            existing_user_cols = {c["name"] for c in inspector.get_columns("users")}
            needed_user_cols = [
                ("status", "TEXT DEFAULT 'active'"),
                ("updated_at", "DATETIME"),
                ("last_login", "DATETIME")
            ]
            with target_engine.begin() as conn:
                for col_name, col_type in needed_user_cols:
                    if col_name not in existing_user_cols:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};"))
    except Exception as err:
        print(f"[DB Migration Warning] Exception during database migration: {err}")

    # Seed default accounts
    try:
        db = SessionLocal()
        seed_default_users(db)
        db.close()
    except Exception as e:
        print(f"[DB Seed Warning] Exception during user seeding: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
