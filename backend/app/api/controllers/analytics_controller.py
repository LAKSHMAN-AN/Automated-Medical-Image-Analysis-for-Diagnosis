"""
Analytics Controller Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.schemas.analytics_schema import AnalyticsSummaryResponse
from backend.app.services.analytics_service import AnalyticsService
from backend.app.dependencies.auth_deps import require_doctor_or_radiologist

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary", response_model=AnalyticsSummaryResponse, dependencies=[Depends(require_doctor_or_radiologist)])
def get_analytics_summary(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_system_summary()
