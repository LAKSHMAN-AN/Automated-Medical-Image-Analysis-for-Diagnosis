#!/bin/bash
# Free port 8000 if currently occupied by any background process
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

echo "Starting FastAPI Backend Server on http://127.0.0.1:8000..."
./venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
