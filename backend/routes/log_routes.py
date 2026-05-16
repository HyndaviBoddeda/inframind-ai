from fastapi import APIRouter
from models.log_models import LogRequest
from services.log_services import analyze_log

router = APIRouter()

@router.post("/analyze-log")
def analyze(request: LogRequest):

    result = analyze_log(request.log_text)

    return result