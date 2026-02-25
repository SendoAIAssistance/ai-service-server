# Tools loader: Load OpenAPI tools từ YAML
import yaml
import requests
from langchain_community.utilities import RequestsWrapper
from sqlalchemy.dialects.postgresql import JSONB

from ai_engine.core.config import console, settings
from langchain_core.tools import tool
from langchain_community.agent_toolkits.openapi import toolkit
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.tools.json.tool import JsonSpec

import json

# If needed, reduce the spec to only relevant endpoints
# def get_api_spec(url="https://localhost:8000/openapi.json"):
#     response = requests.get(url)
#     raw_spec = response.json()
#     return reduce_openapi_spec(raw_spec)

def get_api_header():
    return {"Authorization": f"Bearer"}

class Tools:
    def __init__(self):
        super().__init__()
        # self.dynamic_tools = self.create_dynamic_tools()
        self.api_spec = self.load_api_spec()

        self.requests_wrapper = RequestsWrapper(headers=get_api_header())

    def load_api_spec(self, path: str = settings.TOOLS_YAML_PATH):
        with open(path, 'r', encoding="utf-8") as f:
            return reduce_openapi_spec(yaml.load(f, Loader=yaml.Loader))


    # def create_dynamic_tools(self, path: str = settings.TOOLS_YAML_PATH):
    #     spec = self.load_api_spec(path)
    #
    #     # RequestsWrapper is the "browser" helping AI GET/POST
    #     requests_wrapper = RequestsWrapper(
    #         headers={
    #             "Authorization": "Bearer ..."
    #         }
    #     )
    #
    #     # Magical happens here: Turn JSON to Tools
    #     # This toolkit will contain tools
    #     api_toolkit = toolkit.OpenAPIToolkit.from_llm(
    #         json_spec=spec,
    #         requests_wrapper=requests_wrapper,
    #         llm=None
    #     )
    #     return api_toolkit.get_tools()

tools = Tools()