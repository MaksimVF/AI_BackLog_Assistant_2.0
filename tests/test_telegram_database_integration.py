




"""
Test Telegram Bot Database Integration for AI Backlog Assistant

This module tests the Telegram bot integration with the database.
"""

import pytest
from src.bot.telegram_bot import telegram_bot
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository

@pytest.mark.asyncio
async def test_telegram_task_creation():
    """Test Telegram task creation with database storage"""
    # Process a Telegram message
    result = await telegram_bot.process_telegram_message(
        "Test Telegram task for database integration",
        "test_user_123"
    )

    # Verify the result
    assert result["status"] == "completed"
    assert "task_id" in result

    # Verify the task was stored in the database
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, result["task_id"])

        assert task is not None
        assert task.input_data == "Test Telegram task for database integration"
        assert task.metadata["user_id"] == "test_user_123"

        # Clean up
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_telegram_task_status():
    """Test Telegram task status retrieval"""
    # First create a task
    create_result = await telegram_bot.process_telegram_message(
        "Test Telegram task status",
        "test_user_456"
    )

    task_id = create_result["task_id"]

    # Get the task status
    status_result = await telegram_bot.get_task_status(task_id)

    # Verify the status
    assert status_result["status"] == "completed"
    assert status_result["task_id"] == task_id

    # Clean up
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, task_id)
        if task:
            await db.delete(task)
            await db.commit()

@pytest.mark.asyncio
async def test_telegram_task_listing():
    """Test Telegram task listing"""
    # Create a few tasks
    for i in range(3):
        await telegram_bot.process_telegram_message(
            f"Test Telegram task listing {i}",
            f"test_user_{i}"
        )

    # List the tasks
    list_result = await telegram_bot.list_tasks()

    # Verify the listing
    assert "tasks" in list_result
    assert len(list_result["tasks"]) >= 3

    # Clean up
    async with AsyncSessionLocal() as db:
        tasks = await TaskRepository.list_tasks(db, limit=10)
        for task in tasks:
            if task.input_data.startswith("Test Telegram task listing"):
                await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_telegram_task_archive():
    """Test Telegram task archive retrieval"""
    # Create a task
    create_result = await telegram_bot.process_telegram_message(
        "Test Telegram task archive",
        "test_user_archive"
    )

    task_id = create_result["task_id"]

    # Get the task archive
    archive_result = await telegram_bot.get_task_archive(task_id)

    # Verify the archive
    assert archive_result["task_id"] == task_id
    assert archive_result["original_input"] == "Test Telegram task archive"
    assert "analysis_results" in archive_result

    # Clean up
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, task_id)
        if task:
            await db.delete(task)
            await db.commit()
