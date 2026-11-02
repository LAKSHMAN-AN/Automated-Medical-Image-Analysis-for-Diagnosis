"""
Database Seeder Script
Initializes default roles, admin user, test radiologist, and demo patient data.
Default User Display Name: Dr. Lakshmanan
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from sqlalchemy.orm import Session
from backend.app.database.session import SessionLocal, engine, Base
from backend.app.models.user import User
from backend.app.models.patient import Patient
from backend.app.core.security import get_password_hash

DEFAULT_SEED_PASSWORD = "Lakshmanan@2025"
TARGET_NAME = "Dr. Lakshmanan"

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Create/Update Admin User
        admin_email = "admin@medicalai.org"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                email=admin_email,
                password_hash=get_password_hash(DEFAULT_SEED_PASSWORD),
                full_name=TARGET_NAME,
                role="ADMIN",
                is_active=True
            )
            db.add(admin_user)
        else:
            admin_user.full_name = TARGET_NAME
            admin_user.password_hash = get_password_hash(DEFAULT_SEED_PASSWORD)

        # 2. Create/Update Test Radiologist User
        radio_email = "radiologist@hospital.org"
        radio_user = db.query(User).filter(User.email == radio_email).first()
        if not radio_user:
            radio_user = User(
                email=radio_email,
                password_hash=get_password_hash(DEFAULT_SEED_PASSWORD),
                full_name=TARGET_NAME,
                role="RADIOLOGIST",
                is_active=True
            )
            db.add(radio_user)
        else:
            radio_user.full_name = TARGET_NAME
            radio_user.password_hash = get_password_hash(DEFAULT_SEED_PASSWORD)

        # Update all existing users in DB to Dr. Lakshmanan
        all_users = db.query(User).all()
        for u in all_users:
            u.full_name = TARGET_NAME
            u.password_hash = get_password_hash(DEFAULT_SEED_PASSWORD)

        # 3. Create Sample Patient
        patient_code = "PAT-2026-001"
        sample_patient = db.query(Patient).filter(Patient.patient_code == patient_code).first()
        if not sample_patient:
            sample_patient = Patient(
                patient_code=patient_code,
                age=54,
                gender="MALE",
                medical_history="Non-smoker, presented with acute fever, persistent cough, and dyspnea for 4 days."
            )
            db.add(sample_patient)

        db.commit()
        print("Database Seeding & Name Update to 'Dr. Lakshmanan' Completed Successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
