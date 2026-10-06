try:
    from app.core.database import SessionLocal
    from app.services.recommendation_service import RecommendationService
except ImportError:
    from backend.app.core.database import SessionLocal
    from backend.app.services.recommendation_service import RecommendationService

def test_multilingual_numerical_integrity():
    db = SessionLocal()

    patient_input = {
        "ap_hi": 142,
        "ap_lo": 88,
        "glucose": 160,
        "high_bp": 1,
        "high_chol": 1,
        "smoker": 0,
        "phys_activity": 1
    }

    languages = ["en", "ta", "hi", "te", "ml", "kn", "unsupported_xyz"]
    plans = {}

    for lang in languages:
        plans[lang] = RecommendationService.generate_recommendation_plan(
            db=db,
            patient_id=1,
            health_input=patient_input,
            language=lang
        )

    base_en = plans["en"]

    for lang in ["ta", "hi", "te", "ml", "kn"]:
        p_lang = plans[lang]
        
        # 1. Assert Risk percentages remain numerically identical
        for dis in ["diabetes", "cardio", "ckd"]:
            en_pct = base_en["risk_summary"][dis]["risk_percentage"]
            lang_pct = p_lang["risk_summary"][dis]["risk_percentage"]
            assert en_pct == lang_pct, f"Risk percentage for {dis} mismatched in {lang}"

        # 2. Assert SHAP values remain numerically identical
        if base_en["modifiable_factors"]:
            en_shap = base_en["modifiable_factors"][0]["abs_shap_value"]
            lang_shap = p_lang["modifiable_factors"][0]["abs_shap_value"]
            assert en_shap == lang_shap, f"SHAP value mismatched in {lang}"

        # 3. Assert Patient ID & Prediction ID remain identical
        assert base_en["patient_id"] == p_lang["patient_id"]
        assert base_en["prediction_id"] == p_lang["prediction_id"]

    # 4. Assert unsupported language falls back safely to English
    p_fallback = plans["unsupported_xyz"]
    assert p_fallback["language"] == "en"
