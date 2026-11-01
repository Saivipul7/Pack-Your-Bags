# RoamWise - Local-first smart tourism companion

RoamWise is a runnable student project with a React/Vite frontend and Django REST backend. It includes a destination explorer, preference-based itinerary generator, editable day plans, estimated spend and carbon, local business discovery, plan recovery, group voting, trip expenses, multilingual UI labels, offline itinerary caching, safety support, business listing submissions, and report/correction flows.

## Run in VS Code

Requirements: Python 3.10+ and Node.js 18+.

1. Open this folder in VS Code.
2. In a terminal, run `start-windows.bat` (or `./start.sh` on macOS/Linux). The script creates a Python virtual environment, installs dependencies, migrates the local SQLite database, and starts Django and Vite.
3. Open http://localhost:5173. Django API: http://127.0.0.1:8000/api/.

The app seeds a curated demo destination on first launch. Listings and live conditions are demo data; booking links lead to provider pages where available. No payment credentials or external API keys are needed. Map preview uses OpenStreetMap tiles and requires internet; core planning works offline after first load.

## Feature guide

- **Plan:** describe budget, dates, interests, pace, party and access needs; generate a day-by-day plan grounded in curated places. Reorder, remove, add, refresh and export the itinerary.
- **Local concierge:** ask natural-language discovery questions and get matches grounded in the verified destination directory. It clearly flags that hours and availability need checking.
- **Recover:** simulate rain, closure, delay, or less available time and choose a nearby replacement with time/cost impact.
- **Discover:** filter local food, artisans, tours and attractions; listings show verification status, source, hours, accessibility notes and directions.
- **Group:** share a trip code, add participants and vote on itinerary stops.
- **Expenses:** record shared costs, currency and payer; see per-person totals and suggested settlement.
- **Responsible travel:** see estimated emissions and lower-impact transport suggestions.
- **Support:** emergency contacts, SOS demo, essential trip info, language labels and offline saved plan.
- **For businesses:** submit or update a listing; submissions appear in the admin review queue.
- **Trust:** report inaccurate listings; source and last-checked dates are displayed.

The local concierge uses transparent keyword and category matching so it does not fabricate places, hours or prices. An LLM provider can be connected later through the assistant API boundary.

## Project layout

`backend/` Django REST API and SQLite data models. `frontend/` React app. `start-windows.bat` and `start.sh` are local launchers.

## API

`GET /api/bootstrap/` returns destination, places and app settings. `POST /api/trips/` creates a planned trip; `GET/PATCH /api/trips/<id>/` reads or updates it. `POST /api/trips/<id>/recover/` suggests replacements. `POST /api/trips/<id>/expenses/` adds an expense; `POST /api/trips/<id>/votes/` records a vote. `POST /api/business-submissions/` and `/api/reports/` accept community updates. `POST /api/assistant/` returns grounded local-guide matches. `GET /api/health/` checks service status.

This is a learning prototype, not a production booking or emergency dispatch system. SOS presents local emergency details and a demo confirmation; travelers should contact local emergency services directly.
