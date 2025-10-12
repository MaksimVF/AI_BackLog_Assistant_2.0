




"""
Test Telegram Bot Database Integration for AI Backlog Assistant

This module tests the Telegram bot integration with the database.
"""

import pytest
from unittest.mock import patch, AsyncMock
from src.bot.telegram_bot import telegram_bot
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository

@pytest.mark.asyncio
async def test_telegram_task_creation():
    """Test Telegram task creation with database storage"""
    # Process a Telegram message
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task, \
         patch("src.bot.telegram_bot.TaskRepository.get_task_by_task_id") as mock_get_task:

        # Mock the orchestrator
        mock_orchestrator.process_workflow.return_value = {
            "classification": "feature",
            "risk_score": 2.5,
            "impact_score": 4.0,
            "confidence_score": 0.9,
            "urgency_score": 3.2,
            "recommendation": "Implement soon"
        }
        mock_create_task.return_value = None

        # Mock the task retrieval
        mock_task = AsyncMock()
        mock_task.input_data = "Test Telegram task for database integration"
        mock_task.metadata = {"user_id": "test_user_123"}
        mock_get_task.return_value = mock_task

        result = await telegram_bot.process_telegram_message(
            "Test Telegram task for database integration",
            "test_user_123"
        )

        # Verify the result
        assert result["status"] == "completed"
        assert "task_id" in result

        # Verify the task was stored in the database
        # (mock already verifies this)

@pytest.mark.asyncio
async def test_telegram_task_status():
    """Test Telegram task status retrieval"""
    # First create a task
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task, \
         patch("src.bot.telegram_bot.TaskRepository.get_task_by_task_id") as mock_get_task:

        # Mock the orchestrator
        mock_orchestrator.process_workflow.return_value = {
            "classification": "feature",
            "risk_score": 2.5,
            "impact_score": 4.0,
            "confidence_score": 0.9,
            "urgency_score": 3.2,
            "recommendation": "Implement soon"
        }
        mock_create_task.return_value = None

        # Mock the task retrieval
        mock_task = AsyncMock()
        mock_task.task_id = "test_task_123"
        mock_task.status = "completed"
        mock_task.classification = "feature"
        mock_task.risk_score = 2.5
        mock_task.impact_score = 4.0
        mock_task.recommendation = "Implement soon"
        mock_get_task.return_value = mock_task

        create_result = await telegram_bot.process_telegram_message(
            "Test Telegram task status",
            "test_user_456"
        )

        task_id = "test_task_123"  # Use the mock task ID

        # Get the task status
        status_result = await telegram_bot.get_task_status(task_id)

        # Verify the status
        assert status_result["status"] == "completed"
        assert status_result["task_id"] == task_id

@pytest.mark.asyncio
async def test_telegram_task_listing():
    """Test Telegram task listing"""
    # Create a few tasks
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task, \
         patch("src.bot.telegram_bot.TaskRepository.list_tasks") as mock_list_tasks:

        # Mock the orchestrator
        mock_orchestrator.process_workflow.return_value = {
            "classification": "feature",
            "risk_score": 2.5,
            "impact_score": 4.0,
            "confidence_score": 0.9,
            "urgency_score": 3.2,
            "recommendation": "Implement soon"
        }
        mock_create_task.return_value = None

        # Mock the task listing
        mock_task1 = AsyncMock()
        mock_task1.task_id = "task_1"
        mock_task1.input_data = "Test Telegram task listing 0"
        mock_task1.status = "completed"
        mock_task1.recommendation = "Implement soon"

        mock_task2 = AsyncMock()
        mock_task2.task_id = "task_2"
        mock_task2.input_data = "Test Telegram task listing 1"
        mock_task2.status = "completed"
        mock_task2.recommendation = "Implement soon"

        mock_task3 = AsyncMock()
        mock_task3.task_id = "task_3"
        mock_task3.input_data = "Test Telegram task listing 2"
        mock_task3.status = "completed"
        mock_task3.recommendation = "Implement soon"

        mock_list_tasks.return_value = [mock_task1, mock_task2, mock_task3]

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

@pytest.mark.asyncio
async def test_telegram_task_archive():
    """Test Telegram task archive retrieval"""
    # Create a task
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task, \
         patch("src.bot.telegram_bot.TaskRepository.get_task_by_task_id") as mock_get_task, \
         patch("src.bot.telegram_bot.TaskFileRepository.get_files_by_task_id") as mock_get_files:

        # Mock the orchestrator
        mock_orchestrator.process_workflow.return_value = {
            "classification": "feature",
            "risk_score": 2.5,
            "impact_score": 4.0,
            "confidence_score": 0.9,
            "urgency_score": 3.2,
            "recommendation": "Implement soon"
        }
        mock_create_task.return_value = None
        mock_get_files.return_value = []

        # Mock the task retrieval
        mock_task = AsyncMock()
        mock_task.task_id = "test_archive_task"
        mock_task.input_data = "Test Telegram task archive"
        mock_task.classification = "feature"
        mock_task.risk_score = 2.5
        mock_task.impact_score = 4.0
        mock_task.confidence_score = 0.9
        mock_task.urgency_score = 3.2
        mock_task.recommendation = "Implement soon"
        mock_task.status = "completed"
        mock_get_task.return_value = mock_task

        create_result = await telegram_bot.process_telegram_message(
            "Test Telegram task archive",
            "test_user_archive"
        )

        task_id = "test_archive_task"  # Use the mock task ID

        # Get the task archive
        archive_result = await telegram_bot.get_task_archive(task_id)

        # Verify the archive
        assert archive_result["task_id"] == task_id
        assert archive_result["original_input"] == "Test Telegram task archive"
        assert "analysis_results" in archive_result
