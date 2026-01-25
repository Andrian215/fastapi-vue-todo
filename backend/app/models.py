from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from .db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), unique=True, nullable=False),
    Column("hashed_password", String(255), nullable=False),
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("completed", Boolean, default=False),
    Column("owner_id", Integer, ForeignKey("users.id"), nullable=False),
)
