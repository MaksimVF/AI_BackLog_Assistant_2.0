
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.api.main import app






def test_app_creation():
    assert app is not None
    assert app.title == "AI Backlog Assistant API"
    assert app.version == "0.1.0"






def test_routes_exist():
    # Basic test to ensure the app has routes
    routes = [route for route in app.routes]
    root_route = next((route for route in routes if route.path == "/"), None)
    health_route = next((route for route in routes if route.path == "/health"), None)

    assert root_route is not None
    assert health_route is not None
