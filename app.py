from flask import Flask, request, jsonify, render_template, send_file
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NehaJ@447747',  # Replace with your MySQL root password
    'database': 'mathruseva_foundation'
}

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Serve frontend
@app.route('/')
def index():
    return render_template('index.html')

# Volunteer Management APIs
@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM volunteers ORDER BY join_date DESC")
    volunteers = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(volunteers)

@app.route('/api/volunteers', methods=['POST'])
def add_volunteer():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO volunteers (name, email, phone, role) 
        VALUES (%s, %s, %s, %s)
    """, (data['name'], data['email'], data['phone'], data['role']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Volunteer added successfully'})

@app.route('/api/volunteers/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE volunteers 
        SET name = %s, email = %s, phone = %s, role = %s, status = %s
        WHERE id = %s
    """, (data['name'], data['email'], data['phone'], data['role'], data['status'], volunteer_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Volunteer updated successfully'})

@app.route('/api/volunteers/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM volunteers WHERE id = %s", (volunteer_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Volunteer deleted successfully'})

# Camp Management APIs
@app.route('/api/camps', methods=['GET'])
def get_camps():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM camps ORDER BY camp_date DESC")
    camps = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(camps)

@app.route('/api/camps', methods=['POST'])
def add_camp():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO camps (name, type, location, camp_date, description) 
        VALUES (%s, %s, %s, %s, %s)
    """, (data['name'], data['type'], data['location'], data['camp_date'], data.get('description', '')))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Camp added successfully'})

@app.route('/api/camps/<int:camp_id>', methods=['PUT'])
def update_camp(camp_id):
    print(f"Received update request for camp ID: {camp_id}")
    data = request.get_json()
    print(f"Received data: {data}")
    
    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE camps 
            SET name = %s, type = %s, location = %s, camp_date = %s, description = %s, status = %s
            WHERE id = %s
        """, (data['name'], data['type'], data['location'], data['camp_date'], data.get('description', ''), data.get('status', 'Planned'), camp_id))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully updated camp {camp_id}")
        return jsonify({'message': 'Camp updated successfully'})
    except Exception as e:
        print(f"Error updating camp: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/camps/<int:camp_id>', methods=['DELETE'])
def delete_camp(camp_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM camps WHERE id = %s", (camp_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Camp deleted successfully'})

# Medical Summary APIs
@app.route('/api/medical-summary', methods=['POST'])
def add_medical_summary():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO medical_summary 
        (camp_id, total_patients, eye_checkups, blood_donations, general_consultations, children_benefited, summary_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['camp_id'], data['total_patients'], data.get('eye_checkups', 0), 
          data.get('blood_donations', 0), data.get('general_consultations', 0),
          data.get('children_benefited', 0), data['summary_date'], data.get('notes', '')))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Medical summary added successfully'})

# Donation APIs
@app.route('/api/donations', methods=['GET'])
def get_donations():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT d.*, c.name as camp_name 
        FROM donations d 
        LEFT JOIN camps c ON d.camp_id = c.id 
        ORDER BY donation_date DESC
    """)
    donations = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(donations)

@app.route('/api/donations', methods=['POST'])
def add_donation():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO donations (camp_id, donation_type, quantity, donor_name, donation_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data.get('camp_id'), data['donation_type'], data['quantity'], 
          data.get('donor_name', ''), data['donation_date'], data.get('notes', '')))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Donation added successfully'})

@app.route('/api/donations/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    print(f"Received update request for donation ID: {donation_id}")
    data = request.get_json()
    print(f"Received data: {data}")
    
    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE donations 
            SET camp_id = %s, donation_type = %s, quantity = %s, donor_name = %s, donation_date = %s, notes = %s
            WHERE id = %s
        """, (data.get('camp_id'), data['donation_type'], data['quantity'], 
              data.get('donor_name', ''), data['donation_date'], data.get('notes', ''), donation_id))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully updated donation {donation_id}")
        return jsonify({'message': 'Donation updated successfully'})
    except Exception as e:
        print(f"Error updating donation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/donations/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM donations WHERE id = %s", (donation_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Donation deleted successfully'})

# Analytics Dashboard APIs
@app.route('/api/analytics/dashboard')
def get_dashboard_analytics():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Total counts
    cur.execute("SELECT COUNT(*) as total FROM volunteers")
    total_volunteers = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM camps")
    total_camps = cur.fetchone()['total']
    
    cur.execute("SELECT SUM(total_patients) as total FROM medical_summary")
    total_beneficiaries = cur.fetchone()['total'] or 0
    
    cur.execute("SELECT SUM(quantity) as total FROM donations")
    total_donations = cur.fetchone()['total'] or 0
    
    # Camp type distribution
    cur.execute("SELECT type, COUNT(*) as count FROM camps GROUP BY type")
    camp_types = cur.fetchall()
    
    # Monthly trends
    cur.execute("""
        SELECT DATE_FORMAT(camp_date, '%Y-%m') as month, COUNT(*) as camps
        FROM camps 
        WHERE camp_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(camp_date, '%Y-%m')
        ORDER BY month
    """)
    monthly_trends = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'total_volunteers': total_volunteers,
        'total_camps': total_camps,
        'total_beneficiaries': total_beneficiaries,
        'total_donations': total_donations,
        'camp_types': camp_types,
        'monthly_trends': monthly_trends
    })

# PDF Report Generation
@app.route('/api/reports/generate-pdf')
def generate_pdf_report():
    try:
        from utils.pdf_generator import generate_pdf_report
        import os
        from datetime import datetime
        
        # Use the same MySQL configuration
        pdf_path = generate_pdf_report(MYSQL_CONFIG)
        
        if pdf_path and os.path.exists(pdf_path):
            # Return the PDF file for download
            return send_file(pdf_path, as_attachment=True, download_name=f"impact_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        else:
            return jsonify({'error': 'Failed to generate PDF report'}), 500
            
    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
