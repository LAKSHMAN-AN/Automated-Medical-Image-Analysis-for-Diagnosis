"""
Agentic AI Schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class AgentDiagnoseRequest(BaseModel):
    patient_id: str
    image_id: str

class AgentDecisionResponse(BaseModel):
    agent_id: str
    primary_diagnosis: str
    confidence_score: float
    differential_diagnoses: List[Dict[str, Any]]
    reasoning_summary: str
    recommended_actions: List[str]
    requires_hitl_approval: bool
