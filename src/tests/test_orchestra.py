import pytest
from unittest.mock import MagicMock, patch

from langsmith import expect

from ai_engine.schemas.ai_schema import AIResponse
from ai_engine.config import console

from ai_engine.agents.orchestra import Orchestra

@pytest.fixture
def mock_dependencies():
    """
    Fixture này dùng để mock các thành phần nặng:
    1. tools (để không cần phải load file yaml)
    2. ChatOllama (để không cần bật server Ollama)
    3. create_openapi_agent (để không cần phải tạo agent thật)
    """
    with patch('ai_engine.agents.orchestra.tools') as mock_tools,\
         patch('ai_engine.agents.orchestra.ChatOllama') as mock_llm,\
         patch('ai_engine.agents.orchestra.planner') as mock_planner:

        # Setup giả lập cho tools
        mock_tools.api_spec = "mock_spec"
        mock_tools.requests_wrapper = "mock_wrapper"

        # Setup giả lập cho agent
        mock_agent_instance = MagicMock()
        mock_planner.create_openapi_agent.return_value = mock_agent_instance

        yield {
            "agent": mock_agent_instance,
            "tools": mock_tools,
            "llm": mock_llm,
            "planner": mock_planner,
        }

class TestOrchestra:
    def test_init(self, mock_dependencies):
        """Test xem class có khởi tạo thành công không"""
        orchestra = Orchestra()

        # Kiểm tra xem agent đã được tạo chưa
        assert orchestra.agent is not None

        # Kiểm tra xem có gọi create_openapi_agent đúng tham số mock không
        # (Đây là cách kiểm tra xem logic ghép nối components có đúng không)
        mock_dependencies["planner"].create_openapi_agent.assert_called()

    @pytest.mark.asyncio
    async def test_dispatch_success(self, mock_dependencies):
        """Test luồng chạy chính của hàm dispatch"""
        orchestra = Orchestra()
        mock_agent = mock_dependencies["agent"]

        # Giả lập kết quả trả về từ agent của Langchain
        expected_agent_response = {
            "output": "Đã tìm thấy thông tin sản phẩm"
        }
        mock_agent.invoke.return_value = expected_agent_response

        user_message = "Tìm cho tôi Iphone 15"
        result = await orchestra.dispatch(user_message)

        assert isinstance(result, AIResponse)

        mock_agent.invoke.assert_called_once_with(user_message)
