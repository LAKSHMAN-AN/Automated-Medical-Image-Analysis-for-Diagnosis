"""
Patient Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime
from backend.app.database.session import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_code = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # MALE, FEMALE, OTHER
    medical_history = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
