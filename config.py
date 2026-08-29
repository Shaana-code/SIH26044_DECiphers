from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Info
    PROJECT_NAME: str = "Academia–Industry AI Collaboration Portal"
    
    # Database Configuration (Asynchronous SQLite)
    DATABASE_URL: str = "sqlite+aiosqlite:///./portal.db"

    # 100% Free Groq AI Configuration
    GROQ_API_KEY: str = "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"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # High performance & free tier

    # Identity & Access Management (JWT Security)
    JWT_SECRET_KEY: str = "super-secret-jwt-key-change-this-for-production"
    JWT_REFRESH_SECRET_KEY: str = "super-secret-refresh-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Automatically loads environment variables from root-level .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Global settings instance imported across all modules
settings = Settings()