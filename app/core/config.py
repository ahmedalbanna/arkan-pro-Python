from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "arkan-backend"
    ENV: str = "dev"

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = ["*"]

    # Security
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TOKEN_AUDIENCE: str | None = None
    TOKEN_ISSUER: str | None = None

    # DB (placeholder)
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
