from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import mysql.connector
from flask_cors import CORS
from functools import wraps
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Secret key for session management
app.secret_key = 'mathruseva_foundation_2024_secure_key'

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NehaJ@447747',  # Replace with your actual MySQL password
    'database': 'mathruseva_foundation'
}

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication (you can modify this to check against a database)
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

# Serve login page as default
@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Volunteer Management APIs
@app.route('/api/volunteers', methods=['GET'])
@login_required
def get_volunteers():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM volunteers ORDER BY join_date DESC")
    volunteers = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(volunteers)

@app.route('/api/volunteers', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
def get_camps():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM camps ORDER BY camp_date DESC")
    camps = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(camps)

@app.route('/api/camps', methods=['POST'])
@login_required
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
@login_required
def update_camp(camp_id):
    data = request.get_json()
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
    return jsonify({'message': 'Camp updated successfully'})

@app.route('/api/camps/<int:camp_id>', methods=['DELETE'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
def update_donation(donation_id):
    data = request.get_json()
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
    return jsonify({'message': 'Donation updated successfully'})

@app.route('/api/donations/<int:donation_id>', methods=['DELETE'])
@login_required
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
@login_required
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
@login_required
def generate_pdf_report():
    try:
        from utils.pdf_generator import generate_pdf_report
        
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
