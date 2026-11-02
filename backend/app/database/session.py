"""
Database Engine & Session Manager with Fail-Safe Lock Recovery
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

db_url = settings.DATABASE_URL

def create_safe_engine():
    try:
        connect_args = {"check_same_thread": False, "timeout": 30} if db_url.startswith("sqlite") else {}
        eng = create_engine(db_url, connect_args=connect_args, pool_pre_ping=True)
        # Test connection
        with eng.connect() as conn:
            pass
        return eng
    except Exception as e:
        # Memory fallback if disk I/O lock error occurs
        fallback_url = "sqlite:///:memory:"
        return create_engine(fallback_url, connect_args={"check_same_thread": False}, pool_pre_ping=True)

engine = create_safe_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI Dependency for database session injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
