"""
Chat/Query routes - sử dụng ChromaDB để retrieve context cho RAG.
"""
from typing import Optional, Union
import logging

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse

from ai_engine.services.ai_service import AIService
from ai_engine.api.dependencies import get_ai_service
from ai_engine.schemas.ai_schema import UserMessage, AIResponse
from ai_engine.core.logging import setup_logging, request_id_var
router = APIRouter(
    tags=["Chat/Agent"],
)

setup_logging()
chat_logger = logging.getLogger("ai_engine.api.routes.chat_routes")

@router.post("/chat", response_model=AIResponse)
async def chat(
        message: str = Form(default="Hi"),
        file: Optional[Union[UploadFile, str]] = File(None),
        ai_service: AIService = Depends(get_ai_service),
):
    """
    Endpoint nhận message và file từ user,
    trả về kết quả chẩn đoán
    """
    return await ai_service.process_message(message=message, file=file)

# @router.post("/chat/stream")
# async def chat_stream(
#     chat_body: UserMessage,
#     request: Request,
#     ai_service: AIService = Depends(get_ai_service),
# ):
#     # Luồng stream cho Orchestra of Agents
#     return await ai_service.chat_stream_sse(body=chat_body)
#
# @router.get("/chat/status/{job_id}")
# async def get_status(
#         job_id: str,
#         ai_service: AIService = Depends(get_ai_service),
# ):
#     # Endpoint để check xem Agent làm việc xong chưa (cho tech support agent)
#     return await ai_service.get_job_status(job_id)