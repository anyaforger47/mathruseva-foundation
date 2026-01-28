from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
from flask_cors import CORS
from functools import wraps
from datetime import datetime
import os
import psycopg2

app = Flask(__name__)
CORS(app)

# Secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'mathruseva_foundation_2024_secure_key')

# PostgreSQL Configuration for Render - FIXED VERSION
# Use Neon PostgreSQL connection
POSTGRES_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'mathruseva_user'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 5432,
    'connect_timeout': 10
}

# Alternative IPs to try if this doesn't work
SUPABASE_IPS = [
    '34.136.197.140',
    '34.136.197.141',
    '34.136.197.142',
    '34.136.197.143'
]

# Debug environment variables
print("=== ENVIRONMENT VARIABLES DEBUG ===")
print(f"DB_HOST: '{os.environ.get('DB_HOST', 'NOT_SET')}'")
print(f"DB_USER: '{os.environ.get('DB_USER', 'NOT_SET')}'")
print(f"DB_PASSWORD: '{os.environ.get('DB_PASSWORD', 'NOT_SET')}'")
print(f"DB_NAME: '{os.environ.get('DB_NAME', 'NOT_SET')}'")
print(f"SECRET_KEY: '{os.environ.get('SECRET_KEY', 'NOT_SET')}'")
print("=== END DEBUG ===")

def get_db_connection():
    try:
        print(f"Attempting to connect to: {POSTGRES_CONFIG['host']}")
        print(f"User: {POSTGRES_CONFIG['user']}")
        print(f"Database: {POSTGRES_CONFIG['database']}")
        print(f"Port: {POSTGRES_CONFIG['port']}")
        
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        print("✅ Database connection successful!")
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print(f"❌ Full config: {POSTGRES_CONFIG}")
        return None

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

# Simple test API to debug the issue
@app.route('/api/test')
def test_api():
    try:
        # Test basic response
        return jsonify({'message': 'API is working!', 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'error': f'Test failed: {str(e)}'}), 500

# Test multiple Supabase IPs
@app.route('/api/test-multiple-ips')
def test_multiple_ips():
    results = []
    
    for ip in SUPABASE_IPS:
        try:
            print(f"=== TESTING IP: {ip} ===")
            
            config = {
                'host': ip,
                'user': os.environ.get('DB_USER', 'postgres'),
                'password': os.environ.get('DB_PASSWORD', ''),
                'database': os.environ.get('DB_NAME', 'postgres'),
                'port': 5432,
                'connect_timeout': 5
            }
            
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            results.append({
                'ip': ip,
                'status': 'success',
                'message': f'Connected successfully to {ip}'
            })
            print(f"✅ SUCCESS: {ip}")
            
        except Exception as e:
            results.append({
                'ip': ip,
                'status': 'failed',
                'error': str(e)
            })
            print(f"❌ FAILED: {ip} - {str(e)}")
    
    return jsonify({
        'message': 'IP testing completed',
        'results': results
    })

