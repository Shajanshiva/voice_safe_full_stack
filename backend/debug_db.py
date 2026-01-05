from backend.database import engine, Base
from backend import models
from sqlalchemy import inspect
import os

def debug_db():
    print("Checking database connection from code...")
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable is NOT set.")
        return

    print(f"DATABASE_URL is set (starts with {db_url.split(':')[0]}://...)")

    try:
        # Try connecting
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            
        # Try creating tables
        print("Attempting to create tables...")
        Base.metadata.create_all(bind=engine)
        print("create_all() executed.")

        # Inspect tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_db()
