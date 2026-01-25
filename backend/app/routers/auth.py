from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select
from ..db import engine
from ..models import users
from ..schemas import UserCreate, UserLogin, Token
from ..security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: UserCreate):
    with engine.connect() as conn:
        exists = conn.execute(
            select(users.c.id).where(users.c.email == data.email)
        ).first()
        if exists:
            raise HTTPException(400, "Email already registered")

    with engine.begin() as conn:
        conn.execute(
            insert(users).values(
                email=data.email,
                hashed_password=hash_password(data.password)
            )
        )

    return {"status": "registered"}


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    with engine.connect() as conn:
        user = conn.execute(
            select(users).where(users.c.email == data.email)
        ).mappings().first()

    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(subject=str(user["id"]))
    return {"access_token": token, "token_type": "bearer"}
