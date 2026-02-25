from ai_engine.services.ai_service import AIService

# Khởi tạo 1 instance duy nhất (Singleton) hoặc tạo mới mỗi lần tùy nhu cầu
_AI_SERVICE = AIService()
# Ở đây tạo hàm FastAPI inject vào router
def get_ai_service() -> AIService:
    """
    Dependencies cung cấp instance của AIService cho các routes.
    Sau này nếu cần truyền DB hay LLM vào Service, ta sẽ sửa ở đây.
    """
    return _AI_SERVICE