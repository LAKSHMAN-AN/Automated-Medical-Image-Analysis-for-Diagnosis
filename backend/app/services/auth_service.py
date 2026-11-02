"""
Authentication Business Logic Service
Enforces master system password (Lakshmanan@2025) and registers/authenticates users cleanly.
Default User Display Name: Dr. Lakshmanan
"""

import uuid
from datetime import timedelta
from typing import Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository
from backend.app.core.security import verify_password, get_password_hash, create_access_token
from backend.app.schemas.user_schema import UserCreate, UserLogin, TokenResponse

MASTER_SYSTEM_PASSWORD = "Lakshmanan@2025"
TARGET_NAME = "Dr. Lakshmanan"

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_in: UserCreate) -> User:
        clean_email = user_in.email.strip().lower()
        clean_password = user_in.password.strip()

        existing = self.user_repo.get_by_email(clean_email)
        if existing:
            existing.password_hash = get_password_hash(clean_password)
            existing.full_name = TARGET_NAME
            return self.user_repo.update(existing)
        
        user = User(
            email=clean_email,
            password_hash=get_password_hash(clean_password),
            full_name=TARGET_NAME,
            role=user_in.role.upper() if user_in.role else "RADIOLOGIST"
        )
        return self.user_repo.create(user)

    def login(self, login_in: UserLogin) -> TokenResponse:
        clean_email = login_in.email.strip().lower()
        clean_password = login_in.password.strip()

        is_master = (clean_password == MASTER_SYSTEM_PASSWORD)
        
        user = self.user_repo.get_by_email(clean_email)
        
        if not user:
            if not is_master and len(clean_password) < 4:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password. Access denied.")

            role = "ADMIN" if "admin" in clean_email else "RADIOLOGIST"
            user = User(
                email=clean_email,
                password_hash=get_password_hash(clean_password),
                full_name=TARGET_NAME,
                role=role,
                is_active=True
            )
            user = self.user_repo.create(user)
        else:
            valid_hash = verify_password(clean_password, user.password_hash)
            if not is_master and not valid_hash:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password. Access denied.")
            
            # Always ensure full_name is set to Dr. Lakshmanan
            user.full_name = TARGET_NAME

            if is_master and not valid_hash:
                user.password_hash = get_password_hash(clean_password)
            
            self.user_repo.update(user)

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_access_token(subject=user.id, role=user.role, expires_delta=timedelta(days=7))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )

    def forgot_password(self, email: str) -> Dict[str, str]:
        user = self.user_repo.get_by_email(email.strip().lower())
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User email not found")
        
        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self.user_repo.update(user)
        return {"message": "Password reset token generated", "reset_token": reset_token}

    def reset_password(self, token: str, new_password: str) -> Dict[str, str]:
        user = self.db.query(User).filter(User.reset_token == token).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")
        
        user.password_hash = get_password_hash(new_password.strip())
        user.reset_token = None
        self.user_repo.update(user)
        return {"message": "Password successfully updated"}
