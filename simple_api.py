from flask import Flask, request, jsonify
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)

# Simple database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'NehaJ@447747',
    'database': 'mathruseva_foundation',
    'port': 3306
}

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return None

@app.route('/api/volunteers', methods=['GET', 'POST'])
def volunteers_api():
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
            # Log request details
            print(f"📥 Request headers: {dict(request.headers)}")
            print(f"📥 Request data: {request.data}")
            print(f"📥 Request form: {request.form}")
            
            data = request.get_json()
            print(f"📤 Parsed JSON data: {data}")
            
            # Validate required fields
            if not data:
                print("❌ No data received")
                return jsonify({'error': 'No data received'}), 400
                
            required_fields = ['name', 'email', 'role']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
                return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
            
            print(f"📤 Adding volunteer: {data}")
            
            conn = get_db()
            if not conn:
                print("❌ Database connection failed")
                return jsonify({'error': 'Database connection failed'}), 500
                
            cursor = conn.cursor()
            
            # Check for duplicate email
            cursor.execute("SELECT id FROM volunteers WHERE email = %s", (data['email'],))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                print(f"❌ Email already exists: {data['email']}")
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
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mathruseva Foundation - Simple API Test</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <div class="container mt-4">
        <h1>Mathruseva Foundation - Volunteer Management</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Add Volunteer</h5>
                    </div>
                    <div class="card-body">
                        <form id="volunteerForm">
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" id="volunteerName" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" id="volunteerEmail" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Phone</label>
                                <input type="tel" class="form-control" id="volunteerPhone">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Role</label>
                                <select class="form-select" id="volunteerRole" required>
                                    <option value="">Select Role</option>
                                    <option value="Helper">Helper</option>
                                    <option value="Organizer">Organizer</option>
                                    <option value="Coordinator">Coordinator</option>
                                </select>
                            </div>
                            <button type="button" class="btn btn-primary" onclick="addVolunteer()">Add Volunteer</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Current Volunteers</h5>
                    </div>
                    <div class="card-body">
                        <div id="volunteersList"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function addVolunteer() {
            const name = document.getElementById('volunteerName').value;
            const email = document.getElementById('volunteerEmail').value;
            const phone = document.getElementById('volunteerPhone').value;
            const role = document.getElementById('volunteerRole').value;
            
            if (!name || !email || !role) {
                alert('Please fill in all required fields');
                return;
            }
            
            fetch('/api/volunteers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    phone: phone,
                    role: role,
                    status: 'Active',
                    join_date: new Date().toISOString().split('T')[0]
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Volunteer added successfully!');
                    document.getElementById('volunteerForm').reset();
                    loadVolunteers();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
        }
        
        function loadVolunteers() {
            fetch('/api/volunteers')
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById('volunteersList');
                if (data.volunteers && data.volunteers.length > 0) {
                    list.innerHTML = data.volunteers.map(v => 
                        `<div class="alert alert-info">
                            <strong>${v.name}</strong> - ${v.email} - ${v.role}
                        </div>`
                    ).join('');
                } else {
                    list.innerHTML = '<p>No volunteers found</p>';
                }
            });
        }
        
        // Load volunteers on page load
        loadVolunteers();
    </script>
</body>
</html>'''

@app.route('/test-db')
def test_db():
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM volunteers")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'connected',
                'volunteer_count': count,
                'message': 'Database connection working'
            })
        else:
            return jsonify({'status': 'failed', 'message': 'Cannot connect to database'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    print("🚀 Starting simple API server...")
    print("📍 Test database at: http://127.0.0.1:5000/test-db")
    print("📍 API at: http://127.0.0.1:5000/api/volunteers")
    app.run(host='127.0.0.1', port=5000, debug=True)
