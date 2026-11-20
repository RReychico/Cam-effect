#!/bin/bash
# macOS launcher (equivalent of AVVIA_LOCALE.bat). Double-click in Finder or run:
#   ./VanishCam.command [--mode normal|naruto|particles|goku|itachi] [--camera N] [--no-virtual-camera]
set -e
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
  echo "[Vanish Lab] Creating local Python environment..."
  python3 -m venv .venv
fi
if ! .venv/bin/python -c "import cv2, mediapipe, numpy, pyvirtualcam, pygame, certifi" 2>/dev/null; then
  echo "[Vanish Lab] Installing dependencies (internet needed only this time)..."
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -r local_app/requirements.txt
fi

# python.org builds ship without root certs; model downloads need them.
export SSL_CERT_FILE="$(.venv/bin/python -m certifi)"
exec .venv/bin/python local_app/vanish_cam.py "$@"
