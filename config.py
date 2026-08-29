import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Meta
    PROJECT_NAME: str = "Academia–Industry AI Collaboration Portal"

    # Database Configuration (Asynchronous SQLite)
    DATABASE_URL: str = "sqlite+aiosqlite:///./portal.db"

    # 100% Free Groq AI Settings
    # (Reads from system environment variables / Streamlit secrets first, falls back to .env or default)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "gsk_PASTE_YOUR_LOCAL_KEY_HERE")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Identity & Access Management (JWT Security Keys)
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", 
        "super-secret-jwt-key-change-this-for-production-12345"
    )
    JWT_REFRESH_SECRET_KEY: str = os.getenv(
        "JWT_REFRESH_SECRET_KEY", 
        "super-secret-refresh-key-change-this-for-production-12345"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Pydantic Configuration:
    # Automatically reads from .env if it exists locally, but won't crash if .env is missing on GitHub
    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Global singleton instance imported across all modules
settings = Settings()
