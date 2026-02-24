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

def check_donations_table():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check donations table structure
        cursor.execute("DESCRIBE donations")
        columns = cursor.fetchall()
        
        print("📋 Donations table structure:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_donations_table()
