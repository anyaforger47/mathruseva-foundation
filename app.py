from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import mysql.connector
import os
from datetime import datetime
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️ ReportLab not available. PDF generation will be disabled.")

app = Flask(__name__)

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

# Simple users for authentication
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Administrator'}
}

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
            
            cursor.close()
            conn.close()
            
            stats = {
                'total_volunteers': total_volunteers,
                'total_camps': total_camps,
                'total_donations': total_donations,
                'present_today': present_today,
                'absent_today': 0,
                'late_today': 0,
                'attendance_rate': 100 if present_today > 0 else 0
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

@app.route('/api/volunteers', methods=['GET', 'POST'])
def volunteers_api():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM volunteers")
                volunteers = cursor.fetchall()
                cursor.close()
                conn.close()
                
                # Convert to list of dictionaries
                volunteer_list = []
                for volunteer in volunteers:
                    volunteer_list.append({
                        'id': volunteer[0],
                        'name': volunteer[1],
                        'email': volunteer[2], 
                        'phone': volunteer[3],
                        'role': volunteer[4],
                        'status': volunteer[5],
                        'join_date': str(volunteer[6])
                    })
                
                return jsonify({'volunteers': volunteer_list})
            else:
                return jsonify({'volunteers': []})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO volunteers (name, email, phone, role, status, join_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (data['name'], data['email'], data['phone'], data['role'], data['status'], data['join_date']))
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Volunteer added successfully'})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/camps', methods=['GET', 'POST'])
def camps_api():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM camps")
                camps = cursor.fetchall()
                cursor.close()
                conn.close()
                
                # Convert to list of dictionaries
                camp_list = []
                for camp in camps:
                    camp_list.append({
                        'id': camp[0],
                        'name': camp[1],
                        'type': camp[2],
                        'location': camp[3],
                        'camp_date': str(camp[4]),
                        'description': camp[5],
                        'status': camp[6]
                    })
                
                return jsonify({'camps': camp_list})
            else:
                return jsonify({'camps': []})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO camps (name, type, location, camp_date, description, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (data['name'], data['type'], data['location'], data['camp_date'], data['description'], data['status']))
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Camp added successfully'})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/donations', methods=['GET', 'POST'])
def donations_api():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM donations")
                donations = cursor.fetchall()
                cursor.close()
                conn.close()
                
                # Convert to list of dictionaries
                donation_list = []
                for donation in donations:
                    donation_list.append({
                        'id': donation[0],
                        'donation_type': donation[1],
                        'quantity': donation[2],
                        'amount': donation[3],
                        'donor_name': donation[4],
                        'donation_date': str(donation[5])
                    })
                
                return jsonify({'donations': donation_list})
            else:
                return jsonify({'donations': []})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO donations (donation_type, quantity, amount, donor_name, donation_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (data['donation_type'], data['quantity'], data['amount'], data['donor_name'], data['donation_date']))
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Donation added successfully'})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/media', methods=['GET', 'POST'])
def media_api():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM media ORDER BY upload_date DESC")
                media_files = cursor.fetchall()
                cursor.close()
                conn.close()
                
                # Convert to list of dictionaries
                media_list = []
                for media in media_files:
                    media_list.append({
                        'id': media[0],
                        'filename': media[1],
                        'file_type': media[2],
                        'camp_id': media[3],
                        'upload_date': str(media[4]),
                        'file_path': media[5]
                    })
                
                return jsonify({'media': media_list})
            else:
                return jsonify({'media': []})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            # Handle file upload
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            camp_id = request.form.get('camp_id')
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save file logic here
            filename = file.filename
            file_type = filename.split('.')[-1].lower()
            
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO media (filename, file_type, camp_id, upload_date, file_path)
                    VALUES (%s, %s, %s, %s, %s)
                """, (filename, file_type, camp_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f'/static/uploads/{filename}'))
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Media uploaded successfully'})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def analytics_api():
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            # Get monthly volunteer trends
            cursor.execute("""
                SELECT DATE_FORMAT(join_date, '%Y-%m') as month, COUNT(*) as count 
                FROM volunteers 
                WHERE join_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
                GROUP BY DATE_FORMAT(join_date, '%Y-%m')
                ORDER BY month
            """)
            volunteer_trends = cursor.fetchall()
            
            # Get camp statistics by type
            cursor.execute("""
                SELECT type, COUNT(*) as count 
                FROM camps 
                GROUP BY type
            """)
            camp_stats = cursor.fetchall()
            
            # Get donation trends
            cursor.execute("""
                SELECT DATE_FORMAT(donation_date, '%Y-%m') as month, SUM(amount) as total
                FROM donations 
                WHERE donation_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
                GROUP BY DATE_FORMAT(donation_date, '%Y-%m')
                ORDER BY month
            """)
            donation_trends = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'volunteer_trends': [{'month': row[0], 'count': row[1]} for row in volunteer_trends],
                'camp_stats': [{'type': row[0], 'count': row[1]} for row in camp_stats],
                'donation_trends': [{'month': row[0], 'total': float(row[1])} for row in donation_trends]
            })
    except Exception as e:
        print(f"❌ Analytics API Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/volunteers/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM volunteers WHERE id = %s", (volunteer_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Volunteer deleted successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/camps/<int:camp_id>', methods=['DELETE'])
def delete_camp(camp_id):
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            # First check if camp has related records
            cursor.execute("SELECT COUNT(*) FROM volunteer_attendance WHERE camp_id = %s", (camp_id,))
            attendance_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM camp_media WHERE camp_id = %s", (camp_id,))
            media_count = cursor.fetchone()[0]
            
            if attendance_count > 0 or media_count > 0:
                cursor.close()
                conn.close()
                return jsonify({
                    'error': f'Cannot delete camp. It has {attendance_count} attendance records and {media_count} media files. Please delete these first or mark camp as completed instead.',
                    'has_dependencies': True,
                    'attendance_count': attendance_count,
                    'media_count': media_count
                }), 400
            
            # If no dependencies, proceed with deletion
            cursor.execute("DELETE FROM camps WHERE id = %s", (camp_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Camp deleted successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/donations/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM donations WHERE id = %s", (donation_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Donation deleted successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            # First get file path to delete physical file
            cursor.execute("SELECT file_path FROM media WHERE id = %s", (media_id,))
            result = cursor.fetchone()
            
            if result:
                file_path = result[0]
                # Delete from database
                cursor.execute("DELETE FROM media WHERE id = %s", (media_id,))
                conn.commit()
                
                # Note: Physical file deletion would require file system access
                # For now, we'll just remove from database
                
                cursor.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Media deleted successfully'})
            else:
                cursor.close()
                conn.close()
                return jsonify({'error': 'Media not found'}), 404
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/volunteers/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    try:
        data = request.get_json()
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE volunteers 
                SET name = %s, email = %s, phone = %s, role = %s, status = %s 
                WHERE id = %s
            """, (data['name'], data['email'], data['phone'], data['role'], data['status'], volunteer_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Volunteer updated successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/camps/<int:camp_id>', methods=['PUT'])
def update_camp(camp_id):
    try:
        data = request.get_json()
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE camps 
                SET name = %s, type = %s, location = %s, camp_date = %s, description = %s, status = %s 
                WHERE id = %s
            """, (data['name'], data['type'], data['location'], data['camp_date'], data['description'], data['status'], camp_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Camp updated successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/donations/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    try:
        data = request.get_json()
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE donations 
                SET donation_type = %s, quantity = %s, amount = %s, donor_name = %s, donation_date = %s 
                WHERE id = %s
            """, (data['donation_type'], data['quantity'], data['amount'], data['donor_name'], data['donation_date'], donation_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Donation updated successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['GET', 'POST'])
def attendance_api():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                
                # Get query parameters for filtering
                camp_id = request.args.get('camp_id')
                date_filter = request.args.get('date')
                
                # Build query based on filters
                query = """
                    SELECT at.*, v.name as volunteer_name, c.name as camp_name 
                    FROM attendance_tracking at
                    LEFT JOIN volunteers v ON at.volunteer_id = v.id
                    LEFT JOIN camps c ON at.camp_id = c.id
                """
                params = []
                
                if camp_id:
                    query += " WHERE at.camp_id = %s"
                    params.append(camp_id)
                
                if date_filter:
                    if camp_id:
                        query += " AND at.attendance_date = %s"
                    else:
                        query += " WHERE at.attendance_date = %s"
                    params.append(date_filter)
                
                query += " ORDER BY at.attendance_date DESC, at.check_in_time DESC"
                
                cursor.execute(query, tuple(params) if params else ())
                attendance_records = cursor.fetchall()
                cursor.close()
                conn.close()
                
                # Convert to list of dictionaries
                attendance_list = []
                for record in attendance_records:
                    attendance_list.append({
                        'id': record[0],
                        'volunteer_id': record[1],
                        'camp_id': record[2],
                        'attendance_date': str(record[3]),
                        'check_in_time': str(record[4]) if record[4] else None,
                        'check_out_time': str(record[5]) if record[5] else None,
                        'status': record[6],
                        'notes': record[7],
                        'volunteer_name': record[10],
                        'camp_name': record[11]
                    })
                
                return jsonify({'attendance': attendance_list})
            else:
                return jsonify({'attendance': []})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO attendance_tracking (volunteer_id, camp_id, attendance_date, check_in_time, check_out_time, status, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    data['volunteer_id'], 
                    data.get('camp_id'), 
                    data['attendance_date'], 
                    data.get('check_in_time'), 
                    data.get('check_out_time'), 
                    data['status'], 
                    data.get('notes')
                ))
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Attendance marked successfully'})
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/<int:attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    try:
        data = request.get_json()
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attendance_tracking 
                SET volunteer_id = %s, camp_id = %s, attendance_date = %s, check_in_time = %s, check_out_time = %s, status = %s, notes = %s 
                WHERE id = %s
            """, (
                data['volunteer_id'], 
                data.get('camp_id'), 
                data['attendance_date'], 
                data.get('check_in_time'), 
                data.get('check_out_time'), 
                data['status'], 
                data.get('notes'), 
                attendance_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Attendance updated successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM attendance_tracking WHERE id = %s", (attendance_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Attendance record deleted successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/stats', methods=['GET'])
def attendance_stats_api():
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            
            # Get attendance statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(CASE WHEN status = 'present' THEN 1 END) as present_count,
                    COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_count,
                    COUNT(CASE WHEN status = 'late' THEN 1 END) as late_count,
                    COUNT(CASE WHEN status = 'excused' THEN 1 END) as excused_count,
                    COUNT(DISTINCT volunteer_id) as unique_volunteers,
                    COUNT(DISTINCT camp_id) as unique_camps
                FROM attendance_tracking
            """)
            stats = cursor.fetchone()
            
            # Get today's attendance
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT COUNT(*) as today_present
                FROM attendance_tracking
                WHERE attendance_date = %s AND status = 'present'
            """, (today,))
            today_stats = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'total_records': stats[0],
                'present_count': stats[1],
                'absent_count': stats[2],
                'late_count': stats[3],
                'excused_count': stats[4],
                'unique_volunteers': stats[5],
                'unique_camps': stats[6],
                'today_present': today_stats[0]
            })
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-pdf/<report_type>')
def generate_pdf_report(report_type):
    if not REPORTLAB_AVAILABLE:
        return jsonify({'error': 'PDF generation not available. ReportLab library is not installed.'}), 500
    
    try:
        conn = get_db()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get data based on report type
        if report_type == 'volunteers':
            cursor.execute("""
                SELECT v.name, v.email, v.phone, v.role, v.status, v.join_date
                FROM volunteers v
                ORDER BY v.join_date DESC
            """)
            data = cursor.fetchall()
            title = "Volunteers Report"
            headers = ['Name', 'Email', 'Phone', 'Role', 'Status', 'Join Date']
            
        elif report_type == 'camps':
            cursor.execute("""
                SELECT c.name, c.type, c.location, c.camp_date, c.status, c.description
                FROM camps c
                ORDER BY c.camp_date DESC
            """)
            data = cursor.fetchall()
            title = "Camps Report"
            headers = ['Camp Name', 'Type', 'Location', 'Date', 'Status', 'Description']
            
        elif report_type == 'donations':
            cursor.execute("""
                SELECT d.donation_type, d.quantity, d.amount, d.donor_name, d.donation_date
                FROM donations d
                ORDER BY d.donation_date DESC
            """)
            data = cursor.fetchall()
            title = "Donations Report"
            headers = ['Type', 'Quantity', 'Amount', 'Donor', 'Date']
            
        elif report_type == 'attendance':
            cursor.execute("""
                SELECT at.attendance_date, v.name as volunteer_name, c.name as camp_name, 
                       at.check_in_time, at.check_out_time, at.status, at.notes
                FROM attendance_tracking at
                LEFT JOIN volunteers v ON at.volunteer_id = v.id
                LEFT JOIN camps c ON at.camp_id = c.id
                ORDER BY at.attendance_date DESC
            """)
            data = cursor.fetchall()
            title = "Attendance Report"
            headers = ['Date', 'Volunteer', 'Camp', 'Check In', 'Check Out', 'Status', 'Notes']
            
        elif report_type == 'analytics':
            # Get comprehensive analytics data
            cursor.execute("SELECT COUNT(*) FROM volunteers")
            total_volunteers = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM camps")
            total_camps = cursor.fetchone()[0]
            
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM donations")
            total_donations = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(CASE WHEN status = 'present' THEN 1 END) as present,
                       COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent,
                       COUNT(CASE WHEN status = 'late' THEN 1 END) as late
                FROM attendance_tracking
            """)
            attendance_stats = cursor.fetchone()
            
            data = [
                ['Total Volunteers', total_volunteers],
                ['Total Camps', total_camps],
                ['Total Donations ($)', total_donations],
                ['Present', attendance_stats[0]],
                ['Absent', attendance_stats[1]],
                ['Late', attendance_stats[2]]
            ]
            title = "Analytics Summary Report"
            headers = ['Metric', 'Count']
            
        else:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid report type'}), 400
        
        cursor.close()
        conn.close()
        
        # Create PDF using ReportLab if available, otherwise use simple HTML
        if REPORTLAB_AVAILABLE:
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib.units import inch
                from reportlab.lib import colors
                
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=18)
                
                # Get styles
                styles = getSampleStyleSheet()
                title_style = styles['Heading1']
                normal_style = styles['Normal']
                
                # Add title
                doc.build([
                    Paragraph(title, title_style),
                    Spacer(1, 12),
                    Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style),
                    Spacer(1, 12),
                ])
                
                # Add table
                if report_type == 'analytics':
                    # Special formatting for analytics report
                    table_data = [[header, str(value)] for header, value in zip(headers, data)]
                else:
                    table_data = [headers] + [[str(item) if item is not None else '' for item in row] for row in data]
                
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.grey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                table.wrapOn = True
                doc.build([table])
                
                # Prepare file for download
                buffer.seek(0)
                filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
                return send_file(
                    buffer,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/pdf'
                )
                
            except Exception as e:
                print(f"ReportLab error: {e}")
                # Fallback to HTML if ReportLab fails
                pass
        
        # Fallback HTML approach (always works)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; font-weight: bold; }}
                .header-info {{ margin-bottom: 20px; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }}
                .footer {{ margin-top: 30px; padding: 10px; background-color: #f8f9fa; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header-info">
                <h1>{title}</h1>
                <p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Report Type:</strong> {report_type.replace('_', ' ').title()}</p>
            </div>
            
            <table>
                <tr>
        """
        
        # Add table headers
        for header in headers:
            html_content += f"<th>{header}</th>"
        html_content += "</tr>"
        
        # Add table data
        if report_type == 'analytics':
            for metric, value in data:
                html_content += f"<tr><td><strong>{metric}</strong></td><td>{value}</td></tr>"
        else:
            for row in data:
                html_content += "<tr>"
                for item in row:
                    html_content += f"<td>{str(item) if item is not None else ''}</td>"
                html_content += "</tr>"
        
        html_content += f"""
            </table>
            
            <div class="footer">
                <p><em>This report was generated from the Mathruseva Foundation Volunteer Management System.</em></p>
                <p><em>For any questions, please contact the system administrator.</em></p>
            </div>
        </body>
        </html>
        """
        
        # Create PDF response with proper headers
        response = make_response(html_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={report_type}_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response.headers['Content-Transfer-Encoding'] = 'binary'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/attendance/monthly')
def monthly_attendance_report():
    try:
        conn = get_db()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get monthly attendance data
        cursor.execute("""
            SELECT DATE_FORMAT(attendance_date, '%Y-%m') as month,
                   COUNT(*) as total_days,
                   COUNT(CASE WHEN status = 'present' THEN 1 END) as present_days,
                   COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_days,
                   COUNT(CASE WHEN status = 'late' THEN 1 END) as late_days
            FROM attendance_tracking
            WHERE attendance_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(attendance_date, '%Y-%m')
            ORDER BY month DESC
        """)
        monthly_data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({'monthly_attendance': monthly_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent-activity')
def recent_activity():
    try:
        conn = get_db()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get recent activities from all tables
        activities = []
        
        # Recent volunteers (last 5)
        cursor.execute("""
            SELECT 'volunteer' as activity_type, name, email, join_date as activity_date, 
                   'New volunteer joined' as activity_description
            FROM volunteers 
            ORDER BY join_date DESC 
            LIMIT 5
        """)
        volunteer_activities = cursor.fetchall()
        for activity in volunteer_activities:
            activities.append({
                'type': 'volunteer',
                'title': activity[1],
                'description': activity[2],
                'date': activity[3].strftime('%Y-%m-%d %H:%M'),
                'badge': 'success'
            })
        
        # Recent camps (last 5)
        cursor.execute("""
            SELECT 'camp' as activity_type, name, location, camp_date as activity_date,
                   'New camp created' as activity_description
            FROM camps 
            ORDER BY camp_date DESC 
            LIMIT 5
        """)
        camp_activities = cursor.fetchall()
        for activity in camp_activities:
            activities.append({
                'type': 'camp',
                'title': activity[1],
                'description': f"{activity[2]} - {activity[3]}",
                'date': activity[4].strftime('%Y-%m-%d %H:%M'),
                'badge': 'info'
            })
        
        # Recent donations (last 5)
        cursor.execute("""
            SELECT 'donation' as activity_type, donor_name, amount, donation_date as activity_date,
                   CONCAT('Donation of ', donation_type, ' ($', amount, ')') as activity_description
            FROM donations 
            ORDER BY donation_date DESC 
            LIMIT 5
        """)
        donation_activities = cursor.fetchall()
        for activity in donation_activities:
            activities.append({
                'type': 'donation',
                'title': activity[1],
                'description': activity[2],
                'date': activity[3].strftime('%Y-%m-%d %H:%M'),
                'badge': 'warning'
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({'activities': activities})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/monthly-donations')
def monthly_donations():
    try:
        conn = get_db()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get monthly donation totals
        cursor.execute("""
            SELECT DATE_FORMAT(donation_date, '%Y-%m') as month,
                   COUNT(*) as donation_count,
                   COALESCE(SUM(amount), 0) as total_amount
            FROM donations 
            WHERE donation_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(donation_date, '%Y-%m')
            ORDER BY month DESC
        """)
        monthly_data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({'monthly_donations': monthly_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    return render_template('test_volunteer.html')

if __name__ == '__main__':
    app.secret_key = 'mathruseva_foundation_2024_secure_key'
    print("🚀 Starting Mathruseva Foundation app...")
    print("📍 Running at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
