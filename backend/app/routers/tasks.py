from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import insert, select, update, delete
from ..db import engine
from ..models import tasks
from ..schemas import TaskCreate, TaskUpdate, TaskOut
from ..deps import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskOut)
def create_task(data: TaskCreate, user_id: int = Depends(get_current_user_id)):
    with engine.begin() as conn:
        result = conn.execute(
            insert(tasks).values(title=data.title, completed=False, owner_id=user_id)
        )
        task_id = result.lastrowid
    return {"id": task_id, "title": data.title, "completed": False}

@router.get("/", response_model=list[TaskOut])
def list_tasks(user_id: int = Depends(get_current_user_id)):
    with engine.connect() as conn:
        rows = conn.execute(
            select(tasks).where(tasks.c.owner_id == user_id)
        ).mappings().all()
    return list(rows)

@router.get("/{task_id}")
def get_task(task_id: int):
    with engine.connect() as conn:
        row = conn.execute(
            select(tasks).where(tasks.c.id == task_id)
        ).mappings().first()
        if not row:
            raise HTTPException(404, "Task not found")
        return row

@router.put("/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    values = {k: v for k, v in data.dict().items() if v is not None}
    if not values:
        raise HTTPException(400, "No data to update")
    with engine.begin() as conn:
        res = conn.execute(
            update(tasks).where(tasks.c.id == task_id).values(**values)
        )
        if res.rowcount == 0:
            raise HTTPException(404, "Task not found")
    return {"status": "updated"}

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    with engine.begin() as conn:
        res = conn.execute(delete(tasks).where(tasks.c.id == task_id))
        if res.rowcount == 0:
            raise HTTPException(404, "Task not found")
