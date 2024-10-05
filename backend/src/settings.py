from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import logging


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DATABASE_URL: str


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

logger = logging.getLogger("backend")
