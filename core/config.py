from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings and configuration.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Groq API Configuration
    GROQ_API_KEY: Optional[str] = None
    MODEL_NAME: str = ""

    # Database Configuration (Neon Postgres)
    DATABASE_URL: Optional[str] = None

settings = Settings()
