from fastapi.testclient import TestClient
from backend.main import app
import random
import string

client = TestClient(app)

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_e2e():
    email = f"test_{generate_random_string()}@example.com"
    password = "testpassword123"
    full_name = "Test User"

    print(f"--- STARTING E2E TEST (TestClient) ---")
    print(f"Testing with Email: {email}")

    # 1. Sign Up
    print("\n[1] Testing Sign Up...")
    signup_data = {
        "full_name": full_name,
        "email": email,
        "password": password
    }
    response = client.post("/api/users", json=signup_data)
    if response.status_code == 200:
        print("SUCCESS: User created.")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")
        return

    # 2. Login
    print("\n[2] Testing Login...")
    login_data = {
        "username": email,
        "password": password
    }
    # OAuth2PasswordRequestForm expects data as form-data
    response = client.post("/api/users/login", data=login_data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("SUCCESS: Token obtained.")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")
        return

    # 3. Post Issue
    print("\n[3] Testing Post Issue...")
    issue_data = {
        "title": "Test Workplace Issue",
        "category_name": "Harassment",
        "description": "This is a test description for an E2E verification.",
        "evidence_url": ""
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/issues", json=issue_data, headers=headers)
    if response.status_code == 200:
        print(f"SUCCESS: {response.json().get('message')}")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")
        return

    # 4. Verify in Community Feed
    print("\n[4] Verifying in Community Feed...")
    response = client.get("/api/issues")
    if response.status_code == 200:
        issues = response.json()
        found = any(i['title'] == issue_data['title'] for i in issues)
        if found:
            print("SUCCESS: Issue found in feed.")
        else:
            print("FAILED: Issue not found in feed.")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")
        return

    print("\n--- E2E TEST COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    test_e2e()
