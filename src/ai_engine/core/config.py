# Config: Model (Llama), paths, API keys
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from pathlib import Path

CURRENT_CONFIG_FILE_PATH = Path(__file__).resolve() # config.py
PROJECT_ROOT = CURRENT_CONFIG_FILE_PATH.parent.parent # src
load_dotenv(Path(PROJECT_ROOT) / ".env")
console = Console()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tech Support Agent"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    OLLAMA_HOST: str | None = None
    PROJECT_ROOT: Path = PROJECT_ROOT
    MONGODB_ATLAS_URI: str | None = None
    ALLOW_DANGEROUS_REQUESTS: bool
    WEATHER_API_API_KEY : str
    TOOLS_YAML_PATH: str | Path = PROJECT_ROOT / "ai_engine" / "tools" / "training_apis.yaml"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

if __name__ == "__main__":
    print(settings.WEATHER_API_API_KEY)
    print(settings.MONGODB_ATLAS_URI)