# Get Supabase IP address
@app.route('/api/get-supabase-ip')
def get_supabase_ip():
    try:
        import subprocess
        import re
        
        # Try to get IP address using nslookup or dig
        host = 'db.jlcwxbkndfrtaoybvgsa.supabase.co'
        
        try:
            # Try nslookup first
            result = subprocess.run(['nslookup', host], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Extract IP from nslookup output
                ip_match = re.search(r'Address: (\d+\.\d+\.\d+\.\d+)', result.stdout)
                if ip_match:
                    ip = ip_match.group(1)
                    return jsonify({
                        'message': f'Found IP for {host}',
                        'ip_address': ip,
                        'method': 'nslookup'
                    })
        except:
            pass
        
        # Fallback to socket method
        import socket
        ip = socket.gethostbyname(host)
        return jsonify({
            'message': f'Found IP for {host}',
            'ip_address': ip,
            'method': 'socket'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Could not resolve IP for {host}',
            'details': str(e)
        }), 500

# Test hostname resolution
@app.route('/api/test-hostname')
def test_hostname():
    try:
        import socket
        host = 'db.jlcwxbkndfrtaoybvgsa.supabase.co'
        
        print(f"=== HOSTNAME RESOLUTION TEST ===")
        print(f"Testing hostname: {host}")
        
        # Try to resolve hostname
        ip_address = socket.gethostbyname(host)
        print(f"✅ Hostname resolved to: {ip_address}")
        
        return jsonify({
            'message': f'Hostname {host} resolved successfully',
            'ip_address': ip_address
        })
        
    except socket.gaierror as e:
        print(f"❌ Hostname resolution failed: {str(e)}")
        return jsonify({
            'error': f'Hostname resolution failed for {host}',
            'details': str(e)
        }), 500
    except Exception as e:
        print(f"❌ Hostname test failed: {str(e)}")
        return jsonify({'error': f'Hostname test failed: {str(e)}'}), 500

# Test network connectivity to Supabase
@app.route('/api/test-network')
def test_network():
    try:
        import socket
        host = 'db.jlcwxbkndfrtaoybvgsa.supabase.co'
        port = 5432
        
        print(f"=== NETWORK TEST START ===")
        print(f"Testing connection to {host}:{port}")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Network connection successful to {host}:{port}")
            return jsonify({'message': f'Network connection successful to {host}:{port}', 'result': 'success'})
        else:
            print(f"❌ Network connection failed to {host}:{port} - Error code: {result}")
            return jsonify({'error': f'Network connection failed to {host}:{port}', 'error_code': result}), 500
            
    except Exception as e:
        print(f"❌ Network test failed: {str(e)}")
        return jsonify({'error': f'Network test failed: {str(e)}'}), 500

# Test database connection
@app.route('/api/test-db')
def test_database():
    try:
        print("=== DATABASE CONNECTION TEST START ===")
        print(f"Environment variables loaded: {bool(os.environ.get('DB_HOST'))}")
        
        conn = get_db_connection()
        if not conn:
            print("❌ Connection returned None")
            return jsonify({'error': 'Database connection failed - returned None'}), 500
        
        print("✅ Connection object created successfully")
        
        cursor = conn.cursor()
        # Create media table for camp photos and videos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camp_media (
                id SERIAL PRIMARY KEY,
                camp_id INTEGER REFERENCES camps(id) ON DELETE CASCADE,
                media_type VARCHAR(10) NOT NULL, -- 'photo' or 'video'
                media_url VARCHAR(500) NOT NULL,
                caption TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Tables created successfully")
        
        cursor.execute("SELECT 1 as test")
        print("✅ Query executed successfully")
        
        result = cursor.fetchone()
        print(f"✅ Query result: {result}")
        
        cursor.close()
        conn.close()
        print("✅ Connection closed successfully")
        print("=== DATABASE CONNECTION TEST SUCCESS ===")
        
        return jsonify({'message': 'Database connection working!', 'result': result[0]})
        
    except Exception as e:
        print(f"❌ DATABASE CONNECTION TEST FAILED: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error details: {repr(e)}")
        print("=== DATABASE CONNECTION TEST FAILED ===")
        return jsonify({'error': f'Database test failed: {str(e)}'}), 500

# New test endpoint to force deployment
@app.route('/api/version')
def version_check():
    return jsonify({'version': '2.0', 'database': 'postgresql', 'timestamp': datetime.now().isoformat()})

# Health check for Render
@app.route('/health')
def health():
    try:
        # Test database connection
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({'status': 'healthy', 'database': 'postgresql', 'connection': 'ok'})
        else:
            return jsonify({'status': 'healthy', 'database': 'postgresql', 'connection': 'failed'})
    except Exception as e:
        return jsonify({'status': 'healthy', 'database': 'postgresql', 'connection': f'error: {str(e)}'})

# Database setup route
@app.route('/setup-database')
def setup_database():
    try:
        print("Starting database setup...")
        conn = get_db_connection()
        if not conn:
            print("❌ Database connection failed")
            return jsonify({'error': 'Database connection failed'}), 500
        
        print("✅ Database connected successfully")
        cursor = conn.cursor()
        
        # Create volunteers table first
        print("Creating volunteers table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS volunteers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(20) NOT NULL,
                join_date DATE DEFAULT CURRENT_DATE,
                status VARCHAR(20) DEFAULT 'Active'
            )
        """)
        print("✅ Volunteers table created")
        
        # Create camps table
        print("Creating camps table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camps (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                type VARCHAR(50) NOT NULL,
                location VARCHAR(200) NOT NULL,
                camp_date DATE NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'Planned'
            )
        """)
        print("✅ Camps table created")
        
        # Create donations table
        print("Creating donations table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id SERIAL PRIMARY KEY,
                camp_id INTEGER,
                donation_type VARCHAR(50) NOT NULL,
                quantity INTEGER NOT NULL,
                donor_name VARCHAR(100),
                donation_date DATE NOT NULL,
                notes TEXT
            )
        """)
        print("✅ Donations table created")
        
        # Create medical_summary table
        print("Creating medical_summary table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_summary (
                id SERIAL PRIMARY KEY,
                camp_id INTEGER,
                total_patients INTEGER DEFAULT 0,
                eye_checkups INTEGER DEFAULT 0,
                blood_donations INTEGER DEFAULT 0,
                general_consultations INTEGER DEFAULT 0,
                children_benefited INTEGER DEFAULT 0,
                summary_date DATE DEFAULT CURRENT_DATE,
                notes TEXT
            )
        """)
        print("✅ Medical_summary table created")
        
        # Create media table for camp photos and videos
        print("Creating media table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camp_media (
                id SERIAL PRIMARY KEY,
                camp_id INTEGER REFERENCES camps(id) ON DELETE CASCADE,
                media_type VARCHAR(10) NOT NULL, -- 'photo' or 'video'
                media_url VARCHAR(500) NOT NULL,
                caption TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Media table created")
        
        # Insert sample data
        print("Inserting sample data...")
        cursor.execute("""
            INSERT INTO volunteers (name, email, phone, role) 
            VALUES ('Test Volunteer', 'test@example.com', '1234567890', 'Doctor')
            ON CONFLICT (email) DO NOTHING
        """)
        print("✅ Sample data inserted")
        
        # Commit the transaction
        conn.commit()
        print("✅ Transaction committed")
        
        # Verify tables exist
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"✅ Tables found: {tables}")
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Database setup completed successfully!', 
            'tables_created': tables,
            'sample_data_added': True
        })
        
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return jsonify({'error': f'Database setup failed: {str(e)}'}), 500

