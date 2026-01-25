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
POSTGRES_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'mathruseva_user'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'mathruseva_foundation'),
    'port': 5432
}

def get_db_connection():
    try:
        return psycopg2.connect(**POSTGRES_CONFIG)
    except Exception as e:
        print(f"Database connection error: {e}")
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

# Test database connection
@app.route('/api/test-db')
def test_database():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Database connection working!', 'result': result[0]})
    except Exception as e:
        return jsonify({'error': f'Database test failed: {str(e)}'}), 500

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
