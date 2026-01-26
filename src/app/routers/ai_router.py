# Endpoint: /process (nhận userMessage, call service)
from fastapi import APIRouter, Depends
from ai_engine.schemas.ai_schema import UserMessage, AIResponse
from ai_engine.services.ai_service import AIService

router = APIRouter()

@router.post("/process", response_model=AIResponse)
async def process_request(request: UserMessage):
    service = AIService()
    return await service.process_message(request)
