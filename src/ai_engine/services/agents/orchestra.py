# src/ai_engine/services/agents/orchestra.py
import logging
from typing import Optional

from langgraph.graph import StateGraph, END

from ai_engine.services.agents.state import AgentState
from ai_engine.schemas.ai_schema import AIResponse

orchestra_logger = logging.getLogger("ai_engine.orchestra")

class Orchestra:
    def __init__(self):
        workflow = StateGraph(AgentState)

        # Định nghĩa các Node
        workflow.add_node("router", self.route_input)
        workflow.add_node("text_expert", self.process_text)
        workflow.add_node("table_expert", self.process_table)
        workflow.add_node("aggregator", self.aggregator_and_respond)

        # Chạy song song text và image cùng lúc!
        workflow.set_entry_point("router")

        # Router quyết định có chạy song song hay không
        workflow.add_edge("router", "text_expert")
        workflow.add_edge("router", "table_expert")

        # Đổ context về Aggregator
        workflow.add_edge("text_expert", "aggregator")
        workflow.add_edge("table_expert", "aggregator")

        workflow.add_edge("aggregator", END)
        self.app = workflow.compile()
        orchestra_logger.info("🎻 Orchestra initialized!")

    async def route_input(self, state: AgentState):
        orchestra_logger.info("🛠 Router: Phân loại dữ liệu...")
        # TODO: Logic lọc loại file cơ bản
        return {"file_type": "table" if state.get("file_data") else "None"}

    async def process_text(self, state: AgentState):
        orchestra_logger.info("📝 Text Expert: Đang phân tích yêu cầu...")
        # TODO: PHân tích "Địt mẹ lỗi rồi"
        return {"text_context": "Người dùng báo lỗi đồng bộ dữ liệu."}

    async def process_table(self, state: AgentState):
        if not state.get("file_data"):
            return {"file_context": "Không có file bảng."}
        orchestra_logger.info("📊 Table Expert: Đang đọc dữ liệu bảng...")
        # TODO: dùng Pandas hoặc Polars để xử lý file_data ở đây
        return {"file_content": "Phát hiện dòng log ID #123 có status 500."}

    async def aggregator_and_respond(self, state: AgentState):
        orchestra_logger.info("🤖 Aggregator: Đang tổng hợp Context...")
        # Lấy text_context + file_context để ra chẩn đoán cuối
        return {
            "diagnosis": f"Lỗi ID #123 dựa trên: {state['text_context']}",
            "case_type": "Transaction Error",
            "solution": "Kiểm tra lại gateway Senpay",
            "final_answer": "Case này do ID #123 bị treo, để mình báo team dev fix."
        }

    async def dispatch(self, message: str, file_data: Optional[bytes] = None) -> AIResponse:
        """
        Hàm khởi động
        1. Nhận input từ AI Service.
        2. Đẩy vào LangGraph để chạy song song.
        3. Gom kết quả trả về cho Backend.
        """
        try:
            orchestra_logger.info("--- Orchestra Starting ---")

            # 1. Khởi tạo State
            inputs = {
                "message": [message],
                "file_data": file_data,
                "text_context": "",
                "file_context": ""
            }

            # 2. Thực thi Graph
            result = await self.app.ainvoke(inputs)

            return AIResponse(
                diagnosis=result.get("diagnosis", "Không tìm thấy lỗi cụ thể."),
                case_type=result.get("case_type", "General Support"),
                solution=result.get("solution", "Vui lòng liên hệ bộ phận kỹ thuật để biết thêm chi tiết."),
                response=result.get("final_answer", "Xin lỗi, mình gặp chút vấn đề khi xử lý yêu cầu.")
            )
        except Exception as e:
            orchestra_logger.error(f"❌ Lỗi nghiêm trọng tại Orchestra: {str(e)}", exc_info=True)
            return AIResponse(
                diagnosis="System Crash",
                case_type="Error",
                solution="Restart Service",
                response=str(e)
            )