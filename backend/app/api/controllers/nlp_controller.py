"""
NLP Controller Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.services.nlp_service import NLPService
from backend.app.dependencies.auth_deps import require_doctor_or_radiologist

router = APIRouter(prefix="/nlp", tags=["NLP"])
nlp_service = NLPService()

class NLPExtractRequest(BaseModel):
    clinical_text: str

@router.post("/extract", dependencies=[Depends(require_doctor_or_radiologist)])
def extract_entities(req: NLPExtractRequest):
    entities = nlp_service.extract_entities(req.clinical_text)
    return {"cleaned_text": nlp_service.clean_text(req.clinical_text), "entities": entities}
