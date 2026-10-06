"""
SmartCare AI - Module 4 Good Daily Habits Engine
Generates practical lifestyle habit recommendations.
"""

from typing import Dict, Any, List

class HabitRulesEngine:

    @classmethod
    def generate_daily_habits(
        cls,
        patient_data: Dict[str, Any],
        disease_risks: Dict[str, Dict[str, Any]],
        top_shap_factors: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        habits = []

        # 1. Sleep Habit
        habits.append({
            "title": "Consistent Sleep Schedule",
            "description": "Maintain 7–8 hours of uninterrupted sleep nightly to support metabolic and cardiovascular recovery.",
            "category": "Rest & Recovery"
        })

        # 2. Movement Habit
        habits.append({
            "title": "Hourly Movement Breaks",
            "description": "Stand up and walk for 2–3 minutes for every hour of sitting to reduce vascular stiffness.",
            "category": "Physical Movement"
        })

        # 3. Hydration Habit
        habits.append({
            "title": "Adequate Water Intake",
            "description": "Drink sufficient water throughout the day to support kidney filtration and circulation.",
            "category": "Hydration"
        })

        # 4. Nutrition & Meal Timing
        habits.append({
            "title": "Mindful & Timely Meals",
            "description": "Eat meals at consistent daily times and avoid heavy late-night snacking.",
            "category": "Nutrition"
        })

        # 5. Tobacco Avoidance (if smoker or general)
        if patient_data.get("smoker", 0) == 1 or any(f.get("feature_name", "").lower() in ["smoker", "smoke"] for f in top_shap_factors):
            habits.append({
                "title": "Tobacco Cessation Focus",
                "description": "Avoid direct smoking and secondhand tobacco smoke exposure to protect arterial walls.",
                "category": "Behavioral Health"
            })

        # 6. Stress Management
        habits.append({
            "title": "Daily Stress Reduction",
            "description": "Practice 10 minutes of deep abdominal breathing or mindfulness daily to lower sympathetic stress.",
            "category": "Mental Wellness"
        })

        # 7. Regular Health Monitoring
        habits.append({
            "title": "Routine Self-Monitoring",
            "description": "Consistently log blood pressure, blood glucose, or weight as advised by your clinical team.",
            "category": "Monitoring"
        })

        return habits
