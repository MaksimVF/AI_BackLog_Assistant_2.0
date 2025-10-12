




"""
Test API Database Integration for AI Backlog Assistant

This module tests the API endpoints with database integration.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TriggerRepository
from datetime import datetime

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_task_api():
    """Test the /tasks API endpoint with database storage"""
    # Create a task via API
    response = client.post(
        "/tasks",
        json={
            "input_data": "Test API task creation",
            "metadata": {"source": "api_test"}
        }
    )

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "completed"

    # Verify the task was stored in the database
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, data["task_id"])

        assert task is not None
        assert task.input_data == "Test API task creation"

        # Clean up
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_get_triggers_api():
    """Test the /triggers API endpoint with database data"""
    # Create a test task and trigger
    async with AsyncSessionLocal() as db:
        # Create task
        task_data = {
            "task_id": "test_trigger_task",
            "input_data": "Test trigger task",
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

        # Create trigger
        trigger_data = {
            "trigger_id": "test_trigger_1",
            "task_id": "test_trigger_task",
            "reason": "high_urgency",
            "timestamp": datetime.utcnow()
        }

        await TriggerRepository.create_trigger(db, trigger_data)
        await db.commit()

    # Get triggers via API
    response = client.get("/triggers")

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["trigger_id"] == "test_trigger_1"

    # Clean up
    async with AsyncSessionLocal() as db:
        await db.delete(trigger)
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_telegram_message_api():
    """Test the /telegram/message API endpoint with database storage"""
    # Send a Telegram message via API
    response = client.post(
        "/telegram/message",
        json={
            "message_text": "Test Telegram API message",
            "user_id": "api_test_user"
        }
    )

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "completed"

    # Verify the task was stored in the database
    async with AsyncSessionLocal() as db:
        task = await TaskRepository.get_task_by_task_id(db, data["task_id"])

        assert task is not None
        assert task.input_data == "Test Telegram API message"

        # Clean up
        await db.delete(task)
        await db.commit()

@pytest.mark.asyncio
async def test_telegram_task_status_api():
    """Test the /telegram/status API endpoint with database data"""
    # First create a task
    async with AsyncSessionLocal() as db:
        task_data = {
            "task_id": "test_status_task",
            "input_data": "Test status task",
            "metadata": {"source": "test", "user_id": "api_test_user"},
            "status": "completed",
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
        await db.commit()

    # Get task status via API
    response = client.get(f"/telegram/status/{task.task_id}")

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task.task_id
    assert data["status"] == "completed"

    # Clean up
    async with AsyncSessionLocal() as db:
        await db.delete(task)
        await db.commit()
