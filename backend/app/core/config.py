from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional, List
import logging
import os

# Path to backend/.env
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """Application settings loaded from backend/.env"""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
        case_sensitive=False,
    )

    # PostgreSQL
    DATABASE_URL: Optional[str] = None

    # MongoDB
    MONGODB_URL: Optional[str] = "mongodb://localhost:27017/"

    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Agmarknet API
    AGMARKNET_API_KEY: Optional[str] = None
    AGMARKNET_URL: str = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    # Kafka
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_ORDER_TOPIC: str = "order-topic"

    # App runtime
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    UPLOAD_DIR: Path = BASE_DIR / "uploads"

    # Logging
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://agromart.in",
        "https://www.agromart.in",
        "https://agromart-frontend.vercel.app",
    ]


settings = Settings()

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
)
logger = logging.getLogger("app.config")
