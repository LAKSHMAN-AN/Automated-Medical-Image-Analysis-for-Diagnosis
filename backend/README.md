# Automated Medical Image Analysis - Backend API Service

Production-ready FastAPI backend for **Automated Medical Image Analysis for Diagnosis**, supporting multi-modal image classification, Grad-CAM visual explainability, clinical NLP entity extraction, SLM report summarization, GenAI synthetic data generation, and Agentic AI diagnostic workflows.

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Seed Database
```bash
python -m backend.app.database.seeder
```

### 3. Run FastAPI Application Server
```bash
uvicorn backend.app.main:app --reload --port 8000
```

---

## 📚 Interactive API Documentation (Swagger / ReDoc)
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🔒 Default Admin Credentials (Seeded)
- **Admin:** `admin@medicalai.org` / `AdminSecret2026!`
- **Radiologist:** `radiologist@hospital.org` / `RadioSecret2026!`
