# Pydantic schemas: UserMessage, AIResponse
from typing import Optional, Union
from fastapi import UploadFile, File
from pydantic import BaseModel

class AIResponse(BaseModel):
    """
    Response trả về cho /chat endpoint
    - thinking: quá trình suy nghĩ (string, dễ hiển thị trên UI)
    - response: câu trả lời cuối cùng
    """
    thinking: str = ""
    response: str = ""
