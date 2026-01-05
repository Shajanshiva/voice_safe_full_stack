"""
Test to check if login returns user_id
"""
import requests

BASE_URL = "http://127.0.0.1:8001/api"

# Create a test user
test_user = {
    "full_name": "Debug User",
    "email": "debug@test.com",
    "password": "testpass123"
}

print("Creating test user...")
try:
    response = requests.post(f"{BASE_URL}/users", json=test_user)
    print(f"Signup status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"User created: {user_data}")
except Exception as e:
    print(f"Signup error (user may already exist): {e}")

# Try to login
print("\nAttempting login...")
form_data = {
    "username": test_user["email"],
    "password": test_user["password"]
}

response = requests.post(
    f"{BASE_URL}/users/login",
    data=form_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

print(f"Login status: {response.status_code}")
login_data = response.json()
print(f"Login response: {login_data}")

# Check if user_id is in the response
if "user_id" in login_data:
    print(f"\n[OK] user_id found in login response: {login_data['user_id']}")
else:
    print(f"\n[ISSUE] user_id NOT in login response")
    print("This may cause issues with frontend localStorage")
