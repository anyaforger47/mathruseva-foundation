import requests
import json

def test_volunteer_api():
    url = "http://127.0.0.1:5000/api/volunteers"
    
    # Test GET first
    print("🔍 Testing GET /api/volunteers...")
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"GET Error: {e}")
    
    # Test POST
    print("\n📤 Testing POST /api/volunteers...")
    data = {
        "name": "Test User",
        "email": "test123@example.com", 
        "phone": "1234567890",
        "role": "Helper",
        "status": "Active",
        "join_date": "2024-02-19"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"POST Error: {e}")

if __name__ == "__main__":
    test_volunteer_api()
