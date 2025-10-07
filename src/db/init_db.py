



"""
Database Initialization for AI Backlog Assistant

This module provides database initialization and migration utilities.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Base
from src.db.connection import async_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """Initialize the database with tables"""
    async with async_engine.begin() as conn:
        # Drop all tables (for development only)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

async def drop_db():
    """Drop all database tables (for development only)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped successfully")

if __name__ == "__main__":
    import asyncio

    async def main():
        await init_db()

    asyncio.run(main())

