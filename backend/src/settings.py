import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"


app_config = Settings()

log_directory = "./logs"
report_directory = "./reports"
Path(log_directory).mkdir(parents=True, exist_ok=True)
Path(report_directory).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Path(log_directory, "app.log")),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("backend")
