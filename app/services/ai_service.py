# Core AI logic: Process message -> Call Orchestra
from app.schemas.ai_schema import UserMessage, AIResponse
from app.agents.orchestra import Orchestra

class AIService:
    def __init__(self):
        self.orchestra = Orchestra()

    async def process_message(self, request: UserMessage) -> AIResponse:
        # Logic gọi Agent Orchestra tại đây
        result = await self.orchestra.dispatch(request.message)
        return result
