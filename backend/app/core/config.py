"""
Production Configuration Settings
Compatible with Pydantic v1 and v2
"""

import os
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    try:
        from pydantic.v1 import BaseSettings, Field
    except ImportError:
        from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Automated Medical Image Analysis API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = Field(default="super-secret-medical-ai-jwt-key-change-in-production-2026", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = Field(default="sqlite:///./medical_analysis.db", env="DATABASE_URL")
    
    UPLOAD_DIR: str = Field(default="datasets/uploaded_scans", env="UPLOAD_DIR")
    MODEL_DIR: str = Field(default="ml/models", env="MODEL_DIR")
    DL_MODEL_DIR: str = Field(default="dl/weights", env="DL_MODEL_DIR")
    
    # Dataset directory paths
    CHEST_XRAY_DIR: str = Field(default="datasets/chest_xray", env="CHEST_XRAY_DIR")
    BRAIN_MRI_DIR: str = Field(default="datasets/brain_mri", env="BRAIN_MRI_DIR")
    LUNG_CT_DIR: str = Field(default="datasets/lung_ct", env="LUNG_CT_DIR")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.DL_MODEL_DIR, exist_ok=True)
