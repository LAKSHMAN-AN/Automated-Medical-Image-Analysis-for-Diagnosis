"""
Medical Image Upload Controller Endpoints
"""

import os
import hashlib
import uuid
import cv2
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.database.session import get_db
from backend.app.models.image import MedicalImage
from backend.app.repositories.image_repository import ImageRepository
from backend.app.schemas.image_schema import ImageUploadResponse
from backend.app.dependencies.auth_deps import require_radiologist_or_admin

router = APIRouter(prefix="/images", tags=["Medical Images"])

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.dcm'}

@router.post("/upload", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_radiologist_or_admin)])
async def upload_medical_image(
    file: UploadFile = File(...),
    patient_id: str = Form(...),
    modality: str = Form("CHEST_XRAY"),
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported file format {ext}")

    contents = await file.read()
    if len(contents) > 50 * 1024 * 1024:  # 50MB Limit
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeds 50MB limit")

    file_hash = hashlib.sha256(contents).hexdigest()
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    # Validate image dimensions using OpenCV
    height, width = None, None
    try:
        img = cv2.imread(filepath)
        if img is not None:
            height, width, _ = img.shape
    except Exception:
        pass

    image_record = MedicalImage(
        patient_id=patient_id,
        image_url=filepath,
        modality=modality.upper(),
        width=width,
        height=height,
        file_hash=file_hash
    )

    repo = ImageRepository(db)
    return repo.create(image_record)
