from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from src.core.config import stgs
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

engine = create_async_engine(stgs.DB_URL)
async_ses_mkr = async_sessionmaker(bind=engine, expire_on_commit=False)


class BaseModel(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_ses_mkr() as session:
        yield session
