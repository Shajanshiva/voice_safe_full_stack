from backend.database import engine, Base
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy import text

def final_debug():
    print("--- FINAL AUTH DEBUG ---")
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("RESULT: DATABASE_URL is NOT found by load_dotenv().")
        return

    try:
        parsed = urlparse(db_url)
        print(f"RESULT: DATABASE_URL was found.")
        print(f"Parsed Host: {parsed.hostname}")
        print(f"Parsed Username: '{parsed.username}'")
        
        if parsed.username == "postgres":
            print("!!! WARNING: The username is 'postgres', but it should be 'postgres.gyjszumojxsamumwospj' !!!")
            print("Check if you have another .env file or if the line is correctly formatted.")
        
        print("\nAttempting connection test...")
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("SUCCESS: Connection established!")
            
    except Exception as e:
        print(f"CONNECTION FAILED: {e}")

if __name__ == "__main__":
    final_debug()
