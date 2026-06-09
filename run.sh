#!/usr/bin/env bash
# AI Hedge Fund - Kevin's Launcher (Mac/Linux)

cd "$(dirname "$0")"

echo "================================================"
echo " AI Hedge Fund - Kevin's Launcher (Mac/Linux)"
echo "================================================"
echo

if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

source .venv/bin/activate
export PYTHONIOENCODING=utf-8

echo "[INFO] Starting backend (FastAPI) on http://127.0.0.1:8000 ..."
nohup poetry run uvicorn app.backend.main:app --host 127.0.0.1 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

echo "[INFO] Starting frontend (React) on http://localhost:5173 ..."
(cd app/frontend && nohup npm run dev > ../../frontend.log 2>&1 &)

echo "[INFO] Waiting for services to start..."
sleep 5

echo "[INFO] Seeding default flow (first run only)..."
python3 seed_default_flow.py

echo "[INFO] Opening browser..."
open "http://localhost:5173" 2>/dev/null || true

echo
echo "================================================"
echo " AI Hedge Fund is running"
echo " Frontend: http://localhost:5173"
echo " Backend:  http://127.0.0.1:8000  (pid $BACKEND_PID)"
echo " Docs:     http://127.0.0.1:8000/docs"
echo
echo " Logs: backend.log / frontend.log"
echo " Stop the app with: kill $BACKEND_PID  (and quit the npm run dev process)"
echo "================================================"
echo

# Convert the latest saved analysis report (outputs/*.json) to a PDF, if any
python3 convert_report.py
