from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta

# Database setup for async operations
DATABASE_URL = "sqlite+aiosqlite:///./sh7omylab.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base: DeclarativeMeta = declarative_base()

# Dependency to get async database session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db