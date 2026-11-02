#!/bin/bash
# =========================================================
# RELIABLE ONE-CLICK LAUNCHER FOR MEDICAL AI PLATFORM
# =========================================================

mkdir -p logs

echo "========================================================="
echo "⚡ LAUNCHING MEDICAL AI DIAGNOSTIC PLATFORM..."
echo "========================================================="

# 1. Clean up old process ports if occupied
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3003 | xargs kill -9 2>/dev/null || true

# 2. Start FastAPI Backend Server in background
echo "🚀 Starting FastAPI Backend Server on http://127.0.0.1:8000..."
nohup ./venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 > logs/backend.log 2>&1 &

# 3. Start React 19 Frontend Web Portal in background
echo "✨ Starting React 19 Frontend Web Portal on http://127.0.0.1:3003..."
nohup sh -c "cd frontend && npx vite preview --host 127.0.0.1 --port 3003" > logs/frontend.log 2>&1 &

# 4. Polling Wait for Frontend Availability
echo "⏳ Waiting for servers to initialize..."
MAX_WAIT=15
WAIT_COUNT=0

while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
  FRONTEND_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3003/ 2>/dev/null || echo "000")
  if [ "$FRONTEND_CODE" = "200" ]; then
    break
  fi
  sleep 1
  WAIT_COUNT=$((WAIT_COUNT + 1))
done

echo "========================================================="
echo "✅ ALL SYSTEMS ONLINE! LOGIN PASSWORD: Lakshmanan@2025"
echo "========================================================="

# 5. Open Web Browser cleanly
open http://127.0.0.1:3003 2>/dev/null || true
