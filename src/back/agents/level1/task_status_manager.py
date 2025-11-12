
"""
Task Status Manager

This module manages task status workflow including transitions between
different statuses like new, in progress, completed, etc.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository
from src.db.models import Task

# Configure logging
logger = logging.getLogger(__name__)

class TaskStatusManager:
    """Manages task status workflow"""

    # Define valid status transitions
    VALID_TRANSITIONS = {
        'new': ['in_progress', 'cancelled'],
        'in_progress': ['completed', 'on_hold', 'cancelled'],
        'on_hold': ['in_progress', 'cancelled'],
        'completed': [],  # Terminal state
        'cancelled': [],  # Terminal state
        'pending': ['new', 'in_progress', 'cancelled']  # Initial state
    }

    def __init__(self):
        """Initialize the Task Status Manager"""
        logger.info("Initializing Task Status Manager")

    async def update_task_status(self, task_id: str, new_status: str, user_id: str = None) -> Dict[str, Any]:
        """
        Update task status with validation

        Args:
            task_id: The task ID to update
            new_status: The new status to set
            user_id: Optional user ID for permission checking

        Returns:
            Dict with update status and task information
        """
        result = {
            "status": "failed",
            "task_id": task_id,
            "message": "",
            "task": None
        }

        try:
            async with AsyncSessionLocal() as db:
                # Get current task
                task = await TaskRepository.get_task_by_task_id(db, task_id)

                if not task:
                    result["message"] = "Task not found"
                    return result

                # Validate status transition
                if not self._is_valid_transition(task.status, new_status):
                    result["message"] = f"Invalid status transition: {task.status} -> {new_status}"
                    return result

                # Update task status
                update_data = {
                    "status": new_status,
                    "updated_at": datetime.utcnow()
                }

                # Add user info if provided
                if user_id:
                    if task.task_metadata is None:
                        task.task_metadata = {}
                    task.task_metadata["last_updated_by"] = user_id
                    update_data["task_metadata"] = task.task_metadata

                updated_task = await TaskRepository.update_task(db, task_id, update_data)

                if updated_task:
                    result["status"] = "success"
                    result["message"] = f"Task status updated to {new_status}"
                    result["task"] = updated_task
                else:
                    result["message"] = "Failed to update task status"

        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            result["message"] = str(e)

        return result

    def _is_valid_transition(self, current_status: str, new_status: str) -> bool:
        """
        Validate status transition

        Args:
            current_status: Current task status
            new_status: New status to transition to

        Returns:
            True if transition is valid, False otherwise
        """
        if current_status not in self.VALID_TRANSITIONS:
            logger.warning(f"Unknown current status: {current_status}")
            return False

        if new_status in self.VALID_TRANSITIONS[current_status]:
            return True

        logger.warning(f"Invalid transition: {current_status} -> {new_status}")
        return False

    def get_valid_transitions(self, current_status: str) -> list:
        """
        Get valid transitions from current status

        Args:
            current_status: Current task status

        Returns:
            List of valid next statuses
        """
        return self.VALID_TRANSITIONS.get(current_status, [])

    async def get_task_status_info(self, task_id: str) -> Dict[str, Any]:
        """
        Get detailed task status information

        Args:
            task_id: The task ID to check

        Returns:
            Dict with task status information
        """
        result = {
            "status": "failed",
            "task_id": task_id,
            "message": "",
            "task_info": None
        }

        try:
            async with AsyncSessionLocal() as db:
                task = await TaskRepository.get_task_by_task_id(db, task_id)

                if not task:
                    result["message"] = "Task not found"
                    return result

                task_info = {
                    "task_id": task.task_id,
                    "current_status": task.status,
                    "valid_transitions": self.get_valid_transitions(task.status),
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "classification": task.classification,
                    "recommendation": task.recommendation
                }

                result["status"] = "success"
                result["task_info"] = task_info
                result["message"] = "Task status information retrieved"

        except Exception as e:
            logger.error(f"Error getting task status info: {e}")
            result["message"] = str(e)

        return result

# Create a global instance
task_status_manager = TaskStatusManager()
