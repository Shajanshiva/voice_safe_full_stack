import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def check_db_config():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found locally.")
        return

    try:
        parsed = urlparse(db_url)
        print(f"Local Host: {parsed.hostname}")
        print(f"Local Port: {parsed.port}")
        print(f"Local DB Name: {parsed.path[1:]}")
    except Exception as e:
        print(f"Error parsing URL: {e}")

if __name__ == "__main__":
    check_db_config()
