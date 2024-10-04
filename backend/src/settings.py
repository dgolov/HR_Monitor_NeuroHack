import os
import logging

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

log_directory = './logs'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_directory, "app.log")),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)
