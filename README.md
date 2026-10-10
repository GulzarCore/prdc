# DevOps Lab

A lightweight three-tier task tracker for hands-on DevOps practice.

## Architecture

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Database: PostgreSQL

## Prerequisites

- Python 3
- PostgreSQL
- Git

## Setup

Create and activate a Python virtual environment, then install
dependencies:

    python3 -m venv .venv
    source .venv/bin/activate.fish
    python -m pip install -r requirements.txt

Create the devops_lab database and devops_user role in PostgreSQL.

Set the DATABASE_URL environment variable using your local
database credentials.

## Run

    uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000

Open http://127.0.0.1:8000.

## Test

    ./scripts/test.sh
    ./scripts/check.sh

## API

- GET /healthz
- GET /readyz
- GET /api/tasks
- POST /api/tasks
- PATCH /api/tasks/{task_id}
- DELETE /api/tasks/{task_id}

## Roadmap

1. Git and scripting
2. Docker and Compose
3. CI/CD
4. Kubernetes
5. Monitoring and security# prdc
# prdc
# prdc
