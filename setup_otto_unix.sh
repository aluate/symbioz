#!/bin/bash

# Setup Script - Install All Otto Dependencies
# Run this once to set up Otto + Life OS
# Usage: ./setup_otto_unix.sh

set -e  # Exit on error

echo ""
echo "========================================"
echo "  Setting Up Otto + Life OS"
echo "========================================"
echo ""
echo "This will install all dependencies needed."
echo ""

# Get the directory where this script is located (repo root)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Repo root: $REPO_ROOT"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3 and try again"
    exit 1
fi

# Check for Node.js (optional but recommended)
SKIP_FRONTEND=0
if ! command -v node &> /dev/null; then
    echo "WARNING: Node.js not found. Frontend setup will be skipped."
    echo "Install Node.js from https://nodejs.org/ if you want the frontend."
    SKIP_FRONTEND=1
fi

# Create virtualenv if it doesn't exist (optional but recommended)
if [ ! -d "$REPO_ROOT/.venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv "$REPO_ROOT/.venv"
    echo "✓ Virtual environment created"
fi

# Activate virtualenv
echo ""
echo "Activating virtual environment..."
source "$REPO_ROOT/.venv/bin/activate"

# 1. Install Otto dependencies
echo ""
echo "[1/3] Installing Otto dependencies..."
if [ -f "$REPO_ROOT/apps/otto/requirements.txt" ]; then
    pip install -r "$REPO_ROOT/apps/otto/requirements.txt"
    echo "✓ Otto dependencies installed"
else
    echo "WARNING: requirements.txt not found in apps/otto"
fi

# 2. Install Life OS Backend dependencies
echo ""
echo "[2/3] Installing Life OS Backend dependencies..."
if [ -f "$REPO_ROOT/apps/life_os/backend/requirements.txt" ]; then
    pip install -r "$REPO_ROOT/apps/life_os/backend/requirements.txt"
    echo "✓ Life OS Backend dependencies installed"
else
    echo "WARNING: requirements.txt not found in apps/life_os/backend"
fi

# 3. Install Life OS Frontend dependencies
if [ "$SKIP_FRONTEND" -eq 0 ]; then
    echo ""
    echo "[3/3] Installing Life OS Frontend dependencies..."
    if [ -f "$REPO_ROOT/apps/life_os/frontend/package.json" ]; then
        cd "$REPO_ROOT/apps/life_os/frontend"
        npm install
        echo "✓ Life OS Frontend dependencies installed"
        cd "$REPO_ROOT"
    else
        echo "WARNING: package.json not found in apps/life_os/frontend"
    fi
else
    echo ""
    echo "[3/3] Skipping Frontend (Node.js not found)"
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Run ./start_otto_unix.sh to start everything"
echo "  2. Open http://localhost:3000/otto in your browser"
echo "  3. Start talking to Otto!"
echo ""

