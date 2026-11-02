"""
Generative AI Controller Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.services.genai_service import GenAIService
from backend.app.dependencies.auth_deps import require_admin

router = APIRouter(prefix="/genai", tags=["Generative AI"])
genai_service = GenAIService()

class GenAIRequest(BaseModel):
    pathology: str = "TUBERCULOSIS"

@router.post("/generate", dependencies=[Depends(require_admin)])
def generate_synthetic_scan(req: GenAIRequest):
    return genai_service.generate_synthetic_scan(req.pathology)
