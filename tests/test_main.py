
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.api.main import app

client = TestClient(app)




def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Backlog Assistant API is running"}




def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}
