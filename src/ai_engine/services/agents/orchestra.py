# src/ai_engine/services/agents/orchestra.py
import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Optional

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END

from ai_engine.services.agents.state import AgentState
from ai_engine.schemas.ai_schema import AIResponse
from ai_engine.services.agents.experts.table_expert import TableExpert
from ai_engine.services.agents.experts.dynamic_router.dr_floor_1 import Floor1Router
from ai_engine.services.database.mongo_manager import MongoDBVectorManager
from ai_engine.schemas.chat_schema import StreamEvent, MessageStatus

orchestra_logger = logging.getLogger("ai_engine.orchestra")

system_prompt = """
    You are a precise, highly logical reasoning AI. Your primary directive is accuracy and efficiency. You MUST strictly adhere to the following rules:

1. FAIL-FAST ON MISSING DATA: If the user's prompt requires real-time information, current events, live web data, or facts strictly outside your training knowledge, DO NOT attempt to reason, guess, or extrapolate. Terminate your reasoning process immediately.
2. ZERO HALLUCINATION: If you lack the definitive factual basis to solve a problem or answer a question, you must admit ignorance. Never invent facts, data, URLs, or statistics to complete your logic.
3. NO ENDLESS LOOPS: Do not overthink. If your internal reasoning cannot find a solid factual foundation after the first few logical steps, abort the process. Do not go into circles trying to deduce unavailable information.
4. EXACT FALLBACK RESPONSE: When aborting due to lack of real-time data or knowledge, stop all reasoning and output exactly this response in Vietnamese: "Tôi không có đủ dữ liệu thực tế hoặc thông tin cập nhật để trả lời chính xác câu hỏi này." Do not apologize or offer speculative advice.
"""

