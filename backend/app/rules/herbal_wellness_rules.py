"""
SmartCare AI - Module 4 Home Herbal & Natural Wellness Engine
Provides food-level culinary herb and spice guidance while strictly enforcing safety guardrails
against concentrated supplements, unproven cure claims, or unsafe renal usage.
"""

from typing import Dict, Any, List

class HerbalWellnessRulesEngine:

    GENERAL_HERBAL_NOTICE = (
        "Herbal and natural wellness suggestions are culinary food-level culinary options only and do not replace medical treatment. "
        "Do NOT start concentrated herbal extracts, capsules, or supplements without consulting a qualified healthcare professional."
    )

    RENAL_HERBAL_SAFETY_WARNING = (
        "Food-level herbs and spices may be used for meal variety, but herbal supplements or concentrated preparations "
        "should not be started based on this AI recommendation. Discuss herbal products with a qualified healthcare professional first."
    )

    @classmethod
    def generate_herbal_wellness_guidance(
        cls,
        patient_data: Dict[str, Any],
        disease_risks: Dict[str, Dict[str, Any]],
        top_shap_factors: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        ckd_prob = disease_risks.get("ckd", {}).get("probability", 0.0)
        ckd_cat = disease_risks.get("ckd", {}).get("risk_category", "LOW")
        sc_val = patient_data.get("serum_creatinine", 1.0)
        high_ckd_risk = (ckd_prob >= 0.40 or ckd_cat == "HIGH" or sc_val > 1.2)

        safety_msg = cls.RENAL_HERBAL_SAFETY_WARNING if high_ckd_risk else cls.GENERAL_HERBAL_NOTICE

        herbal_items = [
            {
                "name": "Culinary Turmeric (Curcuma longa)",
                "food_level_use": "Add a small pinch (1/4 tsp) to soups, cooked lentils, or warm food preparation.",
                "purpose": "Provides natural antioxidant phytonutrients for general culinary flavor and meal variety.",
                "safety_warning": safety_msg
            },
            {
                "name": "Fresh Ginger (Zingiber officinale)",
                "food_level_use": "Grate fresh ginger into warm water or culinary dishes.",
                "purpose": "Aids digestion and adds natural flavor without added salt or sodium.",
                "safety_warning": safety_msg
            },
            {
                "name": "Ceylon Cinnamon (Cinnamomum verum)",
                "food_level_use": "Sprinkle a pinch over morning oatmeal or unsweetened yogurt.",
                "purpose": "Provides natural aromatic sweetness to meals without refined sugar.",
                "safety_warning": safety_msg
            },
            {
                "name": "Fresh Mint & Holy Basil Leaves",
                "food_level_use": "Steep fresh mint leaves in warm water as a light home beverage.",
                "purpose": "Comforting, soothing non-caffeinated herbal drink option.",
                "safety_warning": safety_msg
            }
        ]

        return herbal_items
