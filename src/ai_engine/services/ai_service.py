# Core AI logic: Process message -> Call Orchestra
import logging
import asyncio
from typing import AsyncGenerator, Optional, Union

from fastapi import UploadFile

from ai_engine.schemas.chat_schema import UserMessage, StreamEvent, MessageStatus

from ai_engine.services.agents.orchestra import Orchestra
from ai_engine.schemas.ai_schema import AIResponse

logger_service = logging.getLogger('ai_service.service.ai_service')

class AIService:
    def __init__(self):
        self.orchestra = Orchestra()

    async def _read_file(self, file: UploadFile) -> Optional[bytes]:
        if file and file.filename:
            await file.seek(0)
            return await file.read()
        return None

    async def stream_message(
            self,
            conversation_id: str,
            message: str,
            file: Optional[Union[UploadFile, str]]
    ) -> AsyncGenerator[str, None]:
        """Hàm stream thay vì return 1 lần"""
        async for event in self.orchestra.stream_dispatch(
                conversationId=conversation_id,
                usr_message=message,
                file_data=await self._read_file(file) if file else None
        ):
            yield f"data: {event.model_dump_json()}\n\n"