# Simple volunteer test (no login required)
@app.route('/api/test-volunteers')
def test_volunteers():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteers ORDER BY join_date DESC")
        
        columns = [desc[0] for desc in cursor.description]
        volunteers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        return jsonify({'message': f'Found {len(volunteers)} volunteers', 'data': volunteers})
        
    except Exception as e:
        return jsonify({'error': f'Volunteer test failed: {str(e)}'}), 500

# Simple add volunteer test (no login required)
@app.route('/api/test-add-volunteer', methods=['POST'])
def test_add_volunteer():
    try:
        data = request.get_json()
        if not data:
            data = {
                'name': 'Test Volunteer',
                'email': 'test@example.com',
                'phone': '1234567890',
                'role': 'Doctor'
            }
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO volunteers (name, email, phone, role) 
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (data['name'], data['email'], data['phone'], data['role']))
        
        volunteer_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': f'Test volunteer added with ID: {volunteer_id}', 'id': volunteer_id})
        
    except Exception as e:
        return jsonify({'error': f'Add volunteer test failed: {str(e)}'}), 500

# Volunteer Management APIs
@app.route('/api/volunteers', methods=['GET'])
@login_required
def get_volunteers():
    try:
        conn = get_db_connection()
        if not conn:
            print("Database connection failed for volunteers")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteers ORDER BY join_date DESC")
        
        # Convert to dictionary format
        columns = [desc[0] for desc in cursor.description]
        volunteers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        print(f"Successfully loaded {len(volunteers)} volunteers")
        return jsonify(volunteers)
        
    except Exception as e:
        print(f"Error loading volunteers: {str(e)}")
        return jsonify({'error': f'Failed to load volunteers: {str(e)}'}), 500

@app.route('/api/volunteers', methods=['POST'])
@login_required
def add_volunteer():
    try:
        data = request.get_json()
        print(f"Received volunteer data: {data}")
        
        conn = get_db_connection()
        if not conn:
            print("Database connection failed")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO volunteers (name, email, phone, role) 
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (data['name'], data['email'], data['phone'], data['role']))
        
        volunteer_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully added volunteer with ID: {volunteer_id}")
        return jsonify({'message': 'Volunteer added successfully', 'id': volunteer_id})
        
    except Exception as e:
        print(f"Error adding volunteer: {str(e)}")
        return jsonify({'error': f'Failed to add volunteer: {str(e)}'}), 500

