import requests
import json

def test_donations_api():
    url = "http://127.0.0.1:5000/api/donations"
    
    try:
        print("🧪 Testing donations API...")
        
        response = requests.get(url)
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_json = response.json()
            print(f"✅ Response JSON: {response_json}")
            
            if 'donations' in response_json:
                donations = response_json['donations']
                print(f"📋 Found {len(donations)} donations")
                for donation in donations:
                    print(f"  - {donation.get('donation_type', 'Unknown')}: {donation.get('quantity', 0)} from {donation.get('donor_name', 'Unknown')}")
            else:
                print("❌ No 'donations' key in response")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == '__main__':
    test_donations_api()
