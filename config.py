"""
SIH Problem Statement 26044 | Team DECiphers
Central Configuration Management (Streamlit Cloud & Local Environment Support)
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_secret(key: str, default: str = "") -> str:
    """
    Safely retrieves a configuration key prioritizing:
    1. Streamlit Cloud Secrets (st.secrets)
    2. OS Environment Variables (os.getenv)
    3. Default fallback value
    """
    # 1. Check Streamlit Secrets if running on Streamlit Community Cloud
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass

    # 2. Check System / OS Environment Variables
    val = os.getenv(key)
    if val is not None and val.strip() != "":
        return val

    # 3. Return Fallback Default
    return default


class Settings(BaseSettings):
    # Application Metadata
    PROJECT_NAME: str = "Academia–Industry AI Collaboration Portal (SIH 26044 - DECiphers)"

    # Database Configuration (Asynchronous SQLite)
    DATABASE_URL: str = get_secret("DATABASE_URL", "sqlite+aiosqlite:///./portal.db")

    # 100% Free Groq AI Configuration
    GROQ_API_KEY: str = get_secret("GROQ_API_KEY", "gsk_PASTE_YOUR_LOCAL_KEY_HERE")
    GROQ_BASE_URL: str = get_secret("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    GROQ_MODEL: str = get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Identity & Access Management (JWT Security Keys)
    JWT_SECRET_KEY: str = get_secret(
        "JWT_SECRET_KEY", 
        "super-secret-jwt-key-change-this-for-production-12345"
    )
    JWT_REFRESH_SECRET_KEY: str = get_secret(
        "JWT_REFRESH_SECRET_KEY", 
        "super-secret-refresh-key-change-this-for-production-12345"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Pydantic Settings Configuration:
    # Loads .env locally if present, but never crashes if .env is missing on Streamlit Cloud
    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Global singleton instance imported across all modules
settings = Settings()
