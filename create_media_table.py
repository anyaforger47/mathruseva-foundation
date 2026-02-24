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

print("🔧 Creating missing media table...")

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Create media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            camp_id INT NULL,
            upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_path VARCHAR(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (camp_id) REFERENCES camps(id) ON DELETE SET NULL
        )
    """)
    
    conn.commit()
    print("✅ Media table created successfully!")
    
    # Verify table exists
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    print(f"📋 Updated tables: {tables}")
    
    cursor.close()
    conn.close()
    
    print("✅ Database schema updated successfully!")
    
except Exception as e:
    print(f"❌ Error creating media table: {e}")
