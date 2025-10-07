



"""
Test Database Integration for AI Backlog Assistant

This module tests the database integration functionality.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TaskFileRepository, TriggerRepository
from src.db.models import Task, TaskFile, Trigger
from datetime import datetime

@pytest.mark.asyncio
async def test_task_creation():
    """Test task creation in the database"""
    async with AsyncSessionLocal() as db:
        # Create a test task
        task_data = {
            "task_id": "test_task_1",
            "input_data": "Test task input data",
            "metadata": {"source": "test"},
            "status": "pending",
            "classification": "idea",
            "risk_score": 3.5,
            "impact_score": 7.2,
            "confidence_score": 8.1,
            "urgency_score": 6.8,
            "recommendation": "Test recommendation",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        task = await TaskRepository.create_task(db, task_data)

        # Verify task was created
        assert task is not None
        assert task.task_id == "test_task_1"
        assert task.input_data == "Test task input data"

        # Clean up
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_task_retrieval():
    """Test task retrieval from the database"""
    async with AsyncSessionLocal() as db:
        # Create a test task
        task_data = {
            "task_id": "test_task_2",
            "input_data": "Test task retrieval",
            "metadata": {"source": "test"},
            "status": "completed",
            "classification": "bug",
            "risk_score": 4.2,
            "impact_score": 6.5,
            "confidence_score": 7.8,
            "urgency_score": 5.3,
            "recommendation": "Fix immediately",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        task = await TaskRepository.create_task(db, task_data)

        # Retrieve the task
        retrieved_task = await TaskRepository.get_task_by_task_id(db, "test_task_2")

        # Verify retrieval
        assert retrieved_task is not None
        assert retrieved_task.task_id == "test_task_2"
        assert retrieved_task.status == "completed"

        # Clean up
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_task_listing():
    """Test task listing from the database"""
    async with AsyncSessionLocal() as db:
        # Create multiple test tasks
        for i in range(3):
            task_data = {
                "task_id": f"test_task_list_{i}",
                "input_data": f"Test task {i}",
                "metadata": {"source": "test"},
                "status": "pending",
                "classification": "idea",
                "risk_score": 3.0,
                "impact_score": 6.0,
                "confidence_score": 7.0,
                "urgency_score": 5.0,
                "recommendation": f"Test recommendation {i}",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            await TaskRepository.create_task(db, task_data)

        # List tasks
        tasks = await TaskRepository.list_tasks(db, limit=5)

        # Verify listing
        assert len(tasks) >= 3
        assert tasks[0].task_id.startswith("test_task_list_")

        # Clean up
        for task in tasks:
            if task.task_id.startswith("test_task_list_"):
                await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_task_file_creation():
    """Test task file creation in the database"""
    async with AsyncSessionLocal() as db:
        # Create a test task first
        task_data = {
            "task_id": "test_task_file",
            "input_data": "Test task for file",
            "metadata": {"source": "test"},
            "status": "pending",
            "classification": "idea",
            "risk_score": 3.0,
            "impact_score": 6.0,
            "confidence_score": 7.0,
            "urgency_score": 5.0,
            "recommendation": "Test recommendation",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        task = await TaskRepository.create_task(db, task_data)

        # Create a test file
        file_data = {
            "task_id": "test_task_file",
            "file_url": "https://example.com/test.pdf",
            "file_type": "pdf",
            "s3_key": "test-files/test.pdf",
            "created_at": datetime.utcnow()
        }

        task_file = await TaskFileRepository.create_task_file(db, file_data)

        # Verify file was created
        assert task_file is not None
        assert task_file.file_url == "https://example.com/test.pdf"

        # Clean up
        await db.delete(task_file)
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_trigger_creation():
    """Test trigger creation in the database"""
    async with AsyncSessionLocal() as db:
        # Create a test task first
        task_data = {
            "task_id": "test_trigger_task",
            "input_data": "Test task for trigger",
            "metadata": {"source": "test"},
            "status": "pending",
            "classification": "idea",
            "risk_score": 3.0,
            "impact_score": 6.0,
            "confidence_score": 7.0,
            "urgency_score": 5.0,
            "recommendation": "Test recommendation",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        task = await TaskRepository.create_task(db, task_data)

        # Create a test trigger
        trigger_data = {
            "trigger_id": "test_trigger_1",
            "task_id": "test_trigger_task",
            "reason": "high_urgency",
            "timestamp": datetime.utcnow()
        }

        trigger = await TriggerRepository.create_trigger(db, trigger_data)

        # Verify trigger was created
        assert trigger is not None
        assert trigger.trigger_id == "test_trigger_1"
        assert trigger.reason == "high_urgency"

        # Clean up
        await db.delete(trigger)
        await db.delete(task)
        await db.commit()


