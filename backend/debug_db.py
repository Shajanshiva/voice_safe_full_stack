from backend.database import engine, Base, session
from backend.models import User
from sqlalchemy import inspect, text
import os

def debug_db():
    print("--- DEBUGGING DATABASE ---")
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL is missing!")
        return
    
    # Hide password in logs
    safe_url = db_url.split("@")[-1] if "@" in db_url else "..."
    print(f"Connecting to: ...@{safe_url}")

    try:
        with engine.connect() as connection:
            # Check DB Name
            db_name = connection.execute(text("SELECT current_database();")).scalar()
            print(f"\n[1] Connected to Database: '{db_name}'")
            
            # Check Schema
            schema = connection.execute(text("SELECT current_schema();")).scalar()
            print(f"[2] Current Schema: '{schema}'")

            # Force create tables again (idempotent)
            print("\n[3] Running create_all()...")
            Base.metadata.create_all(bind=engine)
            
            # List Tables
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"\n[4] Tables found in public schema: {tables}")
            
            if "users" not in tables:
                print("!!! CRITICAL: 'users' table is MISSING even after create_all() !!!")
                return

            # Test Insert
            print("\n[5] Attempting to insert a test user...")
            db = session()
            try:
                # Check if user exists first to avoid unique constraint error
                existing = db.query(User).filter(User.email == "debug_test@example.com").first()
                if not existing:
                    new_user = User(
                        full_name="Debug User",
                        email="debug_test@example.com",
                        password="hashed_secret_password"
                    )
                    db.add(new_user)
                    db.commit()
                    print(f"SUCCESS: Created user with ID: {new_user.user_id}")
                else:
                    print(f"SUCCESS: Test user already exists (ID: {existing.user_id})")
            except Exception as e:
                print(f"INSERT FAILED: {e}")
            finally:
                db.close()

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

if __name__ == "__main__":
    debug_db()
