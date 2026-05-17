# InfraMind AI

InfraMind AI is an AI-driven Cloud Operations Copilot designed to analyze infrastructure logs, classify incidents, assign severity, track incident status, and maintain incident history.

## Features

- Analyze infrastructure logs
- Classify incidents
- Assign severity levels
- Store incidents in SQLite
- Retrieve incident history
- Filter incidents
- View incident details
- Update incident status

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Docker

## Run Project

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Open Swagger docs at:

http://127.0.0.1:8000/docs
