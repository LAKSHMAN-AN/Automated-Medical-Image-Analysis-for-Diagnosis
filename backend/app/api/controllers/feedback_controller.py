"""
Doctor Feedback Controller Endpoints
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.schemas.feedback_schema import FeedbackSubmitRequest, FeedbackResponse
from backend.app.services.feedback_service import FeedbackService
from backend.app.dependencies.auth_deps import get_current_user, require_doctor_or_radiologist

router = APIRouter(prefix="/feedback", tags=["Doctor Feedback"])

@router.post("/submit", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_doctor_or_radiologist)])
def submit_feedback(req: FeedbackSubmitRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = FeedbackService(db)
    return service.submit_feedback(req, doctor_id=current_user.id)
