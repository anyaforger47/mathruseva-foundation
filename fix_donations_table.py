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

def fix_donations_table():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=== ADDING AMOUNT COLUMN TO DONATIONS TABLE ===")
        cursor.execute("""
            ALTER TABLE donations 
            ADD COLUMN amount DECIMAL(10,2) DEFAULT 0.00
        """)
        conn.commit()
        print("✅ Amount column added to donations table successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    fix_donations_table()
