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

def check_tables():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=== CHECKING CAMPS TABLE STRUCTURE ===")
        cursor.execute("DESCRIBE camps")
        camps_columns = cursor.fetchall()
        print("Camps table columns:")
        for column in camps_columns:
            print(f"  - {column[0]} ({column[1]})")
        
        print("\n=== CHECKING DONATIONS TABLE STRUCTURE ===")
        cursor.execute("DESCRIBE donations")
        donations_columns = cursor.fetchall()
        print("Donations table columns:")
        for column in donations_columns:
            print(f"  - {column[0]} ({column[1]})")
        
        print("\n=== CHECKING VOLUNTEERS TABLE STRUCTURE ===")
        cursor.execute("DESCRIBE volunteers")
        volunteers_columns = cursor.fetchall()
        print("Volunteers table columns:")
        for column in volunteers_columns:
            print(f"  - {column[0]} ({column[1]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_tables()
