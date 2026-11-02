"""
Prediction Controller Endpoints
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.prediction import Prediction
from backend.app.repositories.image_repository import ImageRepository
from backend.app.repositories.prediction_repository import PredictionRepository
from backend.app.schemas.prediction_schema import PredictionRequest, PredictionResponse
from backend.app.services.dl_service import DeepLearningService
from backend.app.dependencies.auth_deps import require_doctor_or_radiologist

router = APIRouter(prefix="/predictions", tags=["Predictions"])
dl_service = DeepLearningService()

@router.post("/analyze", response_model=PredictionResponse, dependencies=[Depends(require_doctor_or_radiologist)])
def analyze_image(req: PredictionRequest, db: Session = Depends(get_db)):
    image_repo = ImageRepository(db)
    image = image_repo.get_by_id(req.image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical image not found")

    result = dl_service.predict(image.image_url, model_type=req.model_type)

    prediction = Prediction(
        image_id=req.image_id,
        model_name=result["model_name"],
        model_version=result["model_version"],
        predicted_class=result["predicted_class"],
        confidence_score=result["confidence_score"],
        class_probabilities_json=json.dumps(result["class_probabilities"]),
        execution_time_ms=result["execution_time_ms"]
    )

    pred_repo = PredictionRepository(db)
    saved = pred_repo.create(prediction)

    return PredictionResponse(
        id=saved.id,
        image_id=saved.image_id,
        model_name=saved.model_name,
        model_version=saved.model_version,
        predicted_class=saved.predicted_class,
        confidence_score=saved.confidence_score,
        class_probabilities=result["class_probabilities"],
        execution_time_ms=saved.execution_time_ms,
        predicted_at=saved.predicted_at
    )
