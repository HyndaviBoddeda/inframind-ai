from fastapi import FastAPI

from database import engine, Base
from models.incident import Incident

from routes.health import router as health_router
from routes.log_routes import router as log_router
from routes.ai_routes import router as ai_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health_router)
app.include_router(log_router)
app.include_router(ai_router)