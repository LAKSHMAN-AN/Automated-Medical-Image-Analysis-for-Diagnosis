"""
Analytics Schemas
"""

from typing import Dict, List, Any
from pydantic import BaseModel

class AnalyticsSummaryResponse(BaseModel):
    total_scans: int
    total_patients: int
    total_predictions: int
    total_approved_reports: int
    class_distribution: Dict[str, int]
    model_performance: Dict[str, Dict[str, float]]
    confusion_matrix: List[List[int]]
