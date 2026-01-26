# Config: Model (Llama), paths, API keys
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tech Support Agent"
    OLLAMA_HOST: str | None = None
    TOOLS_YAML_PATH: str | None = None

    MONGODB_ATLAS_URI: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

if __name__ == "__main__":
    print(settings.MONGODB_ATLAS_URI)