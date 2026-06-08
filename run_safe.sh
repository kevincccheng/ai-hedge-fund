#!/usr/bin/env bash
# AI Hedge Fund - Safe Launcher (crash protected)
cd "$(dirname "$0")"
chmod +x "$0"

mkdir -p crash_logs

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="crash_logs/run_${TIMESTAMP}.log"

echo "================================================"
echo " AI Hedge Fund - Safe Launcher (crash protected)"
echo "================================================"
echo "[INFO] Logging output to $LOGFILE"
echo

./run.sh > "$LOGFILE" 2>&1
EXITCODE=$?

if [ $EXITCODE -ne 0 ]; then
    echo "[ERROR] run.sh exited with code $EXITCODE"
    echo "[ERROR] Crash log saved to $LOGFILE"
    if [ -d "outputs" ]; then
        echo "[INFO] Preserving any partial report output..."
        cp outputs/*.json crash_logs/ 2>/dev/null || true
    fi
else
    echo "[SUCCESS] Run finished. Log saved to $LOGFILE"
fi
