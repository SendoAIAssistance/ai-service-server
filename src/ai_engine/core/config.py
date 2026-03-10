# Config: Model (Llama), paths, API keys
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from pathlib import Path

CURRENT_CONFIG_FILE_PATH = Path(__file__).resolve() # config.py
PROJECT_ROOT = CURRENT_CONFIG_FILE_PATH.parent.parent.parent.parent # $
load_dotenv(Path(PROJECT_ROOT) / ".env")
console = Console()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tech Support Agent"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    OLLAMA_HOST: str | None = None
    PROJECT_ROOT: Path = PROJECT_ROOT
    DATA_ROOT: Path = PROJECT_ROOT / "src" / "storage" / "vector_db" / "sendo_dictionary"
    MONGODB_ATLAS_URI: str | None = None
    WEATHER_API_API_KEY : str | None = None

    TOOLS_YAML_PATH: str | Path = PROJECT_ROOT / "ai_engine" / "tools" / "training_apis.yaml"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()