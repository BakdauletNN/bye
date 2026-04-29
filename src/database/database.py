from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.core.config import stgs
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(stgs.DB_URL)

async_ses_mkr = async_sessionmaker(bind=engine, expire_on_commit=False)
session = async_sessionmaker()


class BaseModel(DeclarativeBase):
    pass