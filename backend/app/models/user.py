"""
User Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from backend.app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="RADIOLOGIST")  # ADMIN, DOCTOR, RADIOLOGIST, PATIENT
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
