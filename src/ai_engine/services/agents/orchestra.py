# src/ai_engine/services/agents/orchestra.py
import logging
import re
import time
from collections.abc import AsyncGenerator
from typing import Optional, Literal

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from ai_engine.schemas.chat_schema import StreamEvent, MessageStatus
from ai_engine.services.database.mongo_manager import MongoDBVectorManager  # ← Import class bạn đã có

orchestra_logger = logging.getLogger("ai_engine.orchestra")

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
            model="tech_support_classifier_model:latest",
            temperature=0.0,
        )

        # Basic agent - cho small talk
        self.basic_agent = create_agent(
            model=ChatOllama(model="tech_support_basic_model:latest"),
            checkpointer=self.memory,
        )

        # Reasoning agent - sẽ được augment prompt động (có RAG)
        self.reasoning_agent = create_agent(
            model=ChatOllama(model="tech_support_order_expert:latest", temperature=0.1, reasoning=True),
            checkpointer=self.memory,
        )

        orchestra_logger.info("🎻 Orchestra initialized with Vector RAG!")

    async def manage_ollama_memory(self, model_name: str, keep_alive: str):
        """
        keep_alive: "0" (unload ngay), "-1" (giữ mãi mãi), hoặc "5m", "10m"...
        """
        try:
            from langchain_ollama import ChatOllama
            # Gọi dummy để set keep_alive
            temp_llm = ChatOllama(model=model_name, keep_alive=keep_alive)
            await temp_llm.ainvoke(" ")
        except Exception:
            pass

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
                # case_id = res["metadata"].get("case_id", "N/A")
                # score = res["score"]
                text = res["text"]
                context_parts.append(
                    # f"[Case {i}] (score: {score:.3f}) - ID: {case_id}\n"
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
            usr_message: str,
            file_data: Optional[bytes] = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        config = {
            "configurable": {"thread_id": conversationId}
        }
        orchestra_logger.info(f"Processing: {usr_message[:80]}...")
        # Yield ngay status PENDING để frontend biết đang xử lý
        yield StreamEvent(
            type="reasoning",
            content="Planning...",
            status=MessageStatus.IN_PROGRESS
        )

        input_intent = [HumanMessage(content=usr_message)]
        classifier_agent = create_agent(
            model=self.classifier,
        )
        intent = classifier_agent.invoke(input={"messages": input_intent})["messages"][1].content

        if intent == "small_talk":
            agent = self.basic_agent
            orchestra_logger.info("→ SMALL TALK → basic_agent")
        else:
            # TECHNICAL → LẤY RAG CONTEXT TRƯỚC
            yield StreamEvent(
                type="reasoning",
                content="Đang kiểm tra kiến thức đã học...",
                status=MessageStatus.IN_PROGRESS
            )
            try:
                rag_context = await self._retrieve_rag_context(usr_message, top_k=5)
            except:
                rag_context = ""
            # Augment prompt động: thêm RAG context vào system prompt
            if rag_context:
                usr_message +="\n\n=== KIẾN THỨC TRUY VẤN ===\n" + rag_context

            agent = self.reasoning_agent

        # Yield thêm status trước khi vào agent stream
        yield StreamEvent(
            type="reasoning",
            content="Đang suy nghĩ và xử lý...",
            status=MessageStatus.IN_PROGRESS
        )

        try:
            async for token, metadata in agent.astream(
                input={"messages": usr_message},
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