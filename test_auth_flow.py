import requests
import json

# Test the complete authentication and API flow
BASE_URL = "https://codealpha-shopsphere-backend.onrender.com"

def test_authentication_flow():
    print("🔍 Testing Authentication Flow...\n")
    
    # Step 1: Test if endpoints are accessible
    print("1. Testing endpoint accessibility:")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        print(f"   Products endpoint: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/get_username")
        print(f"   Get username endpoint: {response.status_code} (expected 401)")
        
        response = requests.get(f"{BASE_URL}/get_cart_stat?cart_code=test123")
        print(f"   Get cart stat endpoint: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing endpoints: {e}")
        return
    
    # Step 2: Test user authentication
    print("\n2. Testing user authentication:")
    try:
        # Try to get token with debug user
        auth_data = {
            "username": "debuguser",
            "password": "debug123"
        }
        
        response = requests.post(
            f"{BASE_URL}/token/",
            headers={"Content-Type": "application/json"},
            json=auth_data
        )
        
        print(f"   Token request status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print(f"   ✅ Token received: {access_token[:20]}...")
            
            # Step 3: Test authenticated requests
            print("\n3. Testing authenticated requests:")
            
            # Test get_username with token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{BASE_URL}/get_username", headers=headers)
            print(f"   Get username with auth: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Username: {response.json()}")
            else:
                print(f"   ❌ Error: {response.text}")
                
            # Test cart endpoint with auth
            response = requests.get(
                f"{BASE_URL}/get_cart_stat?cart_code=test123", 
                headers=headers
            )
            print(f"   Get cart stat with auth: {response.status_code}")
            if response.status_code != 200:
                print(f"   Response: {response.text}")
                
        else:
            print(f"   ❌ Authentication failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error in authentication flow: {e}")

def test_cors():
    print("\n4. Testing CORS headers:")
    try:
        response = requests.options(f"{BASE_URL}/get_username")
        print(f"   OPTIONS request status: {response.status_code}")
        print(f"   Allow header: {response.headers.get('Allow', 'Not found')}")
        print(f"   CORS headers present: {'Access-Control-Allow-Origin' in response.headers}")
    except Exception as e:
        print(f"   ❌ Error testing CORS: {e}")

if __name__ == "__main__":
    test_authentication_flow()
    test_cors()
    print("\n📋 Test completed!")