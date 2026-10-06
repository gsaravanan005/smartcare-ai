"""
SmartCare AI - Module 4 Home Exercise Recommendation Engine
Generates safe, conservative home activity suggestions (walking, stretching, mobility breaks)
with explicit safety disclaimers for high-risk patients.
"""

from typing import Dict, Any, List

class ExerciseRulesEngine:

    HIGH_RISK_EXERCISE_SAFETY = (
        "Discuss an appropriate exercise plan with a qualified healthcare professional before starting a new exercise program."
    )

    @classmethod
    def generate_exercise_plan(
        cls,
        patient_data: Dict[str, Any],
        disease_risks: Dict[str, Dict[str, Any]],
        top_shap_factors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        # Check high risk trigger across any disease
        is_high_risk = any(
            info.get("probability", 0.0) >= 0.60 or info.get("risk_category") == "HIGH"
            for info in disease_risks.values()
        )

        phys_act = patient_data.get("phys_activity", 1)
        ap_hi = patient_data.get("ap_hi", 120)

        # Morning Session
        m_act = "Gentle morning warm-up and light joint mobility stretching."
        m_dur = "5–10 minutes"
        m_freq = "Daily"
        m_int = "Light / Low Intensity"

        # Afternoon Session
        if phys_act == 0:
            a_act = "Short indoor movement breaks or comfortable brisk walking around home/office."
            a_dur = "10–15 minutes"
            a_freq = "5 days / week"
            a_int = "Light to Moderate Intensity"
        else:
            a_act = "Continuous outdoor or indoor brisk walking at a steady, comfortable pace."
            a_dur = "20–30 minutes"
            a_freq = "5 days / week"
            a_int = "Moderate Intensity"

        # Evening Session
        e_act = "Relaxing evening posture stretching and slow deep-breathing mobility exercises."
        e_dur = "5–10 minutes"
        e_freq = "Daily"
        e_int = "Very Light / Restorative Intensity"

        safety_note = cls.HIGH_RISK_EXERCISE_SAFETY if (is_high_risk or ap_hi > 140) else (
            "Pace your activities gradually. Listen to your body and stop immediately if you experience dizziness, shortness of breath, or chest discomfort."
        )

        return {
            "morning": {
                "time_of_day": "Morning",
                "activity": m_act,
                "duration": m_dur,
                "frequency": m_freq,
                "intensity": m_int,
                "safety_note": safety_note
            },
            "afternoon": {
                "time_of_day": "Afternoon",
                "activity": a_act,
                "duration": a_dur,
                "frequency": a_freq,
                "intensity": a_int,
                "safety_note": safety_note
            },
            "evening": {
                "time_of_day": "Evening",
                "activity": e_act,
                "duration": e_dur,
                "frequency": e_freq,
                "intensity": e_int,
                "safety_note": safety_note
            },
            "general_safety_warning": cls.HIGH_RISK_EXERCISE_SAFETY if is_high_risk else None
        }
