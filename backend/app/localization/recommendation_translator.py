"""
SmartCare AI - Module 4 Recommendation Translator
Translates recommendation payloads using controlled translation dictionaries while strictly
preserving numerical values, percentages, metrics, and IDs.
"""

from typing import Dict, Any, List
from .translations import TRANSLATIONS

class RecommendationTranslator:

    SUPPORTED_LANGUAGES = ["en", "ta", "hi", "te", "ml", "kn"]

    @classmethod
    def _tr(cls, text: Any, lang: str) -> Any:
        if not text or not isinstance(text, str) or lang == "en":
            return text
        if text in TRANSLATIONS and lang in TRANSLATIONS[text]:
            return TRANSLATIONS[text][lang]
        return text

    @classmethod
    def translate_plan(cls, plan_dict: Dict[str, Any], lang: str) -> Dict[str, Any]:
        """
        Translates plan payload to target language. Falls back to English if language
        is unsupported or missing. Never modifies numbers, percentages, or metrics.
        """
        if not lang or lang.lower() not in cls.SUPPORTED_LANGUAGES:
            lang = "en"
        else:
            lang = lang.lower()

        plan_dict["language"] = lang

        # Translate Top-Level Labels / Messages if present
        if "disclaimer" in plan_dict and plan_dict["disclaimer"]:
            plan_dict["disclaimer"] = cls._get_trans("disclaimer_text", lang, plan_dict["disclaimer"])

        if "follow_up_message" in plan_dict and plan_dict["follow_up_message"]:
            plan_dict["follow_up_message"] = cls._get_trans("high_risk_message", lang, plan_dict["follow_up_message"])

        if "clinical_followup_message" in plan_dict and plan_dict["clinical_followup_message"]:
            plan_dict["clinical_followup_message"] = cls._tr(plan_dict["clinical_followup_message"], lang)

        # 1. Translate Recommendations
        if "recommendations" in plan_dict and isinstance(plan_dict["recommendations"], list):
            for rec in plan_dict["recommendations"]:
                prio = rec.get("priority", "Medium")
                rec["priority_localized"] = cls._tr(prio, lang)
                if "category" in rec:
                    rec["category"] = cls._tr(rec["category"], lang)
                if "recommendation" in rec:
                    rec["recommendation"] = cls._tr(rec["recommendation"], lang)
                if "reason" in rec:
                    rec["reason"] = cls._tr(rec["reason"], lang)
                if "safety_note" in rec and rec["safety_note"]:
                    rec["safety_note"] = cls._tr(rec["safety_note"], lang)

        # 2. Translate Daily Food Plan
        if "daily_food_plan" in plan_dict and plan_dict["daily_food_plan"]:
            fp = plan_dict["daily_food_plan"]
            for meal_key in ["breakfast", "mid_morning", "lunch", "evening_snack", "dinner"]:
                if meal_key in fp and isinstance(fp[meal_key], dict):
                    m = fp[meal_key]
                    m["meal_localized"] = cls._tr(m.get("meal", meal_key), lang)
                    if "suggestion" in m:
                        m["suggestion"] = cls._tr(m["suggestion"], lang)
                    if "why" in m:
                        m["why"] = cls._tr(m["why"], lang)
                    if "safety_note" in m and m["safety_note"]:
                        m["safety_note"] = cls._tr(m["safety_note"], lang)
                    if "why_relevant" in m and m["why_relevant"]:
                        m["why_relevant"] = cls._tr(m["why_relevant"], lang)

        # 3. Translate Exercise Plan
        if "exercise_plan" in plan_dict and plan_dict["exercise_plan"]:
            ep = plan_dict["exercise_plan"]
            for s_key in ["morning", "afternoon", "evening"]:
                if s_key in ep and isinstance(ep[s_key], dict):
                    sess = ep[s_key]
                    if "time_of_day" in sess:
                        sess["time_of_day"] = cls._tr(sess["time_of_day"], lang)
                    if "activity" in sess:
                        sess["activity"] = cls._tr(sess["activity"], lang)
                    if "duration" in sess:
                        sess["duration"] = cls._tr(sess["duration"], lang)
                    if "frequency" in sess:
                        sess["frequency"] = cls._tr(sess["frequency"], lang)
                    if "intensity" in sess:
                        sess["intensity"] = cls._tr(sess["intensity"], lang)
                    if "safety_note" in sess and sess["safety_note"]:
                        sess["safety_note"] = cls._tr(sess["safety_note"], lang)
            if "general_safety_warning" in ep and ep["general_safety_warning"]:
                ep["general_safety_warning"] = cls._tr(ep["general_safety_warning"], lang)

        # 4. Translate Daily Habits
        if "daily_habits" in plan_dict and isinstance(plan_dict["daily_habits"], list):
            for h in plan_dict["daily_habits"]:
                if "title" in h:
                    h["title"] = cls._tr(h["title"], lang)
                if "description" in h:
                    h["description"] = cls._tr(h["description"], lang)
                if "category" in h:
                    h["category"] = cls._tr(h["category"], lang)

        # 5. Translate Herbal Wellness
        if "herbal_wellness" in plan_dict and isinstance(plan_dict["herbal_wellness"], list):
            for herb in plan_dict["herbal_wellness"]:
                if "name" in herb:
                    herb["name"] = cls._tr(herb["name"], lang)
                if "food_level_use" in herb:
                    herb["food_level_use"] = cls._tr(herb["food_level_use"], lang)
                if "purpose" in herb:
                    herb["purpose"] = cls._tr(herb["purpose"], lang)
                if "safety_warning" in herb:
                    herb["safety_warning"] = cls._tr(herb["safety_warning"], lang)

        # 6. Translate Monitoring Guidance
        if "monitoring_guidance" in plan_dict and isinstance(plan_dict["monitoring_guidance"], list):
            for mg in plan_dict["monitoring_guidance"]:
                if "parameter" in mg:
                    mg["parameter"] = cls._tr(mg["parameter"], lang)
                if "guidance" in mg:
                    mg["guidance"] = cls._tr(mg["guidance"], lang)
                if "frequency" in mg:
                    mg["frequency"] = cls._tr(mg["frequency"], lang)

        return plan_dict

    @classmethod
    def _get_trans(cls, key: str, lang: str, default_str: str) -> str:
        if key in TRANSLATIONS and lang in TRANSLATIONS[key]:
            return TRANSLATIONS[key][lang]
        return default_str
