"""
Doctor Feedback Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from backend.app.database.session import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = Column(String, ForeignKey("diagnostic_reports.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("users.id"), nullable=False)
    doctor_action = Column(String, nullable=False)  # APPROVED, MODIFIED, REJECTED
    corrected_class = Column(String, nullable=True)
    doctor_notes = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
