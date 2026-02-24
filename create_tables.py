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

def check_and_create_tables():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check existing tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 Existing tables: {tables}")
        
        # Create volunteer_attendance table if it doesn't exist
        if 'volunteer_attendance' not in tables:
            print("🔧 Creating volunteer_attendance table...")
            cursor.execute("""
                CREATE TABLE volunteer_attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    volunteer_id INT,
                    camp_id INT,
                    attendance_date DATE,
                    check_in_time TIME,
                    check_out_time TIME,
                    status VARCHAR(20),
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id),
                    FOREIGN KEY (camp_id) REFERENCES camps(id)
                )
            """)
            print("✅ volunteer_attendance table created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("🎉 Table check and creation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_and_create_tables()
