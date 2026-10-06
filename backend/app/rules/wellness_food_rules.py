"""
SmartCare AI - Module 4 Daily Food Recommendation Engine
Generates personalized daily meal suggestions based on patient risk factors while enforcing
strict renal safety checks and conflict avoidance.
"""

from typing import Dict, Any, List

class WellnessFoodRulesEngine:

    @classmethod
    def generate_daily_food_plan(
        cls,
        patient_data: Dict[str, Any],
        disease_risks: Dict[str, Dict[str, Any]],
        top_shap_factors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        # Check risk flags
        bmi = patient_data.get("bmi") or (
            patient_data.get("weight_kg", 70) / ((patient_data.get("height_cm", 170) / 100) ** 2)
            if patient_data.get("weight_kg") and patient_data.get("height_cm") else 24.0
        )
        high_bmi = (bmi >= 25.0) or any(f.get("feature_name", "").lower() in ["bmi"] for f in top_shap_factors)
        high_glucose = (patient_data.get("glucose", 100) > 100) or any(f.get("feature_name", "").lower() in ["glucose", "bgr"] for f in top_shap_factors)
        high_bp = (patient_data.get("high_bp", 0) == 1 or patient_data.get("ap_hi", 120) > 130) or any(f.get("feature_name", "").lower() in ["high_bp", "ap_hi", "ap_lo"] for f in top_shap_factors)
        high_chol = (patient_data.get("high_chol", 0) == 1 or patient_data.get("cholesterol", 1) > 1) or any(f.get("feature_name", "").lower() in ["high_chol", "cholesterol"] for f in top_shap_factors)
        
        ckd_prob = disease_risks.get("ckd", {}).get("probability", 0.0)
        ckd_cat = disease_risks.get("ckd", {}).get("risk_category", "LOW")
        sc_val = patient_data.get("serum_creatinine", 1.0)
        high_ckd_risk = (ckd_prob >= 0.40 or ckd_cat == "HIGH" or sc_val > 1.2)

        # 1. Breakfast
        if high_glucose:
            b_sug = "Steel-cut oatmeal or whole-grain porridge topped with ground flaxseed and a handful of berries."
            b_why = "Provides complex carbohydrates and high soluble fiber to encourage steady glycemic response."
        elif high_bmi:
            b_sug = "Poached or boiled eggs with steamed vegetables and a slice of whole-grain toast."
            b_why = "High protein and nutrient density support morning satiety and weight management."
        elif high_bp:
            b_sug = "Unsalted rolled oats prepared with water or low-fat milk, topped with sliced banana."
            b_why = "Potassium-rich, low-sodium breakfast supporting healthy arterial pressure."
        else:
            b_sug = "Whole-grain cereal or oatmeal with fresh fruit and unsweetened plant or low-fat milk."
            b_why = "Balanced fiber and protein for baseline morning energy."

        # 2. Mid-Morning
        if high_glucose or high_bmi:
            mm_sug = "Handful of raw unsalted almonds or walnuts with cucumber slices."
            mm_why = "Healthy fats and low-glycemic crunch stabilize hunger without blood sugar spikes."
        elif high_chol:
            mm_sug = "Fresh apple or pear with skin on."
            mm_why = "Pectin soluble fiber helps support healthy blood lipid levels."
        else:
            mm_sug = "A seasonal fresh fruit (e.g., apple, orange, or berries)."
            mm_why = "Provides natural antioxidants and essential vitamins."

        # 3. Lunch
        if high_bp and high_chol:
            l_sug = "Steamed or grilled lean protein (chicken breast, fish, or lentils) with a large leafy green salad dressed in olive oil and lemon."
            l_why = "Low sodium and rich in unsaturated fatty acids for heart-healthy lipid and BP support."
        elif high_glucose:
            l_sug = "Quinoa or brown rice bowl with mixed grilled vegetables and chickpeas or baked tofu."
            l_why = "High fiber and complex plant protein slow carbohydrate absorption."
        elif high_bmi:
            l_sug = "Clear vegetable soup paired with a colorful salad and grilled protein."
            l_why = "High volume, nutrient-rich meals promote fullness with controlled calorie density."
        else:
            l_sug = "Balanced plate: half non-starchy vegetables, one-quarter lean protein, one-quarter whole grains."
            l_why = "Provides optimal macronutrient balance for daily energy."

        # 4. Evening Snack
        if high_bp:
            ev_sug = "Homemade unsalted roasted chickpeas or fresh carrot sticks with hummus."
            ev_why = "Low-sodium, fiber-rich snack alternative to processed salty chips."
        elif high_glucose:
            ev_sug = "Greek yogurt (plain, unsweetened) with a pinch of cinnamon."
            ev_why = "Protein and protein-bound calcium with zero added sugars."
        else:
            ev_sug = "Green tea or herbal tea with a small portion of roasted makhana (lotus seeds) or seeds."
            ev_why = "Light, comforting refreshment before dinner."

        # 5. Dinner
        if high_glucose or high_bmi:
            d_sug = "Baked fish or steamed tofu with roasted broccoli, cauliflower, and a small serving of sweet potato."
            d_sug_why = "Light evening meal with lean protein and non-starchy vegetables prevents overnight blood sugar elevation."
        elif high_bp:
            d_sug = "Home-cooked vegetable stir-fry with herbs, garlic, ginger, and brown rice, prepared without added salt."
            d_sug_why = "Flavorful salt-free seasoning using culinary herbs and spices."
        else:
            d_sug = "Vegetable stew or grilled protein with steamed green vegetables."
            d_sug_why = "Easy-to-digest evening meal supporting restful sleep."

        # Renal Safety Note Check for ALL meals
        renal_safety = None
        if high_ckd_risk:
            renal_safety = (
                "General kidney wellness guidance only. Do NOT start restrictive renal diets, "
                "protein restrictions, or potassium/phosphorus adjustments without clinical dietitian oversight."
            )

        return {
            "breakfast": {"meal": "Breakfast", "suggestion": b_sug, "why": b_why, "safety_note": renal_safety},
            "mid_morning": {"meal": "Mid-Morning", "suggestion": mm_sug, "why": mm_why, "safety_note": renal_safety},
            "lunch": {"meal": "Lunch", "suggestion": l_sug, "why": l_why, "safety_note": renal_safety},
            "evening_snack": {"meal": "Evening Snack", "suggestion": ev_sug, "why": ev_why, "safety_note": renal_safety},
            "dinner": {"meal": "Dinner", "suggestion": d_sug, "why": d_sug_why, "safety_note": renal_safety}
        }
