
import httpx
import json










def test_api():
    """Test the API with a simple request"""
    url = "http://localhost:8000/process"
    data = {
        "input_data": "This is a test idea for a new feature. We should add user profiles."
    }

    try:
        response = httpx.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
