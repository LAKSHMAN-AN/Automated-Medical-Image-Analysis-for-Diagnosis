"""
SLM Controller Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.image import MedicalImage
from backend.app.models.patient import Patient
from backend.app.models.report import DiagnosticReport
from backend.app.schemas.report_schema import ReportGenerateRequest, ReportResponse
from backend.app.services.slm_service import SLMService
from backend.app.dependencies.auth_deps import require_doctor_or_radiologist

router = APIRouter(prefix="/slm", tags=["Small Language Model (SLM)"])
slm_service = SLMService()

@router.post("/generate-report", response_model=ReportResponse, dependencies=[Depends(require_doctor_or_radiologist)])
def generate_slm_report(req: ReportGenerateRequest, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == req.prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")

    image = db.query(MedicalImage).filter(MedicalImage.id == prediction.image_id).first()
    patient = db.query(Patient).filter(Patient.id == image.patient_id).first() if image else None

    age = patient.age if patient else 45
    gender = patient.gender if patient else "MALE"

    clinical_summary = slm_service.generate_clinical_summary(
        predicted_class=prediction.predicted_class,
        confidence=prediction.confidence_score,
        patient_age=age,
        patient_gender=gender
    )

    patient_explanation = slm_service.generate_patient_explanation(prediction.predicted_class)

    report = db.query(DiagnosticReport).filter(DiagnosticReport.prediction_id == req.prediction_id).first()
    if not report:
        report = DiagnosticReport(
            prediction_id=req.prediction_id,
            slm_clinical_summary=clinical_summary,
            slm_patient_explanation=patient_explanation,
            status="DRAFT"
        )
        db.add(report)
        db.commit()
        db.refresh(report)

    return report
