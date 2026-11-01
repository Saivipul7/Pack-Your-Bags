@echo off
cd /d "%~dp0"
if not exist backend\.venv\Scripts\python.exe py -3 -m venv backend\.venv
call backend\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
cd backend
python manage.py migrate
start "RoamWise API" cmd /k "..\backend\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000"
cd ..\frontend
call npm install
npm run dev -- --host 127.0.0.1
