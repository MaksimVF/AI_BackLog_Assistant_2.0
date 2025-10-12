



"""
Test API Endpoints
"""

import requests
import json
from fastapi.testclient import TestClient
from src.api.main import app

def test_api_endpoints():
    """Test the API endpoints"""
    # Create a test client
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Backlog Assistant API is running" in response.json()["message"]
    print("✅ Root endpoint test passed")

    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health endpoint test passed")

    # Test tasks endpoint
    task_data = {"input_data": "Implement user authentication"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert "result" in response.json()
    print("✅ Tasks endpoint test passed")

    # Test triggers endpoint
    response = client.get("/triggers")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "trigger_id" in response.json()[0]
    print("✅ Triggers endpoint test passed")

    # Test Telegram message endpoint
    telegram_data = {"message_text": "Implement user authentication"}
    response = client.post("/telegram/message", json=telegram_data)
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert "status" in response.json()
    print("✅ Telegram message endpoint test passed")

    # Test Telegram status endpoint
    response = client.get("/telegram/status/123")
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert "status" in response.json()
    print("✅ Telegram status endpoint test passed")

    # Test Telegram tasks endpoint
    response = client.get("/telegram/tasks")
    assert response.status_code == 200
    assert "tasks" in response.json()
    assert len(response.json()["tasks"]) > 0
    print("✅ Telegram tasks endpoint test passed")

    # Test Telegram archive endpoint
    response = client.get("/telegram/archive/123")
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert "original_input" in response.json()
    print("✅ Telegram archive endpoint test passed")

    print("✅ All API endpoint tests passed!")

if __name__ == "__main__":
    test_api_endpoints()
