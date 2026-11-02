"""
Patient Controller Endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.patient_schema import PatientCreate, PatientUpdate, PatientResponse
from backend.app.services.patient_service import PatientService
from backend.app.dependencies.auth_deps import require_doctor_or_radiologist

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_doctor_or_radiologist)])
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.create_patient(patient_in)

@router.get("/", response_model=List[PatientResponse], dependencies=[Depends(require_doctor_or_radiologist)])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.get_all_patients(skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=PatientResponse, dependencies=[Depends(require_doctor_or_radiologist)])
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.get_patient(patient_id)

@router.put("/{patient_id}", response_model=PatientResponse, dependencies=[Depends(require_doctor_or_radiologist)])
def update_patient(patient_id: str, update_in: PatientUpdate, db: Session = Depends(get_db)):
    service = PatientService(db)
    return service.update_patient(patient_id, update_in)
