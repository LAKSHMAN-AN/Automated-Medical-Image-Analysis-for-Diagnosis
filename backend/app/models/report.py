"""
Diagnostic Report Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from backend.app.database.session import Base

class DiagnosticReport(Base):
    __tablename__ = "diagnostic_reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prediction_id = Column(String, ForeignKey("predictions.id"), nullable=False, unique=True)
    nlp_extracted_entities = Column(Text, nullable=True)
    slm_clinical_summary = Column(Text, nullable=False)
    slm_patient_explanation = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="DRAFT", index=True)  # DRAFT, PENDING_REVIEW, APPROVED, REJECTED
    generated_at = Column(DateTime, default=datetime.utcnow)
