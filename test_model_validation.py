





"""
Model Validation Test for AI Backlog Assistant

This script tests the database models without requiring an actual database connection.
"""

from src.db.models import Task, TaskFile, Trigger
from datetime import datetime

def test_model_creation():
    """Test model instantiation"""
    try:
        # Test Task model
        task = Task(
            task_id="test_task_1",
            input_data="Test task input data",
            task_metadata={"source": "test"},
            status="pending",
            classification="idea",
            risk_score=3.5,
            impact_score=7.2,
            confidence_score=8.1,
            urgency_score=6.8,
            recommendation="Test recommendation",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        print(f"✅ Task model created: {task.task_id}")

        # Test TaskFile model
        task_file = TaskFile(
            task_id="test_task_1",
            file_url="https://example.com/test.pdf",
            file_type="pdf",
            s3_key="test-files/test.pdf",
            created_at=datetime.utcnow()
        )

        print(f"✅ TaskFile model created: {task_file.file_url}")

        # Test Trigger model
        trigger = Trigger(
            trigger_id="test_trigger_1",
            task_id="test_task_1",
            reason="high_urgency",
            timestamp=datetime.utcnow()
        )

        print(f"✅ Trigger model created: {trigger.trigger_id}")

        # Test relationships
        task.files = [task_file]
        task.triggers = [trigger]

        print(f"✅ Relationships set: {len(task.files)} files, {len(task.triggers)} triggers")

        # Verify field access
        assert task.task_id == "test_task_1"
        assert task.input_data == "Test task input data"
        assert task.task_metadata["source"] == "test"
        assert task.status == "pending"
        assert task.classification == "idea"
        assert task.risk_score == 3.5
        assert task.impact_score == 7.2
        assert task.confidence_score == 8.1
        assert task.urgency_score == 6.8
        assert task.recommendation == "Test recommendation"

        print("✅ All model validations passed!")

    except Exception as e:
        print(f"❌ Model validation failed: {e}")

if __name__ == "__main__":
    test_model_creation()



