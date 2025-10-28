


"""
Database Repository for AI Backlog Assistant

This module provides database operations for tasks, files, and triggers.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from src.db.models import Task, TaskFile, Trigger
from datetime import datetime
from typing import List, Optional

class TaskRepository:
    """Repository for task operations"""

    @staticmethod
    async def create_task(db: AsyncSession, task_data: dict) -> Task:
        """Create a new task"""
        task = Task(**task_data)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        result = await db.execute(select(Task).filter(Task.task_id == task_id))
        return result.scalars().first()

    @staticmethod
    async def get_task_by_task_id(db: AsyncSession, task_id: str) -> Optional[Task]:
        """Get task by task_id"""
        result = await db.execute(select(Task).filter(Task.task_id == task_id))
        return result.scalars().first()

    @staticmethod
    async def update_task(db: AsyncSession, task_id: str, update_data: dict) -> Optional[Task]:
        """Update task by ID"""
        result = await db.execute(
            update(Task)
            .where(Task.task_id == task_id)
            .values(**update_data)
        )
        if result.rowcount == 0:
            return None
        await db.commit()
        return await TaskRepository.get_task_by_task_id(db, task_id)

    @staticmethod
    async def list_tasks(db: AsyncSession, limit: int = 10) -> List[Task]:
        """List recent tasks"""
        result = await db.execute(select(Task).order_by(Task.created_at.desc()).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def get_recent_tasks_by_user(db: AsyncSession, user_id: str, since_time: datetime) -> List[Task]:
        """Get recent tasks by user since a specific time"""
        result = await db.execute(
            select(Task)
            .filter(Task.metadata["user_id"].as_string() == user_id)
            .filter(Task.created_at >= since_time)
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: str) -> bool:
        """Delete task by ID"""
        result = await db.execute(delete(Task).where(Task.task_id == task_id))
        await db.commit()
        return result.rowcount > 0

class TaskFileRepository:
    """Repository for task file operations"""

    @staticmethod
    async def create_task_file(db: AsyncSession, file_data: dict) -> TaskFile:
        """Create a new task file"""
        task_file = TaskFile(**file_data)
        db.add(task_file)
        await db.commit()
        await db.refresh(task_file)
        return task_file

    @staticmethod
    async def get_files_by_task_id(db: AsyncSession, task_id: str) -> List[TaskFile]:
        """Get files by task ID"""
        result = await db.execute(select(TaskFile).filter(TaskFile.task_id == task_id))
        return result.scalars().all()

class TriggerRepository:
    """Repository for trigger operations"""

    @staticmethod
    async def create_trigger(db: AsyncSession, trigger_data: dict) -> Trigger:
        """Create a new trigger"""
        trigger = Trigger(**trigger_data)
        db.add(trigger)
        await db.commit()
        await db.refresh(trigger)
        return trigger

    @staticmethod
    async def get_triggers_by_task_id(db: AsyncSession, task_id: str) -> List[Trigger]:
        """Get triggers by task ID"""
        result = await db.execute(select(Trigger).filter(Trigger.task_id == task_id))
        return result.scalars().all()

    @staticmethod
    async def list_triggers(db: AsyncSession, limit: int = 10) -> List[Trigger]:
        """List recent triggers"""
        result = await db.execute(select(Trigger).order_by(Trigger.timestamp.desc()).limit(limit))
        return result.scalars().all()
