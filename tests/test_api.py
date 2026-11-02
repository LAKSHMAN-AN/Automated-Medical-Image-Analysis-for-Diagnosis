"""
Automated Test Suite for FastAPI Medical AI Backend
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Operational"

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_register_and_login_flow():
    # Register test user
    email = f"test_{os.urandom(4).hex()}@hospital.org"
    register_payload = {
        "email": email,
        "password": "TestPassword123!",
        "full_name": "Test Radiologist",
        "role": "RADIOLOGIST"
    }
    reg_response = client.post("/api/v1/auth/register", json=register_payload)
    assert reg_response.status_code == 201

    # Login test user
    login_data = {
        "username": email,
        "password": "TestPassword123!"
    }
    login_response = client.post("/api/v1/auth/login", data=login_data)
    assert login_response.status_code == 200
    token_json = login_response.json()
    assert "access_token" in token_json
    assert token_json["token_type"] == "bearer"
