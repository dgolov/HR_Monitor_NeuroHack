from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from src.settings import app_config
from typing import AsyncGenerator


engine = create_async_engine(app_config.DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)
