import requests
import json

def test_donation_api():
    url = "http://127.0.0.1:5000/api/donations"
    
    # Test data
    donation_data = {
        "camp_id": None,
        "donation_type": "Books",
        "quantity": 10,
        "donor": "Test Donor",
        "donation_date": "2024-02-19"
    }
    
    try:
        print("🧪 Testing donation API...")
        print(f"📤 Sending data: {donation_data}")
        
        response = requests.post(url, json=donation_data)
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        print(f"📥 Response text: {response.text}")
        
        if response.status_code == 200:
            response_json = response.json()
            print(f"✅ Response JSON: {response_json}")
            
            if response_json.get('success'):
                print("✅ Donation API working perfectly!")
            else:
                print(f"❌ API returned error: {response_json.get('error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == '__main__':
    test_donation_api()
