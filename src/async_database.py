from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://admin:123@db/rinha"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

class Base(AsyncAttrs, DeclarativeBase):
    pass

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)