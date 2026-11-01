#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py runserver 127.0.0.1:8000 &
API_PID=$!
trap 'kill $API_PID 2>/dev/null || true' EXIT
cd ../frontend
npm install
npm run dev -- --host 127.0.0.1
