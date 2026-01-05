"""
Comprehensive test suite to identify all issues in the Voice Safe application
"""
import requests
import json
from datetime import datetime
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://127.0.0.1:8001/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_server_health():
    """Test if server is running"""
    print_section("1. SERVER HEALTH CHECK")
    try:
        response = requests.get("http://127.0.0.1:8001/ping", timeout=5)
        if response.status_code == 200:
            print("[OK] Server is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"[FAIL] Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Server is NOT running")
        print("   Please start the server with: uvicorn backend.main:app --reload --port 8001")
        return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_user_signup():
    """Test user registration"""
    print_section("2. USER SIGNUP TEST")
    
    test_user = {
        "full_name": f"Test User {datetime.now().strftime('%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("[OK] User signup successful")
            data = response.json()
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Email: {data.get('email')}")
            return test_user
        else:
            print(f"[FAIL] Signup failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"[FAIL] Error during signup: {e}")
        return None

def test_user_login(user_data):
    """Test user login"""
    print_section("3. USER LOGIN TEST")
    
    if not user_data:
        print("[WARN] Skipping login test (no user data)")
        return None
    
    try:
        form_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        
        response = requests.post(
            f"{BASE_URL}/users/login",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            print("[OK] Login successful")
            data = response.json()
            token = data.get("access_token")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"[FAIL] Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"[FAIL] Error during login: {e}")
        return None

def test_get_issues():
    """Test fetching all issues"""
    print_section("4. GET ALL ISSUES TEST")
    
    try:
        response = requests.get(f"{BASE_URL}/issues")
        
        if response.status_code == 200:
            issues = response.json()
            print(f"[OK] Successfully fetched issues")
            print(f"   Total issues: {len(issues)}")
            if len(issues) > 0:
                print(f"   First issue: {issues[0].get('title', 'N/A')}")
            return issues
        else:
            print(f"[FAIL] Failed to fetch issues with status {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except Exception as e:
        print(f"[FAIL] Error fetching issues: {e}")
        return []

def test_create_issue(token):
    """Test creating a new issue"""
    print_section("5. CREATE ISSUE TEST")
    
    if not token:
        print("[WARN] Skipping issue creation (no auth token)")
        return None
    
    issue_data = {
        "category_name": "Harassment",
        "title": f"Test Issue {datetime.now().strftime('%H:%M:%S')}",
        "description": "This is a test issue created by the automated test suite.",
        "evidence_url": None
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/issues",
            json=issue_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 200:
            print("[OK] Issue created successfully")
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Issue ID: {data.get('issue_id')}")
            return data.get('issue_id')
        else:
            print(f"[FAIL] Failed to create issue with status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"[FAIL] Error creating issue: {e}")
        return None

def test_frontend_config():
    """Check frontend configuration"""
    print_section("6. FRONTEND CONFIGURATION CHECK")
    
    try:
        with open("frontend/js/config.js", "r") as f:
            content = f.read()
            if "8001" in content:
                print("[OK] Frontend configured for port 8001")
            else:
                print("[WARN] Frontend may not be configured for correct port")
            print(f"   Config content:\n{content}")
    except Exception as e:
        print(f"[FAIL] Error reading config: {e}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  VOICE SAFE - COMPREHENSIVE ERROR DIAGNOSIS")
    print("="*60)
    
    # Test 1: Server health
    server_ok = test_server_health()
    if not server_ok:
        print("\n[WARN] Cannot continue tests - server is not running")
        print("   Start server with: uvicorn backend.main:app --reload --port 8001")
        return
    
    # Test 2: User signup
    user_data = test_user_signup()
    
    # Test 3: User login
    token = test_user_login(user_data)
    
    # Test 4: Get issues
    issues = test_get_issues()
    
    # Test 5: Create issue
    issue_id = test_create_issue(token)
    
    # Test 6: Frontend config
    test_frontend_config()
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"Server Running:     {'[OK]' if server_ok else '[FAIL]'}")
    print(f"User Signup:        {'[OK]' if user_data else '[FAIL]'}")
    print(f"User Login:         {'[OK]' if token else '[FAIL]'}")
    print(f"Get Issues:         [OK] ({len(issues)} issues)")
    print(f"Create Issue:       {'[OK]' if issue_id else '[FAIL]'}")
    
    print("\n" + "="*60)
    print("  DIAGNOSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
