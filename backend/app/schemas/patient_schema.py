"""
Patient Schemas
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PatientBase(BaseModel):
    patient_code: str
    age: int
    gender: str
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_history: Optional[str] = None

class PatientResponse(PatientBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
