#!/usr/bin/env bash
# macOS / Linux: crea un entorno virtual, instala python-garminconnect y conecta.
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Instala Python 3.10+ (https://www.python.org/downloads/)"; exit 1; }
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/python -m pip install -q --upgrade pip
./.venv/bin/python -m pip install -q -r requirements.txt
exec ./.venv/bin/python conectar_garmin.py
