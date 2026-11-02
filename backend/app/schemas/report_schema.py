"""
Diagnostic Report Schemas
"""

from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ReportCreateRequest(BaseModel):
    prediction_id: str
    clinical_notes: Optional[str] = None

# Alias for SLM controller import compatibility
ReportGenerateRequest = ReportCreateRequest

class ReportResponse(BaseModel):
    id: str
    prediction_id: str
    technical_summary: str
    patient_summary: str
    key_findings: List[str]
    recommendations: List[str]
    model_used: str
    latency_ms: float
    created_at: datetime

    class Config:
        from_attributes = True
