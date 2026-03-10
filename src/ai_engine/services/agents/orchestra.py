# src/ai_engine/services/agents/orchestra.py
import logging
import re
from collections.abc import AsyncGenerator
from typing import Optional, Literal

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from ai_engine.schemas.chat_schema import StreamEvent, MessageStatus
from ai_engine.services.database.mongo_manager import MongoDBVectorManager  # ← Import class bạn đã có

orchestra_logger = logging.getLogger("ai_engine.orchestra")

# === SYSTEM PROMPT CƠ BẢN (giữ nguyên) ===
BASE_SYSTEM_PROMPT = """
# HƯỚNG DẪN HỆ THỐNG: CHUYÊN VIÊN HỖ TRỢ KỸ THUẬT SENDO FARM (GROCERY)

VAI TRÒ: 
Bạn là hệ thống Trợ lý Kỹ thuật chuyên trách quản lý và hỗ trợ vận hành đơn hàng Sendo Farm (Online Grocery). 

NGUYÊN TẮC PHẢN HỒI:
1. Tính chuyên nghiệp: Sử dụng ngôn từ chuẩn mực, khách quan. Tuyệt đối không sử dụng từ ngữ suồng sã, giễu cợt hoặc biểu tượng cảm xúc.
2. Tính chính xác: Trả lời dựa trên dữ liệu thực tế từ hệ thống (Export 25-02-2026). Nếu thông tin không tồn tại, yêu cầu người dùng cung cấp thêm mã định danh.
3. Cấu trúc: Sử dụng danh sách liệt kê và bảng biểu để tối ưu hóa việc tra cứu thông tin.

---

I. THÔNG TIN NỀN TẢNG VÀ VẬN HÀNH
- Phạm vi quản lý: Hệ thống Sendo Farm / Online Grocery (Store ID: 929107).
- Đơn vị vận chuyển: SENDO STATION DELIVERY (Mã: ecom_shipping_stationdelivery).
- Cổng thanh toán: Senpay (Mặc định).
- Trung tâm điều phối: Kho Logistics HNT Nguyên Khê (Đông Anh, Hà Nội).

---

II. QUY ĐỊNH VỀ TRƯỜNG DỮ LIỆU (DATA MAPPING)
Khi truy vấn, hệ thống phải đối chiếu chính xác các nhóm thông tin sau:

- Nhóm Định danh: Mã đơn hàng, Id, Mã vận đơn.
- Nhóm Trạng thái: Trạng thái đơn hàng, Trạng thái vận chuyển, Trạng thái thanh toán.
- Nhóm Thông tin khách: Họ tên người nhận, Số điện thoại, Địa chỉ chi tiết.
- Nhóm Tài chính: Tổng thanh toán, Voucher, Chiết khấu, Phương thức thanh toán.
- Nhóm Chỉ số sự cố: Đơn hàng xấu (Bad Order), Đang khiếu nại, Đang có sự cố, Lý do hủy.

---

III. QUY TRÌNH XỬ LÝ ĐƠN HÀNG TIÊU CHUẨN (SOP)
1. Tiếp nhận: Hệ thống ghi nhận đơn hàng mới.
2. Xác nhận: Kho kiểm tra tồn kho và xác nhận tình trạng hàng hóa.
3. Điều phối: Khởi tạo vận đơn, chuyển thông tin tới Sendo Station.
4. Xử lý tại kho: Phân loại (Sorting) và đóng gói tại kho Nguyên Khê.
5. Vận chuyển: Shipper thực hiện giao hàng tới địa chỉ người nhận.
6. Hoàn tất: Xác nhận giao hàng thành công và thực hiện đối soát tài chính.

---

IV. TIÊU CHUẨN ĐƠN HÀNG THÀNH CÔNG (HAPPY ORDER)
Đơn hàng được phân loại là "Happy Order" khi đáp ứng đủ 05 tiêu chí:
1. Trạng thái: Hoàn tất đơn hàng hoặc Đã xác nhận (Đang trong tiến độ giao hàng).
2. Tài chính: Đã thanh toán qua Senpay/Cổng thanh toán.
3. An toàn: Đơn hàng xấu = False.
4. Khiếu nại: Không ghi nhận khiếu nại hoặc sự cố kỹ thuật.
5. Logistics: Có thông tin Mã vận đơn hợp lệ trên hệ thống.

---

V. GIAO THỨC HỖ TRỢ VÀ XỬ LÝ SỰ CỐ

1. Xử lý Đơn hàng bị hủy:
- Hành động: Kiểm tra cột Lý do hủy.
- Hướng xử lý: 
  + Nếu do lỗi thanh toán: Hướng dẫn khách hàng kiểm tra ví Senpay hoặc thực hiện lại giao dịch.
  + Nếu do lỗi hệ thống (CBB): Chuyển tiếp (Escalate) cho bộ phận Kỹ thuật kiểm tra Log.

2. Xử lý Đơn hàng xấu (Bad Order = True):
- Hành động: Cảnh báo ngay lập tức cho bộ phận Vận hành. Đây là các đơn hàng có nguy cơ lỗi dữ liệu hoặc rủi ro vận chuyển cao.

3. Tra cứu tiến độ giao hàng:
- Thời gian chuẩn: T+1 kể từ thời điểm đặt hàng thành công.
- Kiểm tra: Nếu đơn hàng quá 24h chưa có Mã vận đơn, yêu cầu bộ phận Điều phối kho kiểm tra trạng thái xác nhận hàng.

---

VI. QUY ĐỊNH PHÁT NGÔN (OUTPUT FORMAT)
- Trả lời trực diện vào vấn đề, không giải thích vòng vo.
- Luôn kết thúc bằng yêu cầu xác nhận hoặc hướng dẫn bước tiếp theo rõ ràng.
- Ví dụ: "Đơn hàng [Mã ID] hiện đang ở trạng thái 'Đang có sự cố'. Lý do: Lỗi phân loại tại kho Nguyên Khê. Đã chuyển thông tin cho bộ phận Logistics xử lý. Cần hỗ trợ thêm thông tin nào khác không?"
"""

