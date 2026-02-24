import mysql.connector
import os

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'), 
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306
}

def check_camps_table():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("DESCRIBE camps")
        columns = cursor.fetchall()
        
        print("📋 Camps table structure:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        # Check existing data
        cursor.execute("SELECT * FROM camps LIMIT 3")
        data = cursor.fetchall()
        
        print(f"\n📊 Sample data ({len(data)} rows):")
        for row in data:
            print(f"  {row}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_camps_table()
