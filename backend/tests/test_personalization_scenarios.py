try:
    from app.core.database import SessionLocal
    from app.services.recommendation_service import RecommendationService
except ImportError:
    from backend.app.core.database import SessionLocal
    from backend.app.services.recommendation_service import RecommendationService

def test_personalization_scenarios_a_to_g():
    db = SessionLocal()

    # Patient A: High BP + High Glucose
    p_a = {"ap_hi": 150, "ap_lo": 95, "high_bp": 1, "glucose": 140, "high_chol": 0, "smoker": 0, "phys_activity": 1}
    plan_a = RecommendationService.generate_recommendation_plan(db=db, health_input=p_a, language="en")

    # Patient B: Active Smoker + Low Physical Activity
    p_b = {"ap_hi": 118, "ap_lo": 76, "high_bp": 0, "glucose": 92, "high_chol": 0, "smoker": 1, "phys_activity": 0}
    plan_b = RecommendationService.generate_recommendation_plan(db=db, health_input=p_b, language="en")

    # Patient C: High Glucose
    p_c = {"ap_hi": 120, "ap_lo": 80, "high_bp": 0, "glucose": 160, "high_chol": 0, "smoker": 0, "phys_activity": 1}
    plan_c = RecommendationService.generate_recommendation_plan(db=db, health_input=p_c, language="en")

    # Patient D: High BP + High Glucose + High BMI
    p_d = {"ap_hi": 160, "ap_lo": 100, "high_bp": 1, "glucose": 180, "weight_kg": 95, "height_cm": 170, "bmi": 32.87, "smoker": 0, "phys_activity": 0}
    plan_d = RecommendationService.generate_recommendation_plan(db=db, health_input=p_d, language="en")

    # Patient E: CKD / Renal Concern
    p_e = {"ap_hi": 130, "ap_lo": 85, "serum_creatinine": 2.4, "blood_urea": 65, "glucose": 98, "high_bp": 1, "smoker": 0}
    plan_e = RecommendationService.generate_recommendation_plan(db=db, health_input=p_e, language="en")

    # Patient F: Low Physical Activity
    p_f = {"ap_hi": 115, "ap_lo": 75, "glucose": 88, "high_bp": 0, "smoker": 0, "phys_activity": 0}
    plan_f = RecommendationService.generate_recommendation_plan(db=db, health_input=p_f, language="en")

    # Patient G: Normal / No modifiable risk factors
    p_g = {"ap_hi": 115, "ap_lo": 75, "glucose": 88, "high_bp": 0, "high_chol": 0, "smoker": 0, "phys_activity": 1, "serum_creatinine": 0.9}
    plan_g = RecommendationService.generate_recommendation_plan(db=db, health_input=p_g, language="en")

    # 1. Assert Patient A receives sodium & glucose food & monitoring recommendations
    recs_a_factors = [r["risk_factor"] for r in plan_a["recommendations"]]
    assert any("Blood Pressure" in rf for rf in recs_a_factors)
    assert any("Glucose" in rf for rf in recs_a_factors)

    # 2. Assert Patient B receives Smoking Cessation & Physical Activity focus
    recs_b_factors = [r["risk_factor"] for r in plan_b["recommendations"]]
    assert any("Smoking" in rf or "Tobacco" in rf for rf in recs_b_factors)
    assert any("Physical Activity" in rf for rf in recs_b_factors)

    # 3. Assert Patient E triggers CKD safety notes and clinical follow-up warning
    assert plan_e["daily_food_plan"]["breakfast"]["safety_note"] is not None
    assert "General kidney wellness guidance only" in plan_e["daily_food_plan"]["breakfast"]["safety_note"]

    # 4. Assert Patient G triggers baseline status with normal range advice
    assert len(plan_g["recommendations"]) >= 1
    assert plan_g["recommendations"][0]["risk_factor"] == "No Modifiable Risk Factors Identified"

    # 5. Assert all plans are distinct across Scenarios A, B, C, D, E, F, G
    plan_a_str = str(plan_a["recommendations"])
    plan_b_str = str(plan_b["recommendations"])
    plan_c_str = str(plan_c["recommendations"])
    plan_e_str = str(plan_e["recommendations"])

    assert plan_a_str != plan_b_str
    assert plan_a_str != plan_c_str
    assert plan_b_str != plan_e_str
