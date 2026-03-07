from typing import TypedDict, Annotated, List, Optional
import operator

from pydantic import BaseModel


class AgentState(BaseModel):
    message: Annotated[List[str], operator.add]
    file_data: Optional[bytes] | None
    file_type: Optional[str] | None # "table", "image", "text", "None"

    router_decision: List[str] | None
    thinking_logs: Annotated[List[str], operator.add] | None

    # Context trung gian (nơi các Expert đổ dữ liệu về)
    text_context: Optional[str] | None
    file_context: str | None

    # Các trường thông tin mà Tech Support Agent cần chẩn đoán
    diagnosis: str | None
    case_type: str | None
    solution: str | None
    final_answer: str | None