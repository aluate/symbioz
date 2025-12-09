#!/bin/bash

# Start all Otto services
# This starts: Otto API, Life OS Backend, Life OS Frontend

set -e

echo "Starting Otto + Life OS services..."
echo ""

# Get the directory where this script is located (repo root)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtualenv if it exists
if [ -d "$REPO_ROOT/.venv" ]; then
    source "$REPO_ROOT/.venv/bin/activate"
fi

# Start Otto API (port 8001)
echo "[1/3] Starting Otto API on port 8001..."
cd "$REPO_ROOT/apps/otto"
python -m otto.cli server &
OTTO_PID=$!
sleep 2

# Start Life OS Backend (port 8000)
echo "[2/3] Starting Life OS Backend on port 8000..."
cd "$REPO_ROOT/apps/life_os/backend"
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 2

# Start Life OS Frontend (port 3000)
echo "[3/3] Starting Life OS Frontend on port 3000..."
cd "$REPO_ROOT/apps/life_os/frontend"
npm run dev &
FRONTEND_PID=$!
sleep 2

echo ""
echo "========================================"
echo "  All services starting!"
echo "========================================"
echo ""
echo "Services:"
echo "  - Otto API: http://localhost:8001"
echo "  - Life OS Backend: http://localhost:8000"
echo "  - Life OS Frontend: http://localhost:3000"
echo "  - Otto Console: http://localhost:3000/otto"
echo ""
echo "Process IDs:"
echo "  - Otto API: $OTTO_PID"
echo "  - Life OS Backend: $BACKEND_PID"
echo "  - Life OS Frontend: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "kill $OTTO_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait

