from flask import Flask, request, jsonify, render_template
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

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return None

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mathruseva Foundation - Fresh Start</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <div class="container mt-4">
        <h1>Mathruseva Foundation - Fresh Working System</h1>
        
        <!-- Navigation -->
        <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
                <a class="nav-link active" href="#" onclick="showSection('volunteers')">Volunteers</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" onclick="showSection('donations')">Donations</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" onclick="showSection('attendance')">Attendance</a>
            </li>
        </ul>
        
        <!-- Volunteers Section -->
        <div id="volunteers" class="section">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Add Volunteer</h5>
                </div>
                <div class="card-body">
                    <form id="volunteerForm">
                        <div class="row">
                            <div class="col-md-3">
                                <input type="text" class="form-control" id="volunteerName" placeholder="Name" required>
                            </div>
                            <div class="col-md-3">
                                <input type="email" class="form-control" id="volunteerEmail" placeholder="Email" required>
                            </div>
                            <div class="col-md-3">
                                <input type="tel" class="form-control" id="volunteerPhone" placeholder="Phone">
                            </div>
                            <div class="col-md-2">
                                <select class="form-select" id="volunteerRole" required>
                                    <option value="">Role</option>
                                    <option value="Helper">Helper</option>
                                    <option value="Organizer">Organizer</option>
                                    <option value="Coordinator">Coordinator</option>
                                </select>
                            </div>
                            <div class="col-md-1">
                                <button type="button" class="btn btn-primary" onclick="addVolunteer()">Add</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h5>Volunteers List</h5>
                </div>
                <div class="card-body">
                    <div id="volunteersList"></div>
                </div>
            </div>
        </div>
        
        <!-- Donations Section -->
        <div id="donations" class="section" style="display: none;">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Add Donation</h5>
                </div>
                <div class="card-body">
                    <form id="donationForm">
                        <div class="row">
                            <div class="col-md-3">
                                <select class="form-select" id="donationType" required>
                                    <option value="">Type</option>
                                    <option value="Books">Books</option>
                                    <option value="Notebooks">Notebooks</option>
                                    <option value="Pencils">Pencils</option>
                                    <option value="Food Packets">Food Packets</option>
                                </select>
                            </div>
                            <div class="col-md-2">
                                <input type="number" class="form-control" id="donationQuantity" placeholder="Quantity" required>
                            </div>
                            <div class="col-md-3">
                                <input type="text" class="form-control" id="donationDonor" placeholder="Donor Name">
                            </div>
                            <div class="col-md-2">
                                <input type="date" class="form-control" id="donationDate">
                            </div>
                            <div class="col-md-2">
                                <button type="button" class="btn btn-primary" onclick="addDonation()">Add</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h5>Donations List</h5>
                </div>
                <div class="card-body">
                    <div id="donationsList"></div>
                </div>
            </div>
        </div>
        
        <!-- Attendance Section -->
        <div id="attendance" class="section" style="display: none;">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Mark Attendance</h5>
                </div>
                <div class="card-body">
                    <form id="attendanceForm">
                        <div class="row">
                            <div class="col-md-3">
                                <select class="form-select" id="attendanceVolunteer" required>
                                    <option value="">Select Volunteer</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <select class="form-select" id="attendanceStatus" required>
                                    <option value="">Status</option>
                                    <option value="present">Present</option>
                                    <option value="absent">Absent</option>
                                    <option value="late">Late</option>
                                </select>
                            </div>
                            <div class="col-md-2">
                                <input type="date" class="form-control" id="attendanceDate">
                            </div>
                            <div class="col-md-2">
                                <input type="time" class="form-control" id="checkInTime">
                            </div>
                            <div class="col-md-2">
                                <button type="button" class="btn btn-primary" onclick="markAttendance()">Mark</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h5>Attendance Records</h5>
                </div>
                <div class="card-body">
                    <div id="attendanceList"></div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        console.log('🚀 Fresh system loaded!');
        
        function showSection(sectionId) {
            console.log('🔄 Showing section:', sectionId);
            
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Show selected section
            document.getElementById(sectionId).style.display = 'block';
            
            // Update nav tabs
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Load data for section
            if (sectionId === 'volunteers') {
                loadVolunteers();
            } else if (sectionId === 'donations') {
                loadDonations();
            } else if (sectionId === 'attendance') {
                loadAttendance();
                loadVolunteerOptions();
            }
        }
        
        function addVolunteer() {
            console.log('👤 Adding volunteer...');
            
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
                    role: role
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('✅ Volunteer response:', data);
                if (data.success) {
                    alert('Volunteer added successfully!');
                    document.getElementById('volunteerForm').reset();
                    loadVolunteers();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('❌ Error:', error);
                alert('Error: ' + error.message);
            });
        }
        
        function addDonation() {
            console.log('🎁 Adding donation...');
            
            const type = document.getElementById('donationType').value;
            const quantity = document.getElementById('donationQuantity').value;
            const donor = document.getElementById('donationDonor').value;
            const date = document.getElementById('donationDate').value;
            
            if (!type || !quantity) {
                alert('Please fill in all required fields');
                return;
            }
            
            fetch('/api/donations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    donation_type: type,
                    quantity: quantity,
                    donor: donor || 'Anonymous',
                    donation_date: date || new Date().toISOString().split('T')[0]
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('✅ Donation response:', data);
                if (data.success) {
                    alert('Donation added successfully!');
                    document.getElementById('donationForm').reset();
                    loadDonations();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('❌ Error:', error);
                alert('Error: ' + error.message);
            });
        }
        
        function markAttendance() {
            console.log('✅ Marking attendance...');
            
            const volunteerId = document.getElementById('attendanceVolunteer').value;
            const status = document.getElementById('attendanceStatus').value;
            const date = document.getElementById('attendanceDate').value;
            const checkInTime = document.getElementById('checkInTime').value;
            
            if (!volunteerId || !status || !date) {
                alert('Please fill in all required fields');
                return;
            }
            
            fetch('/api/attendance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    volunteer_id: volunteerId,
                    status: status,
                    date: date,
                    check_in_time: checkInTime
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('✅ Attendance response:', data);
                if (data.success) {
                    alert('Attendance marked successfully!');
                    document.getElementById('attendanceForm').reset();
                    loadAttendance();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('❌ Error:', error);
                alert('Error: ' + error.message);
            });
        }
        
        function loadVolunteers() {
            console.log('📥 Loading volunteers...');
            fetch('/api/volunteers')
            .then(response => response.json())
            .then(data => {
                console.log('✅ Volunteers loaded:', data);
                const list = document.getElementById('volunteersList');
                if (data.volunteers && data.volunteers.length > 0) {
                    list.innerHTML = data.volunteers.map(v => 
                        `<div class="alert alert-info d-flex justify-content-between">
                            <span><strong>${v.name}</strong> - ${v.email} - ${v.role}</span>
                            <button class="btn btn-sm btn-danger" onclick="deleteVolunteer(${v.id})">Delete</button>
                        </div>`
                    ).join('');
                } else {
                    list.innerHTML = '<p>No volunteers found</p>';
                }
            })
            .catch(error => {
                console.error('Error loading volunteers:', error);
            });
        }
        
        function loadDonations() {
            console.log('📥 Loading donations...');
            fetch('/api/donations')
            .then(response => response.json())
            .then(data => {
                console.log('✅ Donations loaded:', data);
                const list = document.getElementById('donationsList');
                if (data.donations && data.donations.length > 0) {
                    list.innerHTML = data.donations.map(d => 
                        `<div class="alert alert-success d-flex justify-content-between">
                            <span><strong>${d.donation_type}</strong> - ${d.quantity} - ${d.donor_name}</span>
                            <button class="btn btn-sm btn-danger" onclick="deleteDonation(${d.id})">Delete</button>
                        </div>`
                    ).join('');
                } else {
                    list.innerHTML = '<p>No donations found</p>';
                }
            })
            .catch(error => {
                console.error('Error loading donations:', error);
            });
        }
        
        function loadAttendance() {
            console.log('📥 Loading attendance...');
            fetch('/api/attendance')
            .then(response => response.json())
            .then(data => {
                console.log('✅ Attendance loaded:', data);
                const list = document.getElementById('attendanceList');
                if (data.attendance && data.attendance.length > 0) {
                    list.innerHTML = data.attendance.map(a => 
                        `<div class="alert alert-warning">
                            <strong>${a.volunteer_name}</strong> - ${a.status} - ${a.attendance_date}
                        </div>`
                    ).join('');
                } else {
                    list.innerHTML = '<p>No attendance records found</p>';
                }
            })
            .catch(error => {
                console.error('Error loading attendance:', error);
            });
        }
        
        function loadVolunteerOptions() {
            console.log('📥 Loading volunteer options...');
            fetch('/api/volunteers')
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('attendanceVolunteer');
                select.innerHTML = '<option value="">Select Volunteer</option>';
                
                if (data.volunteers) {
                    data.volunteers.forEach(volunteer => {
                        const option = document.createElement('option');
                        option.value = volunteer.id;
                        option.textContent = volunteer.name;
                        select.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error loading volunteer options:', error);
            });
        }
        
        function deleteVolunteer(id) {
            if (confirm('Delete this volunteer?')) {
                fetch('/api/volunteers', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: id })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Volunteer deleted!');
                        loadVolunteers();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error: ' + error.message);
                });
            }
        }
        
        function deleteDonation(id) {
            if (confirm('Delete this donation?')) {
                fetch('/api/donations', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: id })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Donation deleted!');
                        loadDonations();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error: ' + error.message);
                });
            }
        }
        
        // Set today's date
        document.getElementById('donationDate').value = new Date().toISOString().split('T')[0];
        document.getElementById('attendanceDate').value = new Date().toISOString().split('T')[0];
        
        // Load initial data
        loadVolunteers();
    </script>
</body>
</html>'''

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
                datetime.now().strftime('%Y-%m-%d')
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
                None,  # camp_id
                data['donation_type'], 
                data['quantity'], 
                data['donor'], 
                data['donation_date']
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
            print(f"❌ Error: {e}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
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
            
            print(f"✅ Deleted donation ID: {donation_id}")
            return jsonify({
                'success': True, 
                'message': 'Donation deleted successfully'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['GET', 'POST'])
def api_attendance():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT va.*, v.name as volunteer_name 
                    FROM volunteer_attendance va
                    LEFT JOIN volunteers v ON va.volunteer_id = v.id
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
            print(f"❌ Error: {e}")
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
                INSERT INTO volunteer_attendance (volunteer_id, attendance_date, check_in_time, status)
                VALUES (%s, %s, %s, %s)
            """, (
                data['volunteer_id'], 
                data['date'], 
                data.get('check_in_time', '09:00:00'),
                data['status']
            ))
            
            attendance_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Marked attendance ID: {attendance_id}")
            return jsonify({
                'success': True, 
                'message': 'Attendance marked successfully',
                'attendance_id': attendance_id
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting FRESH Mathruseva Foundation system...")
    print("📍 Running at: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
