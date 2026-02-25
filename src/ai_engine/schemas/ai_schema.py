# Pydantic schemas: UserMessage, AIResponse
from typing import Optional, Union
from fastapi import UploadFile, File
from pydantic import BaseModel


class UserMessage(BaseModel):
    message: str
    # Khi dùng Form-data, file sẽ được xử lý riêng
    # nhưng cứ định nghĩa ở đây để document cho rõ
    file: Optional[Union[UploadFile, str]] = None

class AIResponse(BaseModel):
    diagnosis: str # "Vấn đề ở đâu"
    case_type: str # "Case này là gì"
    solution: str # "Giải quyết như thế nào"
    response: str # Câu trả lời cuối cùng

