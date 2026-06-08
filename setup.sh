#!/usr/bin/env bash
# AI Hedge Fund - Kevin's Setup (Mac/Linux)
set -e

cd "$(dirname "$0")"
chmod +x "$0"

echo "================================================"
echo " AI Hedge Fund - Kevin's Setup (Mac/Linux)"
echo "================================================"
echo

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 is not installed. Install it from https://python.org/"
    exit 1
fi

if ! command -v node >/dev/null 2>&1; then
    echo "[ERROR] Node.js is not installed. Install it from https://nodejs.org/"
    exit 1
fi

echo "[INFO] Configuring git line endings..."
git config core.autocrlf input

echo "[INFO] Creating Python virtual environment (.venv)..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
else
    echo "[INFO] .venv already exists, skipping creation"
fi

echo "[INFO] Activating virtual environment and installing Python dependencies..."
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install poetry reportlab
poetry install

echo "[INFO] Installing frontend (Node.js) dependencies..."
pushd app/frontend > /dev/null
npm install
popd > /dev/null

echo "[INFO] Setting up environment file..."
if [ ! -f ".env" ]; then
    if [ -f ".env.kevin.example" ]; then
        cp ".env.kevin.example" ".env"
        echo "[INFO] Created .env from .env.kevin.example - edit it to add your API keys"
    else
        echo "[WARNING] .env.kevin.example not found - create .env manually with your API keys"
    fi
else
    echo "[INFO] .env already exists, leaving it untouched"
fi

echo
echo "================================================"
echo " [SUCCESS] Setup complete!"
echo " Next step: edit .env with your API keys, then"
echo " run ./run.sh to start the app"
echo "================================================"
