"""
Feedback & Active Learning Service
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.models.feedback import Feedback
from backend.app.models.report import DiagnosticReport
from backend.app.schemas.feedback_schema import FeedbackSubmitRequest

class FeedbackService:
    def __init__(self, db: Session):
        self.db = db

    def submit_feedback(self, feedback_in: FeedbackSubmitRequest, doctor_id: str) -> Feedback:
        report = self.db.query(DiagnosticReport).filter(DiagnosticReport.id == feedback_in.report_id).first()
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnostic report not found")

        feedback = Feedback(
            report_id=feedback_in.report_id,
            doctor_id=doctor_id,
            doctor_action=feedback_in.doctor_action.upper(),
            corrected_class=feedback_in.corrected_class,
            doctor_notes=feedback_in.doctor_notes
        )
        self.db.add(feedback)

        # Update report status
        if feedback_in.doctor_action.upper() == "APPROVED":
            report.status = "APPROVED"
        elif feedback_in.doctor_action.upper() in ["MODIFIED", "REJECTED"]:
            report.status = "REJECTED"
        
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
