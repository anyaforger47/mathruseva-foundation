import os
import mysql.connector
from flask import Flask

app = Flask(__name__)

# MySQL Configuration (matching app.py)
MYSQL_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306
}

def setup_database():
    """Create database and tables"""
    try:
        # Connect to MySQL server (without database first)
        config = MYSQL_CONFIG.copy()
        if 'database' in config:
            del config['database']
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        
        # Create tables with MySQL syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS volunteers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(20) NOT NULL,
                skills TEXT,
                availability TEXT,
                join_date DATE DEFAULT (CURRENT_DATE),
                status VARCHAR(20) DEFAULT 'Active'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camps (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                type VARCHAR(50) NOT NULL,
                location VARCHAR(200) NOT NULL,
                camp_date DATE NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'Planned'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_summary (
                id INT AUTO_INCREMENT PRIMARY KEY,
                camp_id INT,
                total_patients INT DEFAULT 0,
                eye_checkups INT DEFAULT 0,
                blood_donations INT DEFAULT 0,
                general_consultations INT DEFAULT 0,
                children_benefited INT DEFAULT 0,
                summary_date DATE DEFAULT (CURRENT_DATE),
                notes TEXT,
                FOREIGN KEY (camp_id) REFERENCES camps(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                camp_id INT,
                donation_type VARCHAR(50) NOT NULL,
                quantity INT NOT NULL,
                donor_name VARCHAR(100),
                donation_date DATE NOT NULL,
                notes TEXT,
                FOREIGN KEY (camp_id) REFERENCES camps(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camp_volunteers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                camp_id INT,
                volunteer_id INT,
                role VARCHAR(50) DEFAULT 'Helper',
                FOREIGN KEY (camp_id) REFERENCES camps(id),
                FOREIGN KEY (volunteer_id) REFERENCES volunteers(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camp_media (
                id INT AUTO_INCREMENT PRIMARY KEY,
                camp_id INT NOT NULL,
                media_type VARCHAR(10) NOT NULL,
                media_url VARCHAR(500) NOT NULL,
                caption TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (camp_id) REFERENCES camps(id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database and tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

@app.route('/setup-database')
def setup_database_route():
    if setup_database():
        return "✅ Database setup completed! You can now use the application."
    else:
        return "❌ Database setup failed. Check logs."

if __name__ == '__main__':
    setup_database()
