from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert
from app.db import engine
from app.models import users
from app.schemas import UserCreate, UserLogin, Token
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(data: UserCreate):
    with engine.begin() as conn:
        exists = conn.execute(select(users.c.id).where(users.c.email == data.email)).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")

        result = conn.execute(
            insert(users).values(
                email=data.email,
                hashed_password=hash_password(data.password)
            )
        )
        user_id = result.lastrowid

    return {"id": user_id, "email": data.email}

@router.post("/login", response_model=Token)
def login(data: UserLogin):
    with engine.connect() as conn:
        row = conn.execute(select(users).where(users.c.email == data.email)).mappings().first()

    if not row or not verify_password(data.password, row["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(row["id"]))
    return {"access_token": token, "token_type": "bearer"}