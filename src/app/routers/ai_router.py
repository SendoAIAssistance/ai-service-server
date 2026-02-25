# Endpoint: /process (nhận userMessage, call service)
from fastapi import APIRouter, Depends
from ai_engine.schemas.ai_schema import UserMessage, AIResponse
from ai_engine.services.ai_service import AIService
from pydantic import BaseModel
from typing import Literal

router = APIRouter()


# Endpoint để xử lý tin nhắn hỗ trợ kỹ thuật
# Message Schema

class Message(BaseModel):
    _id: str
    conversationId: str
    message: str
    isAI: bool
    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "ERROR", "CANCELLED"] = "PENDING"
    created_at: str
    updated_at: str

@router.post("/chat-support", response_model=AIResponse)
async def process_chat_support(request: UserMessage):
    service = AIService()
    return await service.process_message(request)
