import os
import psycopg2

# Test connection to Supabase directly
def test_supabase_connection():
    try:
        print("Testing Supabase connection...")
        print(f"Host: {os.environ.get('DB_HOST')}")
        print(f"User: {os.environ.get('DB_USER')}")
        print(f"Database: {os.environ.get('DB_NAME')}")
        
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=5432
        )
        
        print("✅ Connected to Supabase successfully!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL version: {version}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()
