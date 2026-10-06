"""
SmartCare AI - Module 4 Daily Plan Service
Orchestrates food plans, home exercise plans, good daily habits, and herbal wellness guidance.
"""

from typing import Dict, Any, List
from ..rules.wellness_food_rules import WellnessFoodRulesEngine
from ..rules.exercise_rules import ExerciseRulesEngine
from ..rules.habit_rules import HabitRulesEngine
from ..rules.herbal_wellness_rules import HerbalWellnessRulesEngine

class DailyPlanService:

    @classmethod
    def generate_all_daily_plans(
        cls,
        patient_data: Dict[str, Any],
        disease_risks: Dict[str, Dict[str, Any]],
        top_shap_factors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Aggregates food, exercise, habit, and herbal wellness plans dynamically.
        """
        food_plan = WellnessFoodRulesEngine.generate_daily_food_plan(patient_data, disease_risks, top_shap_factors)
        exercise_plan = ExerciseRulesEngine.generate_exercise_plan(patient_data, disease_risks, top_shap_factors)
        daily_habits = HabitRulesEngine.generate_daily_habits(patient_data, disease_risks, top_shap_factors)
        herbal_wellness = HerbalWellnessRulesEngine.generate_herbal_wellness_guidance(patient_data, disease_risks, top_shap_factors)

        return {
            "daily_food_plan": food_plan,
            "exercise_plan": exercise_plan,
            "daily_habits": daily_habits,
            "herbal_wellness": herbal_wellness
        }
