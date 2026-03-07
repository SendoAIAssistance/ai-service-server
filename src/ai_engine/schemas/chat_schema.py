"""
Chat-specific schemas - Đồng bộ với frontend Message interface
"""
from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class MessageStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class StreamEvent(BaseModel):
    type: str  # thinking = bước suy nghĩ, chunk = chữ trong response
    content: str
    status: MessageStatus = MessageStatus.IN_PROGRESS

class UserMessage(BaseModel):
    """Input từ user qua form"""
    message: str
    # files sẽ được xử lý riêng ở route (UploadFile)

class ChatMessage(BaseModel): # dùng sau này cho conversation history
    _id: Optional[str] = None
    conversationID: str
    message: str
    files: Optional[List[str]] = None
    status: MessageStatus = MessageStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    thinking: Optional[str] = None
    thinkingDuration: Optional[int] = None
    isAI: bool = False

