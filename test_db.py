import mysql.connector
import os

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306,
    'connect_timeout': 10
}

def test_database():
    print("🔍 Testing database connection...")
    print(f"Config: {MYSQL_CONFIG}")
    
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print("✅ Database connection successful!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM volunteers")
        count = cursor.fetchone()[0]
        print(f"📊 Current volunteer count: {count}")
        
        cursor.close()
        conn.close()
        print("✅ Database test completed successfully!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        print(f"❌ Error type: {type(e)}")
        
        # Try alternative connection
        print("\n🔄 Trying alternative connection...")
        try:
            alt_config = MYSQL_CONFIG.copy()
            alt_config['host'] = '127.0.0.1'  # Try localhost IP
            conn = mysql.connector.connect(**alt_config)
            print("✅ Alternative connection successful!")
            conn.close()
        except Exception as e2:
            print(f"❌ Alternative connection also failed: {e2}")

if __name__ == '__main__':
    test_database()
