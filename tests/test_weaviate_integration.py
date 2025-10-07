




"""
Test Weaviate Integration for AI Backlog Assistant

This module tests the Weaviate vector database integration.
"""

import pytest
from src.utils.weaviate_client import weaviate_client

@pytest.mark.skip(reason="Weaviate integration test - requires running Weaviate instance")
def test_weaviate_schema_creation():
    """Test Weaviate schema creation"""
    # Create schema
    result = weaviate_client.create_schema()
    assert result is True

@pytest.mark.skip(reason="Weaviate integration test - requires running Weaviate instance")
def test_weaviate_task_embedding():
    """Test adding and retrieving task embeddings from Weaviate"""
    # Create schema first
    weaviate_client.create_schema()

    # Test data
    task_id = "test_task_weaviate"
    input_data = "Test task for Weaviate integration"
    classification = "idea"
    recommendation = "Implement this feature"
    vector = [0.1, 0.2, 0.3, 0.4, 0.5] * 156  # 780-dimensional vector

    # Add task embedding
    result = weaviate_client.add_task_embedding(
        task_id,
        input_data,
        classification,
        recommendation,
        vector
    )
    assert result is True

    # Retrieve the task
    retrieved_task = weaviate_client.get_task_by_id(task_id)
    assert retrieved_task is not None
    assert retrieved_task["task_id"] == task_id
    assert retrieved_task["input_data"] == input_data

    # Search for similar tasks
    similar_tasks = weaviate_client.search_similar_tasks(vector, limit=3)
    assert len(similar_tasks) >= 1
    assert similar_tasks[0]["task_id"] == task_id

@pytest.mark.skip(reason="Weaviate integration test - requires running Weaviate instance")
def test_weaviate_vector_search():
    """Test vector search functionality in Weaviate"""
    # Create schema first
    weaviate_client.create_schema()

    # Test data - add multiple tasks
    vectors = [
        [0.1, 0.2, 0.3, 0.4, 0.5] * 156,
        [0.2, 0.3, 0.4, 0.5, 0.6] * 156,
        [0.3, 0.4, 0.5, 0.6, 0.7] * 156
    ]

    for i, vector in enumerate(vectors):
        weaviate_client.add_task_embedding(
            f"test_task_{i}",
            f"Test task {i}",
            "idea",
            f"Recommendation {i}",
            vector
        )

    # Search with the first vector
    results = weaviate_client.search_similar_tasks(vectors[0], limit=2)

    # Verify results
    assert len(results) >= 2
    assert results[0]["task_id"] == "test_task_0"




