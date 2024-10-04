from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.settings import config


engine = create_async_engine(config.DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)
