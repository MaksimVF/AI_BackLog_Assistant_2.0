





"""
Migration script to add new fields to the tasks table
"""

from sqlalchemy import create_engine, Column, String, Float, Text
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, Task
from src.config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Run the migration to add new fields to tasks table"""
    try:
        # Create engine
        config = Config()
        engine = create_engine(config.POSTGRES_URL.replace("+asyncpg", "").replace("+aiosqlite", ""))

        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        # Add new columns to Task model
        # Note: In a real migration, we'd use Alembic, but for simplicity we'll do it directly
        try:
            # Try to add the columns one by one (SQLite doesn't support multiple ALTER in one statement)
            session.execute("ALTER TABLE tasks ADD COLUMN sub_category VARCHAR(50)")
            session.execute("ALTER TABLE tasks ADD COLUMN domain VARCHAR(50)")
            session.execute("ALTER TABLE tasks ADD COLUMN sentiment VARCHAR(50)")
            session.execute("ALTER TABLE tasks ADD COLUMN confidence FLOAT")
            session.execute("ALTER TABLE tasks ADD COLUMN priority_score FLOAT")
            session.execute("ALTER TABLE tasks ADD COLUMN priority_level VARCHAR(50)")
            session.execute("ALTER TABLE tasks ADD COLUMN priority_recommendation TEXT")
            session.commit()
            logger.info("✅ Migration completed successfully")
        except Exception as e:
            # If columns already exist, that's fine
            session.rollback()
            logger.warning(f"Migration warning: {e}. Columns may already exist.")

        session.close()

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()





