"""
SmartCare AI - Module 6 Chat & Dashboard Schemas
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatMessageCreate(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatMessageResponse(BaseModel):
    id: Any
    user_id: int
    session_id: str
    role: str
    message: str
    intent: Optional[str] = None
    created_at: Any

    class Config:
        from_attributes = True

class ChatTurnResponse(BaseModel):
    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse
    intent: str
    safety_disclaimer: str

class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatMessageResponse]

class DashboardOverviewResponse(BaseModel):
    patient_id: int
    patient_name: str
    latest_assessment_date: Optional[str] = None
    latest_assessment_id: Optional[str] = None
    disease_risks: Dict[str, Dict[str, Any]]
    risk_trends: Optional[Dict[str, Any]] = None
    top_risk_factors: List[Dict[str, Any]] = []
    wellness_preview: Optional[Dict[str, Any]] = None
    open_alerts: List[Dict[str, Any]] = []
    total_assessments: int = 0
