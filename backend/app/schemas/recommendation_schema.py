from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from .schemas import HealthRecordCreate

class RecommendationItem(BaseModel):
    id: Optional[int] = None
    category: str
    risk_factor: str
    source_feature: Optional[str] = None
    patient_value: Optional[str] = None
    shap_value: Optional[float] = None
    effect_direction: Optional[str] = None
    recommendation: str
    reason: str
    priority: str  # High, Medium, Low
    priority_localized: Optional[str] = None
    related_disease: str  # Diabetes, CVD, CKD, Multi-Disease
    safety_note: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecommendationGenerateRequest(BaseModel):
    patient_id: Optional[int] = None
    assessment_id: Optional[str] = None
    prediction_id: Optional[str] = None
    health_input: Optional[HealthRecordCreate] = None
    language: Optional[str] = "en"

class MealItem(BaseModel):
    meal: str
    meal_localized: Optional[str] = None
    suggestion: str
    why: str
    related_risk_factor: Optional[str] = None
    why_relevant: Optional[str] = None
    safety_note: Optional[str] = None

class DailyFoodPlan(BaseModel):
    breakfast: MealItem
    mid_morning: MealItem
    lunch: MealItem
    evening_snack: MealItem
    dinner: MealItem

class ExerciseSession(BaseModel):
    time_of_day: str
    activity: str
    duration: str
    frequency: str
    intensity: str
    safety_note: Optional[str] = None

class ExercisePlan(BaseModel):
    morning: ExerciseSession
    afternoon: ExerciseSession
    evening: ExerciseSession
    general_safety_warning: Optional[str] = None

class DailyHabitItem(BaseModel):
    title: str
    description: str
    category: str
    related_risk_factor: Optional[str] = None

class HerbalWellnessItem(BaseModel):
    name: str
    food_level_use: str
    purpose: str
    safety_warning: str
    related_risk_factor: Optional[str] = None

class MonitoringGuidanceItem(BaseModel):
    parameter: str
    guidance: str
    frequency: str
    related_risk_factor: Optional[str] = None

class RecommendationPlanResponse(BaseModel):
    patient_id: Optional[int] = None
    prediction_id: Optional[str] = None
    assessment_id: Optional[str] = None
    language: str = "en"
    risk_summary: Dict[str, Dict[str, Any]]
    modifiable_factors: List[Dict[str, Any]]
    recommendations: List[RecommendationItem]
    daily_food_plan: Optional[DailyFoodPlan] = None
    exercise_plan: Optional[ExercisePlan] = None
    daily_habits: List[DailyHabitItem] = []
    herbal_wellness: List[HerbalWellnessItem] = []
    monitoring_guidance: List[MonitoringGuidanceItem] = []
    clinical_followup_required: bool = False
    clinical_followup_message: Optional[str] = None
    disclaimer: str
    timestamp: datetime
