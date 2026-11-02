"""
Audit Log Model
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from backend.app.database.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    resource_endpoint = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
