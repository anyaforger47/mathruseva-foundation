import mysql.connector
import os

# Test database connection
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'), 
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306
}

print("🔍 Testing database connection...")
print(f"Host: {DB_CONFIG['host']}")
print(f"User: {DB_CONFIG['user']}")
print(f"Database: {DB_CONFIG['database']}")
print(f"Port: {DB_CONFIG['port']}")

try:
    # First try to connect without specifying database
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )
    print("✅ Connected to MySQL server successfully!")
    
    # Check if database exists
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    print(f"📊 Available databases: {databases}")
    
    if DB_CONFIG['database'] in databases:
        print(f"✅ Database '{DB_CONFIG['database']}' exists!")
        
        # Try to connect to the specific database
        conn.close()
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 Tables in {DB_CONFIG['database']}: {tables}")
        
        # Check if required tables exist
        required_tables = ['volunteers', 'camps', 'donations', 'media']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
        else:
            print("✅ All required tables exist!")
            
        cursor.close()
        conn.close()
    else:
        print(f"❌ Database '{DB_CONFIG['database']}' does not exist!")
        print("💡 Available databases:", databases)
        
except mysql.connector.Error as e:
    print(f"❌ Database connection error: {e}")
    print("💡 Possible solutions:")
    print("   1. Check if MySQL server is running")
    print("   2. Verify password is correct")
    print("   3. Check if database exists")
    print("   4. Verify user permissions")
except Exception as e:
    print(f"❌ General error: {e}")
