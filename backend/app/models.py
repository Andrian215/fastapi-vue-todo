from sqlalchemy import Table, Column, Integer, String, Boolean
from .db import metadata

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("completed", Boolean, default=False),
)
