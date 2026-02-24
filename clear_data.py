from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306,
    'connect_timeout': 10
}

def check_and_clear_tables():
    try:
        print("🗑️  Connecting to database...")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # First, let's see what tables exist
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 Found tables: {tables}")
        
        print("\n🗑️  Clearing all existing data...")
        
        # Clear all tables (except we'll keep admin user in users table)
        for table in tables:
            if table == 'users':
                # Keep only admin user
                cursor.execute(f"DELETE FROM {table} WHERE username != 'admin'")
                print(f"✅ Cleared table: {table} (kept admin user)")
            else:
                cursor.execute(f"DELETE FROM {table}")
                print(f"✅ Cleared table: {table}")
        
        # Reset auto-increment counters
        for table in tables:
            if table != 'users':
                try:
                    cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
                    print(f"🔄 Reset auto-increment for: {table}")
                except:
                    print(f"⚠️  Could not reset auto-increment for: {table}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 All artificial data cleared successfully!")
        print("📊 Database is now clean and ready for your data!")
        print("👤 Admin user preserved: username='admin', password='admin123'")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")

if __name__ == '__main__':
    check_and_clear_tables()
