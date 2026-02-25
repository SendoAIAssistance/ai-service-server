from typing import TypedDict, Annotated, List, Optional
import operator

class AgentState(TypedDict):
    message: Annotated[List[str], operator.add]
    file_data: Optional[bytes]
    file_type: Optional[str] # "table", "image", "text", "None"

    # Context trung gian (nơi các Expert đổ dữ liệu về)
    text_context: str
    file_context: str

    # Các trường thông tin mà Tech Support Agent cần chẩn đoán
    diagnosis: str
    case_type: str
    solution: str
    final_answer: str