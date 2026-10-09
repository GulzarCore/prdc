import os
from contextlib import asynccontextmanager
from pathlib import Path

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"
DATABASE_URL = os.environ.get("DATABASE_URL", "")


def clean_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    if len(title) > 200:
        raise ValueError("Task title cannot exceed 200 characters")
    return title


class TaskInput(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return clean_title(value)


class TaskUpdate(BaseModel):
    completed: bool


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")
    return psycopg.connect(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
    yield


app = FastAPI(title="DevOps Lab API", lifespan=lifespan)
app.mount("/assets", StaticFiles(directory=FRONTEND), name="assets")


@app.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")


@app.get("/healthz")
def health():
    return {"status": "healthy"}


@app.get("/readyz")
def readiness():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return {"status": "ready", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )


@app.get("/api/tasks")
def list_tasks():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, title, completed
            FROM tasks
            ORDER BY id DESC
        """).fetchall()

    return [
        {"id": row[0], "title": row[1], "completed": row[2]}
        for row in rows
    ]


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskInput):
    with get_connection() as conn:
        row = conn.execute(
            """
            INSERT INTO tasks (title)
            VALUES (%s)
            RETURNING id, title, completed
            """,
            (task.title,),
        ).fetchone()

    return {"id": row[0], "title": row[1], "completed": row[2]}


@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    with get_connection() as conn:
        row = conn.execute(
            """
            UPDATE tasks
            SET completed = %s
            WHERE id = %s
            RETURNING id, title, completed
            """,
            (update.completed, task_id),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"id": row[0], "title": row[1], "completed": row[2]}


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,),
        )

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")









@app.get("/api/version")
def version():
    return {"app": "devops-lab", "version": "1.0.0"}