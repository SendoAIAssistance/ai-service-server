import pytest
from langchain_core.runnables import RunnableBinding
from ai_engine.agents.orchestra import Orchestra
from ai_engine.config import console


# def test_orchestra_llm_has_tools_bound():
#     """
#     Test case: Check Orchestra.llm got tools_bind or not
#     """
#     orch = Orchestra()
#
#     # Type check
#     assert isinstance(orch.llm, RunnableBinding)
#
#     # Datacheck (kwargs)
#     bound_kwargs = orch.llm.kwargs
#
#     assert "tools" in bound_kwargs, \
#             "❌ LỖI: Không tìm thấy tham số 'tools' trong kwargs của model"
#
#     tools = bound_kwargs["tools"]
#
#     # Check number of tools
#     assert len(tools) > 0, "❌ LỖI: Danh sách tools bị rỗng"
#
#     # (Optional) Print to debug if needed
#     console.print(f"\n✅ PASS: Tìm thấy {len(tools)} tools đã được bind thành công.")

def test_orchestra_dispatch_structure():
    """
    Fast check if dispatch structure works
    """
    orch = Orchestra()
    assert orch.analyze_chain is not None
