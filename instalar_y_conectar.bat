@echo off
REM Windows: crea un entorno virtual, instala python-garminconnect y conecta.
cd /d "%~dp0"
if not exist .venv ( py -3 -m venv .venv || python -m venv .venv )
.venv\Scripts\python -m pip install -q --upgrade pip
.venv\Scripts\python -m pip install -q -r requirements.txt
.venv\Scripts\python conectar_garmin.py
pause
