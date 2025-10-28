



"""
Duplicate Message Detector

This module detects and analyzes duplicate/repeated messages.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository

# Configure logging
logger = logging.getLogger(__name__)

class DuplicateDetector:
    """Detects and analyzes duplicate messages"""

    def __init__(self):
        """Initialize the Duplicate Detector"""
        logger.info("Initializing Duplicate Detector")

    async def check_duplicate(self, message_text: str, user_id: str, time_window_minutes: int = 60) -> Dict[str, Any]:
        """
        Check if a message is a duplicate within a time window

        Args:
            message_text: The text message to check
            user_id: The user ID
            time_window_minutes: Time window to check for duplicates

        Returns:
            Dict with duplicate status and analysis
        """
        result = {
            "is_duplicate": False,
            "duplicate_count": 0,
            "last_occurrence": None,
            "time_since_last": None,
            "analysis": "No duplicates found"
        }

        try:
            # Calculate time window
            time_threshold = datetime.utcnow() - timedelta(minutes=time_window_minutes)

            # Get recent tasks for this user
            async with AsyncSessionLocal() as db:
                try:
                    recent_tasks = await TaskRepository.get_recent_tasks_by_user(
                        db, user_id, time_threshold
                    )
                except Exception as e:
                    logger.error(f"Error getting recent tasks: {e}")
                    recent_tasks = []

                if not recent_tasks:
                    return result

                # Check for duplicates
                duplicates = []
                for task in recent_tasks:
                    if task.input_data == message_text:
                        duplicates.append(task)

                if duplicates:
                    result["is_duplicate"] = True
                    result["duplicate_count"] = len(duplicates)

                    # Get most recent duplicate
                    most_recent = max(duplicates, key=lambda x: x.created_at)
                    result["last_occurrence"] = most_recent.created_at
                    result["time_since_last"] = (datetime.utcnow() - most_recent.created_at).total_seconds() / 60  # in minutes

                    # Generate analysis
                    if result["duplicate_count"] == 1:
                        result["analysis"] = "This message was sent once before"
                    else:
                        result["analysis"] = f"This message has been sent {result['duplicate_count']} times before"

                    # Add pattern analysis
                    if result["time_since_last"] and result["time_since_last"] < 10:
                        result["analysis"] += ". User is repeating the message frequently."

        except Exception as e:
            logger.error(f"Error checking for duplicates: {e}")
            result["error"] = str(e)

        return result

# Create a global instance for easy access
duplicate_detector = DuplicateDetector()
