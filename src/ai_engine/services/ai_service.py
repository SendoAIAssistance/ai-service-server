# Core AI logic: Process message -> Call Orchestra
import logging
import asyncio
from typing import AsyncGenerator, Optional, Union

from fastapi import UploadFile

from ai_engine.schemas.ai_schema import UserMessage

from ai_engine.services.agents.orchestra import Orchestra
from ai_engine.schemas.ai_schema import UserMessage, AIResponse

logger_service = logging.getLogger('ai_service.service.ai_service')

class AIService:
    def __init__(self):
        self.orchestra = Orchestra()

    async def process_message(self, message: str, file: Optional[Union[UploadFile, str]]) -> AIResponse:
        logger_service.info(f"Khởi động Orchestra xử lý message: {message}")

        # TODO: Tiền xử lý file tại đây
        file_data = None

        if file and hasattr(file, "filename") and file.filename:
            try:
                # Đảm bảo con trỏ file ở vị trí đầu tiên
                await file.seek(0)
                file_data = await file.read()
                logger_service.info(f"✅ Đã nạp file thành công: {file.filename} ({len(file_data)} bytes)")
            except Exception as e:
                logger_service.error(f"❌ Lỗi khi đọc file: {str(e)}")
        else:
            logger_service.info("ℹ️ Request không kèm file hoặc file rỗng.")

        # TRUYỀN VÀO ORCHESTRA
        # Nhớ check xem bên Orchestra hàm dispatch có nhận tham số file_data chưa nhé
        result = await self.orchestra.dispatch(message=message, file_data=file_data)
        return result