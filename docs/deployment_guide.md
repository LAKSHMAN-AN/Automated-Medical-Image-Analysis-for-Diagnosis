# Production Deployment & Setup Guide

## System Requirements
- **OS:** Linux (Ubuntu 22.04 LTS recommended) / macOS
- **CPU:** 8 Cores minimum
- **RAM:** 16GB RAM minimum (32GB recommended for GPU training)
- **GPU:** NVIDIA GPU with CUDA 11.8+ (Optional for GPU acceleration)
- **Docker:** Docker Engine 24.0+ and Docker Compose v2+

---

## 1. Single Command Docker Deployment

```bash
# Clone Repository and navigate to project root
cd "Automated Medical Image Analysis for Diagnosis"

# Build and launch all microservices (PostgreSQL, FastAPI Backend, React Frontend)
docker-compose up --build -d
```

### Verified Ports:
- **React Frontend (HTTP):** `http://localhost:80`
- **FastAPI Backend (REST API):** `http://localhost:8000`
- **Swagger Documentation:** `http://localhost:8000/docs`
- **PostgreSQL Database:** `localhost:5432`

---

## 2. Local Manual Setup (Development Mode)

### Step 1: Database Seeding
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m backend.app.database.seeder
```

### Step 2: Start Backend
```bash
uvicorn backend.app.main:app --reload --port 8000
```

### Step 3: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 3. Seeded Clinical Credentials

| Role | Email | Default Password |
|---|---|---|
| **System Admin** | `admin@medicalai.org` | `AdminSecret2026!` |
| **Radiologist** | `radiologist@hospital.org` | `RadioSecret2026!` |
| **Sample Patient** | `PAT-2026-001` | N/A |
