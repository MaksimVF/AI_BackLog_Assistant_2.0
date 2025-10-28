




"""
Connection Checker Module

This module checks and logs the status of connections to external services.
"""

import logging
from typing import Dict, Any
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import asyncio
from src.db.connection import AsyncSessionLocal
from src.config import Config

# Configure logging
logger = logging.getLogger(__name__)

class ConnectionChecker:
    """Checks connections to external services"""

    def __init__(self):
        """Initialize the Connection Checker"""
        logger.info("Initializing Connection Checker")

    async def check_all_connections(self) -> Dict[str, Any]:
        """
        Check all external service connections

        Returns:
            Dict with connection status for each service
        """
        result = {
            "database": await self._check_database_connection(),
            "llm": await self._check_llm_connection(),
            "s3": await self._check_s3_connection()
        }

        # Log overall status
        all_connected = all(status.get("connected", False) for status in result.values())
        if all_connected:
            logger.info("✅ All external services are connected successfully")
        else:
            logger.warning("⚠️ Some external services have connection issues")

        return result

    async def _check_database_connection(self) -> Dict[str, Any]:
        """Check database connection with timeout"""
        try:
            # Add timeout to prevent hanging
            async with AsyncSessionLocal() as db:
                # Try a simple query to test connection
                result = await asyncio.wait_for(db.execute("SELECT 1"), timeout=5.0)
                await result.scalar()
                logger.info("✅ Database connection successful")
                return {"connected": True, "error": None, "details": "Connection established, query successful"}
        except asyncio.TimeoutError:
            logger.error("❌ Database connection timed out after 5 seconds")
            return {"connected": False, "error": "Connection timeout", "details": "Database did not respond within 5 seconds"}
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return {"connected": False, "error": str(e), "details": "Unexpected database error"}

    async def _check_llm_connection(self) -> Dict[str, Any]:
        """Check LLM model connection"""
        try:
            # For now, we'll just check if the config is set
            # In a real implementation, we'd try to load the model
            if hasattr(Config, 'LLM_MODEL') and Config.LLM_MODEL:
                logger.info("✅ LLM model configuration found")
                return {"connected": True, "error": None}
            else:
                logger.warning("⚠️ LLM model not configured")
                return {"connected": False, "error": "LLM model not configured"}
        except Exception as e:
            logger.error(f"❌ LLM connection check failed: {e}")
            return {"connected": False, "error": str(e)}

    async def _check_s3_connection(self) -> Dict[str, Any]:
        """Check S3 bucket connection"""
        try:
            # Create S3 client
            s3 = boto3.client(
                's3',
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                region_name=Config.AWS_REGION
            )

            # Try to list buckets to test connection
            s3.head_bucket(Bucket=Config.AWS_S3_BUCKET)
            logger.info("✅ S3 bucket connection successful")
            return {"connected": True, "error": None}
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"❌ S3 connection failed - credentials issue: {e}")
            return {"connected": False, "error": f"Credentials issue: {e}"}
        except Exception as e:
            logger.error(f"❌ S3 connection failed: {e}")
            return {"connected": False, "error": str(e)}

# Create a global instance for easy access
connection_checker = ConnectionChecker()