class Orchestra:
    def __init__(self):
        __basic_agent = ChatOllama(
            model="qwen3-vl:4b",
            temperature=0.1,
            reasoning=True,
        )
        __memory = InMemorySaver()
        self.agent = create_agent(
            model=__basic_agent,
            tools=[],
            checkpointer=__memory,
            middleware=[]
        )

        orchestra_logger.info("🎻 Orchestra initialized!")

    async def stream_dispatch(
            self,
            conversationId: str,
            message: str,
            file_data: Optional[bytes] = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        config = {
            "configurable": {
                "thread_id": conversationId
            }
        }
        orchestra_logger.info(f"Processing message: {message}")
        orchestra_logger.info(f"Calling Agent {self.agent.name}")
        input_message = [SystemMessage(content=system_prompt),
                         HumanMessage(content=message)]
        try:
            async for token, metadata in self.agent.astream(
                input={"messages": input_message},
                stream_mode="messages",
                config=config,
            ):
                type_ = token.content_blocks[-1]["type"]
                print(type_)
                orchestra_logger.error(f"Received message: {token.content_blocks}")
                yield StreamEvent(
                    type=type_,
                    content=token.content_blocks[-1][type_],
                )
        except Exception as e:
            raise e
            orchestra_logger.error(e)
            yield StreamEvent(
                type="error",
                content=str(e),
                status=MessageStatus.ERROR
            )
        finally:
            yield StreamEvent(
                type="done",
                content="END",
                status=MessageStatus.COMPLETED
            )
        # thinking_list = [
        #     f"Nhận conversation: {conversationId}",
        #     f"Message: {message[:80]}...",
        #     f"Đang phân tích bằng placeholder..."
        # ]
        # for thinking in thinking_list:
        #     for i in range(0, len(thinking), 5):
        #         chunk = thinking[i:i + 5]
        #         yield StreamEvent(type="thinking", content=chunk)
        #         await asyncio.sleep(0.03)
        #
        # response_text = f"Khôi không ngu! Khôi biết training AI!"
        # for i in range(0, len(response_text), 5):
        #     chunk = response_text[i:i + 5]
        #     yield StreamEvent(type="chunk", content=chunk)
        #     await asyncio.sleep(0.03)
        #
        # yield StreamEvent(type="done", content="", status=MessageStatus.COMPLETED)
        # return

    # async def dispatch(
    #         self,
    #         conversation_id: str,
    #         message: str,
    #         file_data: Optional[bytes] = None
    # ) -> AIResponse:
    #     """
    #     Hàm khởi động
    #     1. Nhận input từ AI Service.
    #     2. Đẩy vào LangGraph để chạy song song.
    #     3. Gom kết quả trả về cho Backend.
    #     """
    #     # ==================== PLACEHOLDER CHO TEST ====================
    #     # if True:  # ← đổi thành False khi muốn chạy graph thật
    #     return AIResponse(
    #         thinking=f"📨 Conversation: {conversation_id}\n"
    #                  f"💬 Message: {message[:100]}{'...' if len(message) > 100 else ''}\n"
    #                  f"📎 File: {'Có (' + str(len(file_data)) + ' bytes)' if file_data else 'Không'}\n"
    #                  f"🧠 Đang phân tích (placeholder mode)...",
    #         response=f"✅ Nhận được yêu cầu của bạn!\n\n"
    #                  f"Message: {message}\n"
    #                  f"File đính kèm: {'Có' if file_data else 'Không'}\n\n"
    #                  f"Tôi bị ngu."
    #     )
    #     # ============================================================
    #     # try:
    #     #     orchestra_logger.info("--- Orchestra Starting ---")
    #     #     # 1. Khởi tạo State
    #     #     # TODO:  Input should be a valid list [type=list_type, input_value='Fuck u', input_type=str]
    #     #     inputs = AgentState(
    #     #         message=message,
    #     #         file_data=file_data,
    #     #         text_context="",
    #     #         file_type="",
    #     #     )
    #     #     # inputs = {
    #     #     #     "message": [message],
    #     #     #     "file_data": file_data,
    #     #     #     "text_context": "",
    #     #     #     "file_context": ""
    #     #     # }
    #     #
    #     #     # 2. Thực thi Graph
    #     #     result = await self.app.ainvoke(inputs)
    #     #
    #     #     return AIResponse(
    #     #         response=result.get("final_answer", "Xin lỗi, mình gặp chút vấn đề khi xử lý yêu cầu.")
    #     #     )
    #     # except Exception as e:
    #     #     orchestra_logger.error(f"❌ Lỗi nghiêm trọng tại Orchestra: {str(e)}", exc_info=True)
    #     #     return AIResponse(
    #     #         thinking="Hi",
    #     #         response=str(e)
    #     #     )
    #
    # async def dr_floor_1(self, state: AgentState):
    #     """
    #     Gọi AI LOCAL để quyết định luồng chạy
    #     """
    #     orchestra_logger.info("🛠 Router: Phân loại dữ liệu...")
    #     # TODO: Logic lọc loại file cơ bản
    #     result = await self.floor1_router_expert.categorize(state)
    #
    #     decision = result.get("decision", ["text_expert"])
    #     reasoning = result.get("reasoning", "No reasoning provided")
    #
    #     orchestra_logger.info(f"🎯 AI Decision: {decision} | Lý do: {reasoning}")
    #
    #
    #     return {
    #         "router_decision": decision,
    #         "thinking_log": [f"Router: Kích hoạt {decision} vì {reasoning}"]
    #     }
    #
    # async def balancer_decision(self, state: AgentState):
    #     """
    #     LangGraph cho phép trả về một list các node để chạy song song.
    #     Nếu list rỗng, mình bắt nó nhảy tới aggregator luôn.
    #     """
    #     decision = state.get("router_decision", [])
    #     if not decision:
    #         return "aggregator"
    #
    #     valid_nodes = ["table_expert", "text_expert", "aggregator"]
    #     final_path = [d for d in decision if d in valid_nodes]
    #
    #     return final_path if final_path else "aggregator"
    #
    # async def process_text(self, state: AgentState):
    #     orchestra_logger.info("📝 Calling Text Expert: Đang phân tích yêu cầu...")
    #     # TODO: PHân tích "Địt mẹ lỗi rồi"
    #     return {"text_context": "Người dùng báo lỗi đồng bộ dữ liệu."}
    #
    # async def process_table(self, state: AgentState):
    #     if not state.get("file_data"):
    #         return {"thinking_logs": ["Expert Table: Không có file, bỏ qua bước này."]}
    #     orchestra_logger.info("📊 Calling Table Expert: Đang đọc dữ liệu bảng...")
    #     result = await self.table_expert.analyze(state["file_data"])
    #     return result
    #
    # async def aggregator_and_respond(self, state: AgentState):
    #     orchestra_logger.info("🤖 Aggregator: Đang tổng hợp Context...")
    #     # Lấy text_context + file_context để ra chẩn đoán cuối
    #     return {
    #         "diagnosis": f"Lỗi ID #123 dựa trên: {state['text_context']}",
    #         "case_type": "Transaction Error",
    #         "solution": "Kiểm tra lại gateway Senpay",
    #         "final_answer": "Case này do ID #123 bị treo, để mình báo team dev fix."
    #     }