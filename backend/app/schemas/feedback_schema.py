"""
Feedback Schemas
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FeedbackCreateRequest(BaseModel):
    prediction_id: str
    is_correct: bool
    corrected_class: Optional[str] = None
    comments: Optional[str] = None

# Alias for feedback controller import compatibility
FeedbackSubmitRequest = FeedbackCreateRequest

class FeedbackResponse(BaseModel):
    id: str
    prediction_id: str
    user_id: str
    is_correct: bool
    corrected_class: Optional[str] = None
    comments: Optional[str] = None
    submitted_at: datetime

    class Config:
        from_attributes = True
