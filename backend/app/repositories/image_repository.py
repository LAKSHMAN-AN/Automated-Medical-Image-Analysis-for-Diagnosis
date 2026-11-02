"""
Medical Image Repository
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.models.image import MedicalImage

class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, image_id: str) -> Optional[MedicalImage]:
        return self.db.query(MedicalImage).filter(MedicalImage.id == image_id).first()

    def get_by_patient(self, patient_id: str) -> List[MedicalImage]:
        return self.db.query(MedicalImage).filter(MedicalImage.patient_id == patient_id).all()

    def create(self, image: MedicalImage) -> MedicalImage:
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
