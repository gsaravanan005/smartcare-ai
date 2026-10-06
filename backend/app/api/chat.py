"""
SmartCare AI - Module 6 Wellness Chatbot & Dashboard Router
Exposes REST endpoints for patient AI wellness chatbot and aggregated dashboard overview telemetry.
Enforces authentication and strict patient data isolation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from ..core.database import get_db
from ..core.security import get_current_user, verify_patient_access
from ..models.models import User
from ..schemas.chat_schema import ChatMessageCreate, ChatTurnResponse, ChatMessageResponse, DashboardOverviewResponse
from ..services.chat_service import ChatService

router = APIRouter(tags=["Module 6 — Dashboard & Wellness Chatbot"])

@router.post("/chat", response_model=ChatTurnResponse)
def send_chat_message(
    chat_in: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sends a user message to the SmartCare AI Wellness Assistant.
    Retrieves contextual data from the authenticated patient's Modules 1-5 records.
    Generates a medically safe response and stores conversation history.
    """
    if not chat_in.message or not chat_in.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    turn = ChatService.process_chat_message(
        db=db,
        user=current_user,
        message_text=chat_in.message.strip(),
        session_id=chat_in.session_id or "default"
    )
    return turn

@router.get("/chat/history", response_model=List[ChatMessageResponse])
def get_chat_history(
    session_id: str = Query("default", description="Chat session identifier"),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves chat history for the authenticated user.
    """
    history = ChatService.get_chat_history(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        limit=limit
    )
    return history

@router.get("/dashboard/overview", response_model=DashboardOverviewResponse)
def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves aggregated patient dashboard telemetry combining Module 1-5 outputs.
    Enforces patient identity isolation.
    """
    overview = ChatService.get_dashboard_overview(db=db, user=current_user)
    return overview
