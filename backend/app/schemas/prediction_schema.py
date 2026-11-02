"""
Prediction Schemas
"""

from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class PredictionRequest(BaseModel):
    image_id: str
    model_type: str = "RESNET50"
    include_gradcam: bool = True

class PredictionResponse(BaseModel):
    id: str
    image_id: str
    model_name: str
    model_version: str
    predicted_class: str
    confidence_score: float
    class_probabilities: Dict[str, float]
    heatmap_url: Optional[str] = None
    execution_time_ms: float
    predicted_at: datetime

    class Config:
        from_attributes = True
