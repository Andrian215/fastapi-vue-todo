from fastapi import FastAPI
from .db import engine, metadata
from .routers.tasks import router as tasks_router

app = FastAPI()
metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(tasks_router)
