from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'), 
    'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 3306
}

# Simple users for authentication
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Administrator'}
}

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            session['user_role'] = USERS[username]['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get real statistics
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            # Total volunteers
            cursor.execute("SELECT COUNT(*) FROM volunteers")
            total_volunteers = cursor.fetchone()[0]
            
            # Total camps
            cursor.execute("SELECT COUNT(*) FROM camps")
            total_camps = cursor.fetchone()[0]
            
            # Total donations
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM donations")
            total_donations = cursor.fetchone()[0]
            
            # Today's attendance
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM volunteer_attendance WHERE DATE(attendance_date) = %s AND status = 'present'", (today,))
            present_today = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM volunteer_attendance WHERE DATE(attendance_date) = %s AND status = 'absent'", (today,))
            absent_today = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM volunteer_attendance WHERE DATE(attendance_date) = %s AND status = 'late'", (today,))
            late_today = cursor.fetchone()[0]
            
            # Calculate attendance rate
            total_attendance = present_today + absent_today + late_today
            attendance_rate = round((present_today / total_attendance * 100)) if total_attendance > 0 else 0
            
            cursor.close()
            conn.close()
            
            stats = {
                'total_volunteers': total_volunteers,
                'total_camps': total_camps,
                'total_donations': total_donations,
                'present_today': present_today,
                'absent_today': absent_today,
                'late_today': late_today,
                'attendance_rate': attendance_rate
            }
        else:
            stats = {
                'total_volunteers': 0,
                'total_camps': 0,
                'total_donations': 0,
                'present_today': 0,
                'absent_today': 0,
                'late_today': 0,
                'attendance_rate': 0
            }
    except Exception as e:
        print(f"Error loading stats: {e}")
        stats = {
            'total_volunteers': 0,
            'total_camps': 0,
            'total_donations': 0,
            'present_today': 0,
            'absent_today': 0,
            'late_today': 0,
            'attendance_rate': 0
        }
    
    return render_template('index.html', stats=stats)

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# API Routes
@app.route('/api/volunteers', methods=['GET', 'POST', 'DELETE'])
def api_volunteers():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM volunteers ORDER BY id DESC")
                data = cursor.fetchall()
                cursor.close()
                conn.close()
                return jsonify({'volunteers': data})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            print("📤 POST volunteer request received")
            data = request.get_json()
            print(f"📤 Volunteer data: {data}")
            
            conn = get_db()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            
            # Check for duplicate email
            cursor.execute("SELECT id FROM volunteers WHERE email = %s", (data['email'],))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return jsonify({'error': 'Email already exists'}), 400
            
            # Insert volunteer
            cursor.execute("""
                INSERT INTO volunteers (name, email, phone, role, status, join_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data['name'],
                data['email'], 
                data.get('phone', ''),
                data['role'],
                'Active',
                data.get('join_date', datetime.now().strftime('%Y-%m-%d'))
            ))
            
            volunteer_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Added volunteer ID: {volunteer_id}")
            return jsonify({
                'success': True, 
                'message': 'Volunteer added successfully',
                'volunteer_id': volunteer_id
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            volunteer_id = data.get('id')
            
            if not volunteer_id:
                return jsonify({'error': 'Volunteer ID required'}), 400
                
            conn = get_db()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            cursor.execute("DELETE FROM volunteers WHERE id = %s", (volunteer_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Deleted volunteer ID: {volunteer_id}")
            return jsonify({
                'success': True, 
                'message': 'Volunteer deleted successfully'
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({'error': str(e)}), 500

@app.route('/api/camps', methods=['GET', 'POST'])
def api_camps():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM camps ORDER BY id DESC")
                data = cursor.fetchall()
                cursor.close()
                conn.close()
                return jsonify({'camps': data})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            conn = get_db()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO camps (name, type, location, camp_date, description, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data['name'], data['type'], data['location'], 
                data['camp_date'], data.get('description', ''), data['status']
            ))
            
            camp_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({
                'success': True, 
                'message': 'Camp added successfully',
                'camp_id': camp_id
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/donations', methods=['GET', 'POST', 'DELETE'])
def api_donations():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM donations ORDER BY id DESC")
                data = cursor.fetchall()
                cursor.close()
                conn.close()
                return jsonify({'donations': data})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            print("📤 POST donation request received")
            data = request.get_json()
            print(f"📤 Donation data: {data}")
            
            conn = get_db()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO donations (camp_id, donation_type, quantity, donor_name, donation_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data.get('camp_id'), data['donation_type'], data['quantity'], 
                data['donor'], data['donation_date']
            ))
            
            donation_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Added donation ID: {donation_id}")
            return jsonify({
                'success': True, 
                'message': 'Donation added successfully',
                'donation_id': donation_id
            })
            
        except Exception as e:
            print(f"❌ Donation POST Error: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            print("🗑️ DELETE donation request received")
            data = request.get_json()
            donation_id = data.get('id')
            
            if not donation_id:
                return jsonify({'error': 'Donation ID required'}), 400
                
            conn = get_db()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            cursor.execute("DELETE FROM donations WHERE id = %s", (donation_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Donation deleted with ID: {donation_id}")
            return jsonify({
                'success': True, 
                'message': 'Donation deleted successfully'
            })
            
        except Exception as e:
            print(f"❌ Donation DELETE Error: {e}")
            return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['GET', 'POST'])
def api_attendance():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT va.id, va.volunteer_id, va.camp_id, va.attendance_date, 
                           va.check_in_time, va.check_out_time, va.status, va.notes,
                           v.name as volunteer_name, c.name as camp_name 
                    FROM volunteer_attendance va
                    LEFT JOIN volunteers v ON va.volunteer_id = v.id
                    LEFT JOIN camps c ON va.camp_id = c.id
                    ORDER BY va.attendance_date DESC
                """)
                data = cursor.fetchall()
                
                # Convert all time objects to strings for JSON serialization
                for record in data:
                    for key, value in record.items():
                        if hasattr(value, '__str__') and not isinstance(value, str):
                            record[key] = str(value)
                
                cursor.close()
                conn.close()
                print(f"✅ Loaded {len(data)} attendance records")
                return jsonify({'attendance': data})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            print(f"❌ GET attendance error: {e}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            print("📤 POST attendance request received")
            data = request.get_json()
            print(f"📤 Attendance data: {data}")
            
            conn = get_db()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO volunteer_attendance (volunteer_id, camp_id, attendance_date, check_in_time, check_out_time, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data['volunteer_id'], data['camp_id'], data['date'], 
                data['check_in_time'], data.get('check_out_time'), data['status'], data.get('notes', '')
            ))
            
            attendance_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Attendance marked with ID: {attendance_id}")
            return jsonify({
                'success': True, 
                'message': 'Attendance marked successfully',
                'attendance_id': attendance_id
            })
            
        except Exception as e:
            print(f"❌ Attendance POST Error: {e}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.secret_key = 'mathruseva_foundation_2024_secure_key'
    print("🚀 Starting integrated Mathruseva Foundation app...")
    print("📍 Running at: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
