"""
Medical Image Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from backend.app.database.session import Base

class MedicalImage(Base):
    __tablename__ = "medical_images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    image_url = Column(String, nullable=False)
    modality = Column(String, nullable=False, default="CHEST_XRAY")  # CHEST_XRAY, BRAIN_MRI, LUNG_CT
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_hash = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
