from fastapi import Depends
from src.database.db import async_session_maker
from src.repositiry.repo import Repository


async def create_repo():
    async with async_session_maker() as session:
        yield Repository(session=session)


repo_dep = Depends(create_repo)
