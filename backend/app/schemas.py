from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool
