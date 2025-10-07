





"""
Full Integration Test for AI Backlog Assistant

This module tests the complete integration of all components.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TaskFileRepository, TriggerRepository
from src.bot.telegram_bot import telegram_bot
from datetime import datetime

client = TestClient(app)

@pytest.mark.asyncio
async def test_full_workflow_integration():
    """Test the complete workflow from API to database to Telegram"""
    # Step 1: Create a task via API
    api_response = client.post(
        "/tasks",
        json={
            "input_data": "Full integration test task",
            "metadata": {"source": "integration_test"}
        }
    )

    assert api_response.status_code == 200
    api_data = api_response.json()
    task_id = api_data["task_id"]

    # Step 2: Verify task was stored in database
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, task_id)
        assert task is not None
        assert task.input_data == "Full integration test task"

        # Step 3: Process via Telegram bot
        telegram_result = await telegram_bot.process_telegram_message(
            "Telegram integration test",
            "integration_user"
        )

        assert telegram_result["status"] == "completed"
        telegram_task_id = telegram_result["task_id"]

        # Step 4: Verify Telegram task was stored
        telegram_task = await TaskRepository.get_task_by_task_id(db, telegram_task_id)
        assert telegram_task is not None
        assert telegram_task.input_data == "Telegram integration test"

        # Step 5: Get task status
        status_result = await telegram_bot.get_task_status(telegram_task_id)
        assert status_result["status"] == "completed"

        # Step 6: List tasks
        list_result = await telegram_bot.list_tasks()
        assert len(list_result["tasks"]) >= 2

        # Step 7: Get task archive
        archive_result = await telegram_bot.get_task_archive(telegram_task_id)
        assert archive_result["original_input"] == "Telegram integration test"

        # Clean up
        await db.delete(task)
        await db.delete(telegram_task)
        await db.commit()

@pytest.mark.asyncio
async def test_api_telegram_integration():
    """Test API and Telegram integration"""
    # Step 1: Process Telegram message via API
    telegram_response = client.post(
        "/telegram/message",
        json={
            "message_text": "API Telegram integration test",
            "user_id": "api_telegram_user"
        }
    )

    assert telegram_response.status_code == 200
    telegram_data = telegram_response.json()
    task_id = telegram_data["task_id"]

    # Step 2: Get task status via API
    status_response = client.get(f"/telegram/status/{task_id}")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["status"] == "completed"

    # Step 3: List tasks via API
    list_response = client.get("/telegram/tasks")
    assert list_response.status_code == 200
    list_data = list_response.json()
    assert len(list_data["tasks"]) >= 1

    # Step 4: Get triggers
    triggers_response = client.get("/triggers")
    assert triggers_response.status_code == 200

    # Clean up
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, task_id)
        if task:
            await db.delete(task)
            await db.commit()

@pytest.mark.asyncio
async def test_database_consistency():
    """Test database consistency across operations"""
    async with AsyncSessionLocal() as db:
        # Create a task
        task_data = {
            "task_id": "consistency_test",
            "input_data": "Database consistency test",
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

        # Create a file
        file_data = {
            "task_id": "consistency_test",
            "file_url": "https://example.com/test.pdf",
            "file_type": "pdf",
            "s3_key": "test-files/test.pdf",
            "created_at": datetime.utcnow()
        }

        task_file = await TaskFileRepository.create_task_file(db, file_data)

        # Create a trigger
        trigger_data = {
            "trigger_id": "consistency_trigger",
            "task_id": "consistency_test",
            "reason": "high_urgency",
            "timestamp": datetime.utcnow()
        }

        trigger = await TriggerRepository.create_trigger(db, trigger_data)

        # Verify relationships
        retrieved_task = await TaskRepository.get_task_by_task_id(db, "consistency_test")
        assert retrieved_task is not None

        files = await TaskFileRepository.get_files_by_task_id(db, "consistency_test")
        assert len(files) == 1
        assert files[0].file_url == "https://example.com/test.pdf"

        triggers = await TriggerRepository.get_triggers_by_task_id(db, "consistency_test")
        assert len(triggers) == 1
        assert triggers[0].reason == "high_urgency"

        # Clean up
        await db.delete(trigger)
        await db.delete(task_file)
        await db.delete(task)
        await db.commit()





