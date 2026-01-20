from fastapi import FastAPI
from sqlalchemy import insert, select
from .db import engine, metadata
from .models import tasks

app = FastAPI()
metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/tasks")
def create_task(title: str):
    with engine.begin() as conn:
        result = conn.execute(insert(tasks).values(title=title))
        task_id = result.lastrowid
    return {"id": task_id, "title": title, "completed": False}

@app.get("/tasks")
def list_tasks():
    with engine.connect() as conn:
        rows = conn.execute(select(tasks)).mappings().all()
    return list(rows)
