import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DATABASE_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:" \
                        f"{os.getenv('POSTGRES_PASSWORD')}@db/{os.getenv('POSTGRES_DB')}"


app_config = Settings()
