from fastapi import APIRouter
from models.log_models import LogRequest
from services.ai_service import analyze_with_ai

router = APIRouter()

@router.post("/ai-analyze-log")
def ai_analyze(request: LogRequest):

    result = analyze_with_ai(request.log_text)

    return result