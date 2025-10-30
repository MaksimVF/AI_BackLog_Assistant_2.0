

#!/usr/bin/env python3
"""
Test script to verify duplicate detector functionality
"""

import asyncio
from src.agents.level1.duplicate_detector import duplicate_detector
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository
from datetime import datetime, timedelta

async def test_duplicate_detector():
    """Test the duplicate detector with sample data"""
    print("Testing Duplicate Detector...")
    print("=" * 50)

    # Create a test user ID
    test_user_id = "test_user_123"

    # Create test tasks in the database
    async with AsyncSessionLocal() as db:
        # Clear any existing test tasks by deleting tasks with the same task_id
        try:
            await TaskRepository.delete_task(db, "test_task_001")
        except:
            pass

        # Create a test task
        test_task = {
            "task_id": "test_task_001",
            "input_data": "Implement user authentication",
            "task_metadata": {"user_id": test_user_id},
            "status": "completed",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await TaskRepository.create_task(db, test_task)
        print("✅ Created test task in database")

        # Verify the task was created
        created_task = await TaskRepository.get_task_by_task_id(db, "test_task_001")
        if created_task:
            print(f"✅ Verified task creation: {created_task.input_data}")
        else:
            print("❌ Failed to create task")

    # Test 1: Check for duplicate (should find it)
    print("\nTest 1: Checking for duplicate of existing task...")
    result1 = await duplicate_detector.check_duplicate(
        "Implement user authentication",
        test_user_id,
        time_window_minutes=60
    )

    print(f"Is duplicate: {result1['is_duplicate']}")
    print(f"Duplicate count: {result1['duplicate_count']}")
    print(f"Last occurrence: {result1['last_occurrence']}")
    print(f"Time since last: {result1['time_since_last']} minutes")
    print(f"Analysis: {result1['analysis']}")

    # Test 2: Check for non-duplicate (should not find it)
    print("\nTest 2: Checking for non-duplicate...")
    result2 = await duplicate_detector.check_duplicate(
        "Implement payment system",
        test_user_id,
        time_window_minutes=60
    )

    print(f"Is duplicate: {result2['is_duplicate']}")
    print(f"Duplicate count: {result2['duplicate_count']}")
    print(f"Analysis: {result2['analysis']}")

    # Test 3: Check with different time window
    print("\nTest 3: Checking with different time window...")
    result3 = await duplicate_detector.check_duplicate(
        "Implement user authentication",
        test_user_id,
        time_window_minutes=5  # Very short window
    )

    print(f"Is duplicate: {result3['is_duplicate']}")
    print(f"Duplicate count: {result3['duplicate_count']}")
    print(f"Analysis: {result3['analysis']}")

    # Test 4: Add another duplicate and check
    print("\nTest 4: Adding another duplicate task and checking...")
    async with AsyncSessionLocal() as db:
        # Add another duplicate task
        duplicate_task = {
            "task_id": "test_task_002",
            "input_data": "Implement user authentication",
            "task_metadata": {"user_id": test_user_id},
            "status": "completed",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await TaskRepository.create_task(db, duplicate_task)
        print("✅ Created duplicate test task in database")

    # Check again
    result4 = await duplicate_detector.check_duplicate(
        "Implement user authentication",
        test_user_id,
        time_window_minutes=60
    )

    print(f"Is duplicate: {result4['is_duplicate']}")
    print(f"Duplicate count: {result4['duplicate_count']}")
    print(f"Analysis: {result4['analysis']}")

if __name__ == "__main__":
    asyncio.run(test_duplicate_detector())

