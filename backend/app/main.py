from fastapi import FastAPI
from .db import engine, metadata
from .routers.tasks import router as tasks_router
from .routers.auth import router as auth_router 
from fastapi.security import HTTPBearer

app = FastAPI()
security = HTTPBearer()
metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(tasks_router)
