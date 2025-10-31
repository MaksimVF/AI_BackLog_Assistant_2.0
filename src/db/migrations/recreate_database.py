





"""
Script to recreate the database with new schema
"""

from sqlalchemy import create_engine
from src.db.models import Base
from src.config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    """Recreate the database with new schema"""
    try:
        config = Config()

        # Create engine
        engine = create_engine(config.POSTGRES_URL.replace("+asyncpg", "").replace("+aiosqlite", ""))

        # Drop all tables
        Base.metadata.drop_all(engine)
        logger.info("✅ Dropped all tables")

        # Create all tables
        Base.metadata.create_all(engine)
        logger.info("✅ Created all tables")

        logger.info("✅ Database recreation completed successfully")

    except Exception as e:
        logger.error(f"❌ Database recreation failed: {e}")
        raise

if __name__ == "__main__":
    recreate_database()





