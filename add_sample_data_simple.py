import mysql.connector
import os
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'), 
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306
}

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return None

def add_sample_data():
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            print("🎁 Adding sample data...")
            
            # Add sample volunteers
            volunteers_data = [
                ('John Doe', 'john.doe@example.com', '9876543210', 'Helper', 'Active', '2024-01-15'),
                ('Jane Smith', 'jane.smith@example.com', '9876543211', 'Organizer', 'Active', '2024-01-20'),
                ('Mike Johnson', 'mike.johnson@example.com', '9876543212', 'Coordinator', 'Active', '2024-01-25'),
                ('Sarah Wilson', 'sarah.wilson@example.com', '9876543213', 'Helper', 'Active', '2024-02-01'),
            ]
            
            for name, email, phone, role, status, join_date in volunteers_data:
                cursor.execute("""
                    INSERT INTO volunteers (name, email, phone, role, status, join_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, email, phone, role, status, join_date))
                print(f"✅ Added volunteer: {name}")
            
            # Add sample camps
            camps_data = [
                ('Eye Camp 2024', 'Eye Camp', 'Community Center', '2024-02-15', 'Completed'),
                ('Blood Donation Drive', 'Blood Donation', 'Hospital', '2024-02-20', 'Completed'),
                ('Health Checkup', 'General Health', 'School', '2024-02-25', 'Upcoming'),
            ]
            
            for name, type, location, date, status in camps_data:
                cursor.execute("""
                    INSERT INTO camps (name, type, location, camp_date, description, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, type, location, date, 'Free health camp for community', status))
                print(f"✅ Added camp: {name}")
            
            # Add sample donations
            donations_data = [
                ('Books', 50, 'Local Library', '2024-01-10'),
                ('Notebooks', 100, 'Stationery Store', '2024-01-15'),
                ('Pencils', 200, 'School Supply', '2024-02-05'),
                ('Food Packets', 30, 'Community Kitchen', '2024-02-10'),
            ]
            
            for type, quantity, donor, date in donations_data:
                cursor.execute("""
                    INSERT INTO donations (camp_id, donation_type, quantity, donor_name, donation_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (None, type, quantity, donor, date))
                print(f"✅ Added donation: {type} - {quantity}")
            
            # Add sample attendance
            attendance_data = [
                (1, 1, '2024-02-15', '09:00:00', None, 'present', 'Attended eye camp'),
                (2, 1, '2024-02-15', '09:30:00', None, 'present', 'Attended eye camp'),
                (3, 2, '2024-02-20', '10:00:00', '17:00:00', 'late', 'Attended blood donation'),
                (4, 1, '2024-02-25', '09:00:00', None, 'present', 'Attended health checkup'),
                (5, 2, '2024-02-25', '09:15:00', None, 'present', 'Attended health checkup'),
            ]
            
            for volunteer_id, camp_id, date, check_in, check_out, status, notes in attendance_data:
                cursor.execute("""
                    INSERT INTO volunteer_attendance (volunteer_id, camp_id, attendance_date, check_in_time, check_out_time, status, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (volunteer_id, camp_id, date, check_in, check_out, status, notes))
                print(f"✅ Added attendance: Volunteer {volunteer_id} on {date}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("🎉 Sample data added successfully!")
            print("📊 Summary:")
            print("  - Volunteers: " + str(len(volunteers_data)) + " added")
            print("  - Camps: " + str(len(camps_data)) + " added") 
            print("  - Donations: " + str(len(donations_data)) + " added")
            print("  - Attendance records: " + str(len(attendance_data)) + " added")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    if __name__ == '__main__':
        print("🚀 Adding sample data to Mathruseva Foundation database...")
        add_sample_data()
