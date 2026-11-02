"""
FastAPI Enterprise Application Gateway Entrypoint
Automated Medical Image Analysis for Diagnosis
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.database.session import engine, Base

# Import all SQLAlchemy models to ensure metadata registration
from backend.app.models.user import User
from backend.app.models.patient import Patient
from backend.app.models.image import MedicalImage
from backend.app.models.prediction import Prediction
from backend.app.models.report import DiagnosticReport
from backend.app.models.feedback import Feedback
from backend.app.models.audit import AuditLog

# Import API Controllers
from backend.app.api.controllers.auth_controller import router as auth_router
from backend.app.api.controllers.user_controller import router as user_router
from backend.app.api.controllers.patient_controller import router as patient_router
from backend.app.api.controllers.upload_controller import router as upload_router
from backend.app.api.controllers.prediction_controller import router as prediction_router
from backend.app.api.controllers.nlp_controller import router as nlp_router
from backend.app.api.controllers.slm_controller import router as slm_router
from backend.app.api.controllers.genai_controller import router as genai_router
from backend.app.api.controllers.agent_controller import router as agent_router
from backend.app.api.controllers.analytics_controller import router as analytics_router
from backend.app.api.controllers.feedback_controller import router as feedback_router

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise REST API backend for AI-assisted radiological diagnosis, explainability, clinical summarization, and agentic workflows.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api/v1
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(patient_router, prefix=settings.API_V1_STR)
app.include_router(upload_router, prefix=settings.API_V1_STR)
app.include_router(prediction_router, prefix=settings.API_V1_STR)
app.include_router(nlp_router, prefix=settings.API_V1_STR)
app.include_router(slm_router, prefix=settings.API_V1_STR)
app.include_router(genai_router, prefix=settings.API_V1_STR)
app.include_router(agent_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(feedback_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Operational",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
