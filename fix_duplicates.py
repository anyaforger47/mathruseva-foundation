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

def check_and_fix_duplicates():
    try:
        print("🔍 Connecting to database...")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Check for duplicate emails
        cursor.execute("""
            SELECT email, COUNT(*) as count 
            FROM volunteers 
            GROUP BY email 
            HAVING count > 1
        """)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"🔍 Found {len(duplicates)} duplicate emails:")
            for email, count in duplicates:
                print(f"  - {email}: {count} entries")
            
            # Keep the first entry, delete duplicates
            cursor.execute("""
                DELETE v1 FROM volunteers v1
                INNER JOIN volunteers v2 
                WHERE v1.id > v2.id 
                AND v1.email = v2.email
            """)
            
            print("✅ Removed duplicate entries")
        else:
            print("✅ No duplicate emails found")
        
        # Show all current volunteers
        cursor.execute("SELECT id, name, email FROM volunteers ORDER BY id")
        volunteers = cursor.fetchall()
        
        print(f"\n📋 Current volunteers ({len(volunteers)}):")
        for vol_id, name, email in volunteers:
            print(f"  ID: {vol_id}, Name: {name}, Email: {email}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 Database check completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_and_fix_duplicates()
