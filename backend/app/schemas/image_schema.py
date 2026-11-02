"""
Medical Image Schemas
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ImageUploadResponse(BaseModel):
    id: str
    patient_id: str
    image_url: str
    modality: str
    width: Optional[int] = None
    height: Optional[int] = None
    file_hash: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
