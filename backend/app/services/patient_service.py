"""
Patient Management Service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.models.patient import Patient
from backend.app.repositories.patient_repository import PatientRepository
from backend.app.schemas.patient_schema import PatientCreate, PatientUpdate

class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.patient_repo = PatientRepository(db)

    def create_patient(self, patient_in: PatientCreate) -> Patient:
        existing = self.patient_repo.get_by_code(patient_in.patient_code)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient code already exists")
        
        patient = Patient(
            patient_code=patient_in.patient_code,
            age=patient_in.age,
            gender=patient_in.gender.upper(),
            medical_history=patient_in.medical_history
        )
        return self.patient_repo.create(patient)

    def get_patient(self, patient_id: str) -> Patient:
        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return patient

    def get_all_patients(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        return self.patient_repo.get_all(skip=skip, limit=limit)

    def update_patient(self, patient_id: str, update_in: PatientUpdate) -> Patient:
        patient = self.get_patient(patient_id)
        if update_in.age is not None:
            patient.age = update_in.age
        if update_in.gender is not None:
            patient.gender = update_in.gender.upper()
        if update_in.medical_history is not None:
            patient.medical_history = update_in.medical_history
        return self.patient_repo.update(patient)
