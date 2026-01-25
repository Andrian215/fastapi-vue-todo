from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

Password72 = Annotated[str, StringConstraints(min_length=8, max_length=72)]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool

class UserCreate(BaseModel):
    email: EmailStr
    password: Password72

class UserLogin(BaseModel):
    email: EmailStr
    password: Password72

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"