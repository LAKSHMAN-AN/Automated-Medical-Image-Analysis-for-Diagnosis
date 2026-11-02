"""
Prediction Repository
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.models.prediction import Prediction

class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, prediction_id: str) -> Optional[Prediction]:
        return self.db.query(Prediction).filter(Prediction.id == prediction_id).first()

    def get_by_image_id(self, image_id: str) -> List[Prediction]:
        return self.db.query(Prediction).filter(Prediction.image_id == image_id).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Prediction]:
        return self.db.query(Prediction).offset(skip).limit(limit).all()

    def count_total(self) -> int:
        return self.db.query(Prediction).count()

    def create(self, prediction: Prediction) -> Prediction:
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction
