import requests

BASE_URL = "http://127.0.0.1:8000/api"

def test_signup_post():
    url = f"{BASE_URL}/users/"
    data = {
        "full_name": "Debug User",
        "email": "debug@example.com",
        "password": "password123"
    }
    print(f"Testing POST to {url}")
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_signup_post()
