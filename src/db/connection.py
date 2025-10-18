


"""
Database Connection Utilities for AI Backlog Assistant

This module provides database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import Config

config = Config()

# Async database engine
if "sqlite" in config.POSTGRES_URL:
    async_engine = create_async_engine(
        config.POSTGRES_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    async_engine = create_async_engine(
        config.POSTGRES_URL,
        echo=False,
        pool_size=10,
        max_overflow=20
    )

# Async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()

async def get_async_db():
    """Get an async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
