# Pydantic schemas: UserMessage, AIResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserMessage(BaseModel):
    message: str

class AIResponse(BaseModel):
    diagnosis: str # "Vấn đề ở đâu"
    case_type: str # "Case này là gì"
    solution: str # "Giải quyết như thế nào"


