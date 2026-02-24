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

def test_donations_insert():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Test the exact insert statement
        print("🧪 Testing donations insert...")
        
        test_data = {
            'camp_id': None,
            'donation_type': 'Books',
            'quantity': 10,
            'donor': 'Test Donor',
            'donation_date': '2024-02-19'
        }
        
        cursor.execute("""
            INSERT INTO donations (camp_id, donation_type, quantity, donor_name, donation_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            test_data['camp_id'], test_data['donation_type'], test_data['quantity'], 
            test_data['donor'], test_data['donation_date']
        ))
        
        donation_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ Test donation added with ID: {donation_id}")
        
        # Check the record
        cursor.execute("SELECT * FROM donations WHERE id = %s", (donation_id,))
        record = cursor.fetchone()
        print(f"📋 Record: {record}")
        
        # Clean up
        cursor.execute("DELETE FROM donations WHERE id = %s", (donation_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("✅ Donations test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    test_donations_insert()