@app.route('/api/volunteers/<int:volunteer_id>', methods=['PUT'])
@login_required
def update_volunteer(volunteer_id):
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE volunteers 
        SET name = %s, email = %s, phone = %s, role = %s, status = %s
        WHERE id = %s
    """, (data['name'], data['email'], data['phone'], data['role'], data['status'], volunteer_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Volunteer updated successfully'})

@app.route('/api/volunteers/<int:volunteer_id>', methods=['DELETE'])
@login_required
def delete_volunteer(volunteer_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM volunteers WHERE id = %s", (volunteer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Volunteer deleted successfully'})

# Camp Management APIs
@app.route('/api/camps', methods=['GET'])
@login_required
def get_camps():
    try:
        conn = get_db_connection()
        if not conn:
            print("Database connection failed for camps")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM camps ORDER BY camp_date DESC")
        
        columns = [desc[0] for desc in cursor.description]
        camps = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        print(f"Successfully loaded {len(camps)} camps")
        return jsonify(camps)
        
    except Exception as e:
        print(f"Error loading camps: {str(e)}")
        return jsonify({'error': f'Failed to load camps: {str(e)}'}), 500

@app.route('/api/camps', methods=['POST'])
@login_required
def add_camp():
    try:
        data = request.get_json()
        print(f"Received camp data: {data}")
        
        conn = get_db_connection()
        if not conn:
            print("Database connection failed")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO camps (name, type, location, camp_date, description) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (data['name'], data['type'], data['location'], data['camp_date'], data.get('description', '')))
        
        camp_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully added camp with ID: {camp_id}")
        return jsonify({'message': 'Camp added successfully', 'id': camp_id})
        
    except Exception as e:
        print(f"Error adding camp: {str(e)}")
        return jsonify({'error': f'Failed to add camp: {str(e)}'}), 500

@app.route('/api/camps/<int:camp_id>', methods=['PUT'])
@login_required
def update_camp(camp_id):
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE camps 
        SET name = %s, type = %s, location = %s, camp_date = %s, description = %s, status = %s
        WHERE id = %s
    """, (data['name'], data['type'], data['location'], data['camp_date'], data.get('description', ''), data.get('status', 'Planned'), camp_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Camp updated successfully'})

@app.route('/api/camps/<int:camp_id>', methods=['DELETE'])
@login_required
def delete_camp(camp_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM camps WHERE id = %s", (camp_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Camp deleted successfully'})

# Donation APIs
@app.route('/api/donations', methods=['GET'])
@login_required
def get_donations():
    try:
        conn = get_db_connection()
        if not conn:
            print("Database connection failed for donations")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.*, c.name as camp_name 
            FROM donations d 
            LEFT JOIN camps c ON d.camp_id = c.id 
            ORDER BY donation_date DESC
        """)
        
        columns = [desc[0] for desc in cursor.description]
        donations = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        print(f"Successfully loaded {len(donations)} donations")
        return jsonify(donations)
        
    except Exception as e:
        print(f"Error loading donations: {str(e)}")
        return jsonify({'error': f'Failed to load donations: {str(e)}'}), 500

@app.route('/api/donations', methods=['POST'])
@login_required
def add_donation():
    try:
        data = request.get_json()
        print(f"Received donation data: {data}")
        
        conn = get_db_connection()
        if not conn:
            print("Database connection failed")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donations (camp_id, donation_type, quantity, donor_name, donation_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (data.get('camp_id'), data['donation_type'], data['quantity'], 
              data.get('donor_name', ''), data['donation_date'], data.get('notes', '')))
        
        donation_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully added donation with ID: {donation_id}")
        return jsonify({'message': 'Donation added successfully', 'id': donation_id})
        
    except Exception as e:
        print(f"Error adding donation: {str(e)}")
        return jsonify({'error': f'Failed to add donation: {str(e)}'}), 500

@app.route('/api/donations/<int:donation_id>', methods=['PUT'])
@login_required
def update_donation(donation_id):
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE donations 
        SET camp_id = %s, donation_type = %s, quantity = %s, donor_name = %s, donation_date = %s, notes = %s
        WHERE id = %s
    """, (data.get('camp_id'), data['donation_type'], data['quantity'], 
          data.get('donor_name', ''), data['donation_date'], data.get('notes', ''), donation_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Donation updated successfully'})

@app.route('/api/donations/<int:donation_id>', methods=['DELETE'])
@login_required
def delete_donation(donation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM donations WHERE id = %s", (donation_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Donation deleted successfully'})

# Analytics Dashboard APIs
@app.route('/api/analytics/dashboard')
@login_required
def get_dashboard_analytics():
    try:
        conn = get_db_connection()
        if not conn:
            print("Database connection failed for analytics")
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM volunteers")
        total_volunteers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as total FROM camps")
        total_camps = cursor.fetchone()[0]
        
        # Handle medical_summary table that might not exist
        try:
            cursor.execute("SELECT COALESCE(SUM(total_patients), 0) as total FROM medical_summary")
            total_beneficiaries = cursor.fetchone()[0]
        except:
            total_beneficiaries = 0
        
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) as total FROM donations")
        total_donations = cursor.fetchone()[0]
        
        cursor.execute("SELECT type, COUNT(*) as count FROM camps GROUP BY type")
        camp_types_data = cursor.fetchall()
        camp_types = [{'type': row[0], 'count': row[1]} for row in camp_types_data]
        
        cursor.execute("""
            SELECT TO_CHAR(camp_date, 'YYYY-MM') as month, COUNT(*) as camps
            FROM camps 
            WHERE camp_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY TO_CHAR(camp_date, 'YYYY-MM')
            ORDER BY month
        """)
        monthly_data = cursor.fetchall()
        monthly_trends = [{'month': row[0], 'camps': row[1]} for row in monthly_data]
        
        cursor.close()
        conn.close()
        
        print(f"Analytics loaded: {total_volunteers} volunteers, {total_camps} camps")
        return jsonify({
            'total_volunteers': total_volunteers,
            'total_camps': total_camps,
            'total_beneficiaries': total_beneficiaries,
            'total_donations': total_donations,
            'camp_types': camp_types,
            'monthly_trends': monthly_trends
        })
        
    except Exception as e:
        print(f"Error loading analytics: {str(e)}")
        return jsonify({'error': f'Failed to load analytics: {str(e)}'}), 500

# PDF Report Generation
@app.route('/api/reports/generate-pdf')
@login_required
def generate_pdf_report():
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
        from io import BytesIO
        import datetime
        
        # Get data from database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        
        # Get volunteers data
        cursor.execute("SELECT name, email, phone, role, join_date, status FROM volunteers ORDER BY join_date DESC")
        volunteers = cursor.fetchall()
        
        # Get camps data
        cursor.execute("SELECT name, type, location, camp_date, status FROM camps ORDER BY camp_date DESC")
        camps = cursor.fetchall()
        
        # Get donations data
        cursor.execute("SELECT donation_type, quantity, donor_name, donation_date FROM donations ORDER BY donation_date DESC")
        donations = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        story.append(Paragraph("Mathruseva Foundation - Impact Report", title_style))
        story.append(Spacer(1, 20))
        
        # Report date
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"Generated on: {current_date}", styles["Normal"]))
        story.append(Spacer(1, 30))
        
        # Volunteers Section
        story.append(Paragraph("Volunteers Summary", styles["Heading2"]))
        story.append(Spacer(1, 12))
        
        if volunteers:
            # Create volunteers table
            volunteer_data = [["Name", "Email", "Phone", "Role", "Join Date", "Status"]]
            for vol in volunteers:
                volunteer_data.append([
                    vol[0],  # name
                    vol[1],  # email
                    vol[2] if vol[2] else "N/A",  # phone
                    vol[3],  # role
                    vol[4].strftime("%Y-%m-%d") if vol[4] else "N/A",  # join_date
                    vol[5]   # status
                ])
            
            volunteer_table = Table(volunteer_data, repeatRows=1)
            volunteer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(volunteer_table)
            story.append(Paragraph(f"Total Volunteers: {len(volunteers)}", styles["Normal"]))
        else:
            story.append(Paragraph("No volunteers found.", styles["Normal"]))
        
        story.append(Spacer(1, 30))
        
        # Camps Section
        story.append(Paragraph("Medical Camps Summary", styles["Heading2"]))
        story.append(Spacer(1, 12))
        
        if camps:
            # Create camps table
            camp_data = [["Camp Name", "Type", "Location", "Date", "Status"]]
            for camp in camps:
                camp_data.append([
                    camp[0],  # name
                    camp[1],  # type
                    camp[2],  # location
                    camp[3].strftime("%Y-%m-%d") if camp[3] else "N/A",  # camp_date
                    camp[4]   # status
                ])
            
            camp_table = Table(camp_data, repeatRows=1)
            camp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(camp_table)
            story.append(Paragraph(f"Total Camps: {len(camps)}", styles["Normal"]))
        else:
            story.append(Paragraph("No camps found.", styles["Normal"]))
        
        story.append(Spacer(1, 30))
        
        # Donations Section
        story.append(Paragraph("Donations Summary", styles["Heading2"]))
        story.append(Spacer(1, 12))
        
        if donations:
            # Create donations table
            donation_data = [["Donation Type", "Quantity", "Donor Name", "Date"]]
            for donation in donations:
                donation_data.append([
                    donation[0],  # donation_type
                    str(donation[1]),  # quantity
                    donation[2] if donation[2] else "Anonymous",  # donor_name
                    donation[3].strftime("%Y-%m-%d") if donation[3] else "N/A"  # donation_date
                ])
            
            donation_table = Table(donation_data, repeatRows=1)
            donation_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(donation_table)
            story.append(Paragraph(f"Total Donations Recorded: {len(donations)}", styles["Normal"]))
        else:
            story.append(Paragraph("No donations found.", styles["Normal"]))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Thank you for supporting Mathruseva Foundation!", styles["Normal"]))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        from flask import send_file
        return send_file(
            BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=False,
            download_name=f'mathruseva_report_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500

# Media Management APIs
@app.route('/api/media/upload', methods=['POST'])
@login_required
def upload_media():
    try:
        # Handle file upload
        if 'mediaFile' in request.files:
            file = request.files['mediaFile']
            if file.filename != '':
                # Save file to uploads directory
                import os
                import uuid
                from werkzeug.utils import secure_filename
                
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(upload_dir, unique_filename)
                
                # Save file
                file.save(file_path)
                
                # Generate URL for the file
                media_url = f"/static/uploads/{unique_filename}"
                
                # Get other form data
                camp_id = request.form.get('camp_id')
                media_type = request.form.get('media_type')
                caption = request.form.get('caption', '')
                
                # Auto-detect media type if not specified
                if not media_type:
                    media_type = 'photo' if file.content_type.startswith('image/') else 'video'
                
        else:
            # Fallback to URL-based upload (for backward compatibility)
            data = request.get_json()
            camp_id = data.get('camp_id')
            media_type = data.get('media_type')
            media_url = data.get('media_url')
            caption = data.get('caption', '')
        
        if not camp_id or not media_type or not media_url:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if media_type not in ['photo', 'video']:
            return jsonify({'error': 'Invalid media type'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO camp_media (camp_id, media_type, media_url, caption)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (camp_id, media_type, media_url, caption))
        
        media_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Media uploaded successfully', 'id': media_id})
        
    except Exception as e:
        print(f"Error uploading media: {str(e)}")
        return jsonify({'error': f'Failed to upload media: {str(e)}'}), 500

@app.route('/api/media/camp/<int:camp_id>', methods=['GET'])
@login_required
def get_camp_media(camp_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, media_type, media_url, caption, upload_date
            FROM camp_media 
            WHERE camp_id = %s 
            ORDER BY upload_date DESC
        """, (camp_id,))
        
        media_items = []
        for row in cursor.fetchall():
            media_items.append({
                'id': row[0],
                'media_type': row[1],
                'media_url': row[2],
                'caption': row[3],
                'upload_date': row[4].isoformat() if row[4] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({'media': media_items})
        
    except Exception as e:
        print(f"Error fetching camp media: {str(e)}")
        return jsonify({'error': f'Failed to fetch media: {str(e)}'}), 500

@app.route('/api/media/all', methods=['GET'])
@login_required
def get_all_media():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cm.id, cm.camp_id, cm.media_type, cm.media_url, cm.caption, 
                   cm.upload_date, c.name as camp_name, c.location as camp_location
            FROM camp_media cm
            JOIN camps c ON cm.camp_id = c.id
            ORDER BY cm.upload_date DESC
        """)
        
        media_items = []
        for row in cursor.fetchall():
            media_items.append({
                'id': row[0],
                'camp_id': row[1],
                'media_type': row[2],
                'media_url': row[3],
                'caption': row[4],
                'upload_date': row[5].isoformat() if row[5] else None,
                'camp_name': row[6],
                'camp_location': row[7]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({'media': media_items})
        
    except Exception as e:
        print(f"Error fetching all media: {str(e)}")
        return jsonify({'error': f'Failed to fetch media: {str(e)}'}), 500

@app.route('/api/media/<int:media_id>', methods=['DELETE'])
@login_required
def delete_media(media_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute("DELETE FROM camp_media WHERE id = %s", (media_id,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Media not found'}), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Media deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting media: {str(e)}")
        return jsonify({'error': f'Failed to delete media: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