# Prompt cho classifier
CLASSIFIER_PROMPT = """
Bạn là intent classifier cho hệ thống hỗ trợ kỹ thuật.
Phân loại query của user thành đúng MỘT trong các loại sau:

- small_talk: chào hỏi, chửi bới, troll, nói chuyện phiếm, xúc phạm, hỏi linh tinh, hỏi thăm, đùa giỡn.
- technical: liên quan đến lỗi hệ thống, lỗi đơn hàng, kiểm tra đơn hàng, tra cứu trạng thái đơn, lịch sử đơn, mã đơn hàng, bug, crash, không hoạt động...

Chỉ trả lời đúng một từ: small_talk hoặc technical. Không giải thích gì thêm.

Query: 
"""

class Orchestra:
    def __init__(self):
        self.memory = InMemorySaver()

        # Khởi tạo Vector DB Manager (chỉ load 1 lần khi init)
        self.vector_manager = MongoDBVectorManager(
            db_name="AI_Assistance",
            collection_name="AI_Service",
            embed_model="qwen3-embedding:0.6b",
        )
        orchestra_logger.info("🔍 Vector DB Manager initialized")

        # Classifier (nhanh, nhiệt độ 0)
        self.classifier = ChatOllama(
            model="llama3.1:latest",
            temperature=0.0,
        )

        # Basic agent - cho small talk
        self.basic_agent = create_agent(
            model=ChatOllama(model="llama3.1:latest", temperature=0.7),
            checkpointer=self.memory,
        )

        # Reasoning agent - sẽ được augment prompt động (có RAG)
        self.reasoning_agent = create_agent(
            model=ChatOllama(model="qwen3.5:latest", temperature=0.1, reasoning=True),
            checkpointer=self.memory,
        )

        orchestra_logger.info("🎻 Orchestra initialized with Vector RAG!")

    @staticmethod
    def is_greeting(text: str) -> bool:
        greetings = r"^(hi|hello|chào|helo|ê|hey|xin chào|bonjour|sup|yo)"
        return bool(re.search(greetings, text.lower().strip()))

    async def classify_intent(self, message: str) -> Literal["small_talk", "technical"]:
        try:
            prompt = [SystemMessage(content=CLASSIFIER_PROMPT), HumanMessage(content=message)]
            response = await self.classifier.ainvoke(prompt)
            intent = response.content.strip().lower()
            return "technical" if "technical" in intent else "small_talk"
        except Exception as e:
            orchestra_logger.warning(f"Classifier fallback: {e}")
            return "small_talk"

    async def _retrieve_rag_context(self, query: str, top_k: int = 5) -> str:
        """
        Query vector DB để lấy top-k case tương tự nhất
        Trả về chuỗi context để nhồi vào prompt
        """
        try:
            results = self.vector_manager.similarity_search(
                query=query,
                limit=top_k,
                # index_name="vector_index",
            )

            if not results:
                return ""

            context_parts = []
            for i, res in enumerate(results, 1):
                case_id = res["metadata"].get("case_id", "N/A")
                score = res["score"]
                text = res["text"]
                context_parts.append(
                    f"[Case {i}] (score: {score:.3f}) - ID: {case_id}\n"
                    f"{text}\n"
                    f"{'-' * 60}"
                )

            return "\n\n".join(context_parts)
        except Exception as e:
            orchestra_logger.error(f"RAG retrieval error: {e}")
            return ""

    async def stream_dispatch(
            self,
            conversationId: str,
            message: str,
            file_data: Optional[bytes] = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        config = {"configurable": {"thread_id": conversationId}}
        orchestra_logger.info(f"Processing: {message[:80]}...")
        # Yield ngay status PENDING để frontend biết đang xử lý
        yield StreamEvent(
            type="reasoning",
            content="Lựa chọn mô hình...",
            status=MessageStatus.IN_PROGRESS
        )
        # === PHÂN LOẠI Ý ĐỊNH ===
        if self.is_greeting(message):
            intent = "small_talk"
        else:
            intent = await self.classify_intent(message)

        if intent == "small_talk":
            agent = self.basic_agent
            current_prompt = "Bạn là trợ lý AI thân thiện, dí dóm, trả lời ngắn gọn và vui vẻ bằng tiếng Việt. Với câu chửi hoặc troll thì đáp dí dóm nhưng vẫn lịch sự. Không dùng tool."
            orchestra_logger.info("→ SMALL TALK → basic_agent")
        else:
            # TECHNICAL → LẤY RAG CONTEXT TRƯỚC
            yield StreamEvent(
                type="reasoning",
                content="Đang tra cứu kiến thức liên quan...",
                status=MessageStatus.IN_PROGRESS
            )
            rag_context = await self._retrieve_rag_context(message, top_k=5)

            # Augment prompt động: thêm RAG context vào system prompt
            current_prompt = BASE_SYSTEM_PROMPT
            if rag_context:
                current_prompt += "\n\n=== KIẾN THỨC TƯƠNG TỰ TỪ CÁC CASE TRƯỚC ===\n" + rag_context + "\n\nDựa vào các case trên để trả lời chính xác, trích dẫn case nếu phù hợp."

            agent = self.reasoning_agent
            yield StreamEvent(type="reasoning",content="→ TECHNICAL QUERY → reasoning_agent (with RAG)")

        input_message = [SystemMessage(content=current_prompt), HumanMessage(content=message)]
        # Yield thêm status trước khi vào agent stream
        yield StreamEvent(
            type="reasoning",
            content="Đang suy nghĩ và xử lý...",
            status=MessageStatus.IN_PROGRESS
        )
        try:
            async for token, metadata in agent.astream(
                input={"messages": input_message},
                stream_mode="messages",
                config=config,
            ):
                if token.content_blocks:
                    block = token.content_blocks[-1]
                    print(block)
                    type_ = block["type"]

                    if type_ == "tool_call_chunk":
                        func_name = block.get("name", "")
                        args = block.get("args", "")
                        content = f"Called function: {func_name}. Args: {args}"
                        yield StreamEvent(type="reasoning", content=content)
                    else:
                        yield StreamEvent(
                            type=type_,
                            content=block.get(type_, "")
                        )
        except Exception as e:
            orchestra_logger.error(f"Error: {e}")
            yield StreamEvent(
                type="error",
                content="Có lỗi xảy ra khi xử lý yêu cầu.",
                status=MessageStatus.ERROR
            )
        finally:
            yield StreamEvent(
                type="done",
                content="END",
                status=MessageStatus.COMPLETED
            )

    def reset_conversation(self, conversationId: str):
        orchestra_logger.info(f"Resetting conversation {conversationId}")
        self.memory.delete_thread(conversationId)