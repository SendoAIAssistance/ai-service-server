import json
import logging
import re
from langchain_ollama import OllamaLLM
from starlette.routing import Router

from ai_engine.services.agents.state import AgentState

dr_logger = logging.getLogger('ai_engine.experts.router.router_floor_1')

class Floor1Router:
    def __init__(self):
        self.llm = OllamaLLM(
            model="sendo-dynamic_router-f1",
            format="json",
            temperature=0
        )

    def extract_json(self, text: str) -> dict:
        """
        Hàm bóc tách JSON từ chuỗi văn bản bất kỳ của LLM
        """
        try:
            # Tìm nội dung nằm giữa { và }
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return None
        except Exception:
            return None

    async def categorize(self, state: AgentState):
        message = state["message"]
        has_file = "YES" if state.get("file_data") else "NO"

        # Input cho model
        input_text = f"Message: {message} | File: {has_file}"

        try:
            response = await self.llm.ainvoke(input_text)
            # AI Debug
            dr_logger.info(f"🔍 Raw AI Response: {response}")

            data = self.extract_json(response)
            if data: return data
            raise dr_logger.error("Không tìm thấy JSON hợp lệ trong response")
        except Exception as e:
            dr_logger.info(f"❌ Lỗi Router Floor 1: {str(e)}")
            return {
                "decision": "TEXT",
                "reasoning": "Fallback to text expert"
            }