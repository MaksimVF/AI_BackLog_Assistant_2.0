




"""
Simple Database Test for AI Backlog Assistant

This script tests the database integration without external dependencies.
"""

import asyncio
from datetime import datetime
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TaskFileRepository, TriggerRepository

async def test_database_operations():
    """Test basic database operations"""
    try:
        # Test task creation
        async with AsyncSessionLocal() as db:
            task_data = {
                "task_id": "test_task_simple",
                "input_data": "Simple test task",
                "task_metadata": {"source": "test"},
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

            # Create task
            task = await TaskRepository.create_task(db, task_data)
            print(f"✅ Task created: {task.task_id}")

            # Retrieve task
            retrieved_task = await TaskRepository.get_task_by_task_id(db, "test_task_simple")
            print(f"✅ Task retrieved: {retrieved_task.task_id}")

            # List tasks
            tasks = await TaskRepository.list_tasks(db, limit=5)
            print(f"✅ Tasks listed: {len(tasks)} tasks found")

            # Create task file
            file_data = {
                "task_id": "test_task_simple",
                "file_url": "https://example.com/test.pdf",
                "file_type": "pdf",
                "s3_key": "test-files/test.pdf",
                "created_at": datetime.utcnow()
            }

            task_file = await TaskFileRepository.create_task_file(db, file_data)
            print(f"✅ Task file created: {task_file.file_url}")

            # Create trigger
            trigger_data = {
                "trigger_id": "test_trigger_simple",
                "task_id": "test_task_simple",
                "reason": "high_urgency",
                "timestamp": datetime.utcnow()
            }

            trigger = await TriggerRepository.create_trigger(db, trigger_data)
            print(f"✅ Trigger created: {trigger.trigger_id}")

            # List triggers
            triggers = await TriggerRepository.list_triggers(db, limit=5)
            print(f"✅ Triggers listed: {len(triggers)} triggers found")

            # Clean up
            await db.delete(trigger)
            await db.delete(task_file)
            await db.delete(task)
            await db.commit()

            print("✅ All database operations completed successfully!")

    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_database_operations())


