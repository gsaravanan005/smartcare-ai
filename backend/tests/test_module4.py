import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import Base
from app.models.models import User, Patient, HealthRecord, PredictionRecord, RecommendationRecord
from app.rules.wellness_rules import WellnessRulesEngine
from app.rules.wellness_food_rules import WellnessFoodRulesEngine
from app.rules.exercise_rules import ExerciseRulesEngine
from app.rules.herbal_wellness_rules import HerbalWellnessRulesEngine
from app.services.recommendation_service import RecommendationService
from app.localization.recommendation_translator import RecommendationTranslator

# In-memory SQLite database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# 1. High BMI -> Weight management guidance
def test_1_high_bmi_guidance():
    patient_data = {"height_cm": 170, "weight_kg": 95, "bmi": 32.8}
    disease_risks = {"diabetes": {"probability": 0.40, "risk_category": "MODERATE"}}
    top_shap = [{"feature_name": "bmi", "patient_value": 32.8, "shap_value": 0.22, "abs_shap_value": 0.22, "direction": "RISK_INCREASING", "rank": 1, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert any(r["category"] == "Weight Management" for r in res["recommendations"])

# 2. High Blood Pressure -> BP wellness guidance
def test_2_high_bp_guidance():
    patient_data = {"high_bp": 1, "ap_hi": 148, "ap_lo": 92}
    disease_risks = {"cardio": {"probability": 0.50, "risk_category": "MODERATE"}}
    top_shap = [{"feature_name": "high_bp", "patient_value": 1.0, "shap_value": 0.18, "abs_shap_value": 0.18, "direction": "RISK_INCREASING", "rank": 1, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert any(r["category"] == "Cardiovascular Wellness" for r in res["recommendations"])

# 3. Low Physical Activity -> Activity guidance
def test_3_low_physical_activity_guidance():
    patient_data = {"phys_activity": 0}
    disease_risks = {"diabetes": {"probability": 0.25, "risk_category": "LOW"}}
    top_shap = [{"feature_name": "phys_activity", "patient_value": 0.0, "shap_value": 0.12, "abs_shap_value": 0.12, "direction": "RISK_INCREASING", "rank": 2, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert any(r["category"] == "Physical Activity" for r in res["recommendations"])

# 4. Smoking -> Cessation support guidance
def test_4_smoking_cessation_guidance():
    patient_data = {"smoker": 1}
    disease_risks = {"cardio": {"probability": 0.45, "risk_category": "MODERATE"}}
    top_shap = [{"feature_name": "smoker", "patient_value": 1.0, "shap_value": 0.20, "abs_shap_value": 0.20, "direction": "RISK_INCREASING", "rank": 1, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert any(r["category"] == "Behavioral Health" for r in res["recommendations"])

# 5. High Glucose -> Food/monitoring guidance
def test_5_high_glucose_guidance():
    patient_data = {"glucose": 140}
    disease_risks = {"diabetes": {"probability": 0.55, "risk_category": "MODERATE"}}
    top_shap = [{"feature_name": "glucose", "patient_value": 140, "shap_value": 0.25, "abs_shap_value": 0.25, "direction": "RISK_INCREASING", "rank": 1, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    food_res = WellnessFoodRulesEngine.generate_daily_food_plan(patient_data, disease_risks, top_shap)
    
    assert any(r["category"] == "Metabolic Health" for r in res["recommendations"])
    assert "fiber-rich" in food_res["breakfast"]["why"].lower() or "complex" in food_res["breakfast"]["why"].lower()

# 6. High Cholesterol -> Heart-healthy guidance
def test_6_high_cholesterol_guidance():
    patient_data = {"high_chol": 1, "cholesterol": 2}
    disease_risks = {"cardio": {"probability": 0.48, "risk_category": "MODERATE"}}
    top_shap = [{"feature_name": "high_chol", "patient_value": 1.0, "shap_value": 0.15, "abs_shap_value": 0.15, "direction": "RISK_INCREASING", "rank": 2, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert any(r["category"] == "Lipid Management" for r in res["recommendations"])

# 7. Renal Concern -> Renal safety warning
def test_7_renal_concern_warning():
    patient_data = {"serum_creatinine": 1.6}
    disease_risks = {"ckd": {"probability": 0.45, "risk_category": "MODERATE"}}
    top_shap = [{"feature_name": "serum_creatinine", "patient_value": 1.6, "shap_value": 0.30, "abs_shap_value": 0.30, "direction": "RISK_INCREASING", "rank": 1, "modifiable_status": "Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    food_res = WellnessFoodRulesEngine.generate_daily_food_plan(patient_data, disease_risks, top_shap)

    assert any(r["category"] == "Renal Health" for r in res["recommendations"])
    assert food_res["breakfast"]["safety_note"] is not None

# 8. Multiple Risk Factors -> Multi-category plan
def test_8_multiple_risk_factors():
    patient_data = {"height_cm": 170, "weight_kg": 95, "high_bp": 1, "smoker": 1, "phys_activity": 0}
    disease_risks = {"diabetes": {"probability": 0.55, "risk_category": "MODERATE"}, "cardio": {"probability": 0.58, "risk_category": "MODERATE"}}
    top_shap = [
        {"feature_name": "bmi", "patient_value": 32.8, "shap_value": 0.25, "abs_shap_value": 0.25, "direction": "RISK_INCREASING", "rank": 1, "modifiable_status": "Modifiable"},
        {"feature_name": "high_bp", "patient_value": 1.0, "shap_value": 0.20, "abs_shap_value": 0.20, "direction": "RISK_INCREASING", "rank": 2, "modifiable_status": "Modifiable"}
    ]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert len(res["recommendations"]) >= 2

# 9. No Modifiable Factors -> Safe fallback
def test_9_no_modifiable_factors_fallback():
    patient_data = {"age": 25, "sex": 0, "phys_activity": 1, "smoker": 0, "high_bp": 0}
    disease_risks = {"diabetes": {"probability": 0.10, "risk_category": "LOW"}}
    top_shap = [{"feature_name": "age", "patient_value": 25, "shap_value": 0.01, "abs_shap_value": 0.01, "direction": "RISK_DECREASING", "rank": 1, "modifiable_status": "Non-Modifiable"}]

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert res["recommendations"][0]["category"] in ["Assessment Status", "General Maintenance"]

# 10. High Risk Patient -> Clinical follow-up alert
def test_10_high_risk_clinical_alert():
    patient_data = {"high_bp": 1}
    disease_risks = {"cardio": {"probability": 0.75, "risk_category": "HIGH"}}
    top_shap = []

    res = WellnessRulesEngine.evaluate_wellness_rules(patient_data, disease_risks, top_shap)
    assert res["clinical_followup_required"] is True
    assert "Professional medical evaluation is recommended" in res["follow_up_message"]

# 11. Missing SHAP Result -> Graceful handling
def test_11_missing_shap_handling(db_session):
    plan = RecommendationService.generate_recommendation_plan(
        db=db_session,
        health_input={"high_bp": 1, "ap_hi": 140}
    )
    assert len(plan["recommendations"]) > 0

# 12. Missing Patient -> Graceful error / default execution
def test_12_missing_patient_graceful(db_session):
    plan = RecommendationService.generate_recommendation_plan(db=db_session, patient_id=99999)
    assert plan is not None
    assert "recommendations" in plan

# 13. Unsupported Language -> English fallback
def test_13_unsupported_language_fallback(db_session):
    plan = RecommendationService.generate_recommendation_plan(db=db_session, language="xx_unsupported")
    assert plan["language"] == "en"

# 14. Tamil Generation -> Tamil output
def test_14_tamil_generation(db_session):
    plan = RecommendationService.generate_recommendation_plan(db=db_session, language="ta")
    assert plan["language"] == "ta"

# 15. Hindi Generation -> Hindi output
def test_15_hindi_generation(db_session):
    plan = RecommendationService.generate_recommendation_plan(db=db_session, language="hi")
    assert plan["language"] == "hi"

# 16. Language change does not modify risk scores
def test_16_language_preserves_risk_scores(db_session):
    plan_en = RecommendationService.generate_recommendation_plan(db=db_session, language="en")
    plan_ta = RecommendationService.generate_recommendation_plan(db=db_session, language="ta")
    assert plan_en["risk_summary"]["diabetes"]["probability"] == plan_ta["risk_summary"]["diabetes"]["probability"]

# 17. Numerical measurements remain unchanged after localization
def test_17_numerical_measurements_unchanged(db_session):
    plan_en = RecommendationService.generate_recommendation_plan(db=db_session, health_input={"ap_hi": 145}, language="en")
    plan_hi = RecommendationService.generate_recommendation_plan(db=db_session, health_input={"ap_hi": 145}, language="hi")
    assert plan_en["risk_summary"]["cardio"]["probability"] == plan_hi["risk_summary"]["cardio"]["probability"]

# 18. Herbal supplement safety warning for renal-risk patient
def test_18_herbal_renal_warning():
    patient_data = {"serum_creatinine": 1.7}
    disease_risks = {"ckd": {"probability": 0.50, "risk_category": "MODERATE"}}
    top_shap = []

    herbal_res = HerbalWellnessRulesEngine.generate_herbal_wellness_guidance(patient_data, disease_risks, top_shap)
    assert any("Discuss herbal products with a qualified healthcare professional" in h["safety_warning"] for h in herbal_res)

# 19. No medication/dosage recommendation is generated
def test_19_no_medication_or_dosage_generated(db_session):
    plan = RecommendationService.generate_recommendation_plan(db=db_session, health_input={"high_bp": 1, "glucose": 180, "serum_creatinine": 2.0})
    for rec in plan["recommendations"]:
        text_lower = rec["recommendation"].lower()
        assert "mg" not in text_lower
        assert "tablet" not in text_lower
        assert "prescription" not in text_lower
        assert "dose" not in text_lower

# 20. End to end database persistence verification
def test_20_end_to_end_db_persistence(db_session):
    usr = User(username="pat20", email="pat20@smartcare.ai", hashed_password="pw", role="patient")
    db_session.add(usr)
    db_session.commit()

    patient = Patient(user_id=usr.id, age=48, sex=1, height_cm=175, weight_kg=88)
    db_session.add(patient)
    db_session.commit()

    plan = RecommendationService.generate_recommendation_plan(db=db_session, patient_id=patient.id, language="te")
    stored = db_session.query(RecommendationRecord).filter(RecommendationRecord.patient_id == patient.id).all()

    assert len(stored) > 0
    assert stored[0].language == "te"
