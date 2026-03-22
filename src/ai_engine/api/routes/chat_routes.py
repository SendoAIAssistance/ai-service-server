"""
Chat/Query routes - sử dụng ChromaDB để retrieve context cho RAG.
"""
import datetime
from typing import Optional, Union
import logging

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse

from ai_engine.services.ai_service import AIService
from ai_engine.api.dependencies import get_ai_service
from ai_engine.schemas.ai_schema import  AIResponse
from ai_engine.schemas.chat_schema import ChatMessage
from fastapi.responses import StreamingResponse

router = APIRouter(
    tags=["Chat/Agent"],
)

chat_logger = logging.getLogger("ai_engine.api.routes.chat_routes")

@router.post("/chat", response_model=AIResponse)
async def chat(
        conversationId: str = Form(...),
        message: str = Form(default="Hi"),
        files: Optional[Union[UploadFile, str]] = File(None),
        ai_service: AIService = Depends(get_ai_service),
):
    """
    Endpoint nhận message và file từ user,
    trả về kết quả chẩn đoán
    """
    return StreamingResponse(
        ai_service.stream_message(conversation_id=conversationId, message=message, file=files),
        media_type="text/event-stream"
    )
