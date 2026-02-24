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

print("🔧 Creating attendance module table...")

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Create attendance_tracking table (separate from existing volunteer_attendance)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_tracking (
            id INT AUTO_INCREMENT PRIMARY KEY,
            volunteer_id INT NOT NULL,
            camp_id INT NULL,
            attendance_date DATE NOT NULL,
            check_in_time TIME NULL,
            check_out_time TIME NULL,
            status ENUM('present', 'absent', 'late', 'excused') DEFAULT 'present',
            notes TEXT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
            FOREIGN KEY (camp_id) REFERENCES camps(id) ON DELETE SET NULL
        )
    """)
    
    conn.commit()
    print("✅ Attendance tracking table created successfully!")
    
    # Verify table exists
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    print(f"📋 Updated tables: {tables}")
    
    cursor.close()
    conn.close()
    
    print("✅ Attendance module database setup completed!")
    
except Exception as e:
    print(f"❌ Error creating attendance table: {e}")
