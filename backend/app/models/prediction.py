"""
Prediction Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey
from backend.app.database.session import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    image_id = Column(String, ForeignKey("medical_images.id"), nullable=False, index=True)
    model_name = Column(String, nullable=False)
    model_version = Column(String, nullable=False, default="1.0.0")
    predicted_class = Column(String, nullable=False, index=True)  # NORMAL, COVID, PNEUMONIA, TUBERCULOSIS
    confidence_score = Column(Float, nullable=False)
    class_probabilities_json = Column(Text, nullable=False)  # JSON string
    heatmap_url = Column(String, nullable=True)
    execution_time_ms = Column(Float, nullable=False)
    predicted_at = Column(DateTime, default=datetime.utcnow)
