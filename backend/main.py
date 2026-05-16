from fastapi import FastAPI

from routes.health import router as health_router
from routes.log_routes import router as log_router
from routes.ai_routes import router as ai_router

app = FastAPI()

app.include_router(health_router)
app.include_router(log_router)
app.include_router(ai_router)

@app.get("/")
def home():
    return {
        "message": "InfraMind AI Backend Running"
    }