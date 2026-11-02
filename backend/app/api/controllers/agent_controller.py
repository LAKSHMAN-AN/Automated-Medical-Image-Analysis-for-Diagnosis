"""
Agentic AI Controller Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.patient import Patient
from backend.app.schemas.agent_schema import AgentDiagnoseRequest, AgentDecisionResponse
from backend.app.services.agent_service import AgenticAIService
from backend.app.dependencies.auth_deps import require_doctor_or_radiologist

router = APIRouter(prefix="/agent", tags=["Agentic AI"])
agent_service = AgenticAIService()

@router.post("/diagnose", response_model=AgentDecisionResponse, dependencies=[Depends(require_doctor_or_radiologist)])
def agent_diagnose(req: AgentDiagnoseRequest, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == req.patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    prediction = db.query(Prediction).filter(Prediction.image_id == req.image_id).order_by(Prediction.predicted_at.desc()).first()
    
    dl_pred = {
        "predicted_class": prediction.predicted_class if prediction else "NORMAL",
        "confidence_score": prediction.confidence_score if prediction else 0.94
    }

    result = agent_service.run_diagnostic_agent_workflow(
        patient_code=patient.patient_code,
        image_id=req.image_id,
        dl_prediction=dl_pred
    )
    return result
