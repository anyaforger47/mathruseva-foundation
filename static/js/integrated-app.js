console.log('✅ Mathruseva Foundation App Loaded Successfully!');
console.log('🧪 Testing if JavaScript is working...');

// Test function
window.testJS = function() {
    console.log('🧪 JavaScript is working!');
    alert('✅ JavaScript is loaded and working!');
};

let currentSection = 'dashboard';

function showSection(sectionId) {
    console.log('🔄 Switching to section:', sectionId);
    alert(`🔄 Switching to section: ${sectionId}`);
    
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
        console.log('✅ Section displayed:', sectionId);
        alert(`✅ Section ${sectionId} displayed successfully!`);
    } else {
        console.error('❌ Section not found:', sectionId);
        alert(`❌ Section not found: ${sectionId}`);
    }
    
    currentSection = sectionId;
    
    // Load section-specific content
    if (sectionId === 'analytics') {
        console.log('📊 Initializing analytics charts...');
        setTimeout(initializeCharts, 100);
    } else if (sectionId === 'attendance') {
        console.log('📝 Loading attendance data...');
        loadAttendance();
        loadVolunteerOptions();
        loadCampOptions();
    } else if (sectionId === 'volunteers') {
        loadVolunteers();
    } else if (sectionId === 'camps') {
        loadCamps();
    } else if (sectionId === 'donations') {
        loadDonations();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing dashboard...');
    console.log('🧪 Test JavaScript function available:', typeof window.testJS);
    
    // Test the function
    if (typeof window.testJS === 'function') {
        console.log('✅ Test function found, calling it...');
        window.testJS();
    } else {
        console.error('❌ Test function not found!');
        alert('❌ JavaScript is not loading properly. Please refresh the page.');
    }
    
    loadVolunteers();
    loadCamps();
    loadDonations();
    loadAttendance();
    console.log('✅ Dashboard ready!');
});

// Volunteer Management
function addVolunteer() {
    console.log('👤 Adding volunteer...');
    
    const name = document.getElementById('volunteerName').value;
    const email = document.getElementById('volunteerEmail').value;
    const phone = document.getElementById('volunteerPhone').value;
    const role = document.getElementById('volunteerRole').value;
    
    if (!name || !email || !role) {
        alert('⚠️ Please fill in all required fields');
        return;
    }
    
    console.log('📤 Sending data:', { name, email, phone, role });
    
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
    .then(response => {
        console.log('📥 Response status:', response.status);
        
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || `HTTP ${response.status}`);
            });
        }
        
        return response.json();
    })
    .then(data => {
        console.log('✅ Response data:', data);
        
        if (data.success) {
            alert('✅ Volunteer added successfully!');
            document.getElementById('volunteerForm').reset();
            
            // Close modal
            const modalElement = document.getElementById('volunteerModal');
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) {
                modal.hide();
            } else {
                modalElement.classList.remove('show');
                modalElement.style.display = 'none';
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
            }
            
            // Reload data
            loadVolunteers();
            loadVolunteerOptions();
        } else {
            alert('❌ Error: ' + (data.error || 'Failed to add volunteer'));
        }
    })
    .catch(error => {
        console.error('❌ Error details:', error);
        alert('❌ Error: ' + error.message);
    });
}

function loadVolunteers() {
    console.log('📥 Loading volunteers...');
    fetch('/api/volunteers')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Volunteers loaded:', data);
        const tbody = document.getElementById('volunteersTableBody');
        tbody.innerHTML = '';
        
        if (data.volunteers && data.volunteers.length > 0) {
            data.volunteers.forEach(volunteer => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${volunteer.name}</td>
                    <td>${volunteer.email}</td>
                    <td>${volunteer.phone || 'N/A'}</td>
                    <td><span class="badge bg-success">${volunteer.status}</span></td>
                    <td>${volunteer.join_date}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editVolunteer(${volunteer.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteVolunteer(${volunteer.id})">Delete</button>
                    </td>
                `;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No volunteers found. Add your first volunteer!</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading volunteers:', error);
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

// Camp Management
function addCamp() {
    console.log('🏕️ Adding camp...');
    
    const name = document.getElementById('campName').value;
    const type = document.getElementById('campType').value;
    const location = document.getElementById('campLocation').value;
    const date = document.getElementById('campDate').value;
    const description = document.getElementById('campDescription').value;
    
    if (!name || !type || !location || !date) {
        alert('⚠️ Please fill in all required fields');
        return;
    }
    
    fetch('/api/camps', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            type: type,
            location: location,
            camp_date: date,
            description: description,
            status: 'Upcoming'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Camp added successfully!');
            document.getElementById('campForm').reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('campModal'));
            modal.hide();
            loadCamps();
            loadCampOptions();
        } else {
            alert('❌ Error: ' + (data.error || 'Failed to add camp'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Failed to add camp');
    });
}

function loadCamps() {
    fetch('/api/camps')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('campsTableBody');
        tbody.innerHTML = '';
        
        if (data.camps && data.camps.length > 0) {
            data.camps.forEach(camp => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${camp.name}</td>
                    <td><span class="badge bg-info">${camp.type}</span></td>
                    <td>${camp.location}</td>
                    <td>${camp.date}</td>
                    <td><span class="badge bg-${camp.status === 'Completed' ? 'success' : 'warning'}">${camp.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editCamp(${camp.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteCamp(${camp.id})">Delete</button>
                    </td>
                `;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No camps found. Create your first camp!</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading camps:', error);
    });
}

function loadCampOptions() {
    fetch('/api/camps')
    .then(response => response.json())
    .then(data => {
        const attendanceSelect = document.getElementById('attendanceCamp');
        const donationSelect = document.getElementById('donationCamp');
        
        attendanceSelect.innerHTML = '<option value="">Select Camp</option>';
        donationSelect.innerHTML = '<option value="">Select Camp</option>';
        
        if (data.camps) {
            data.camps.forEach(camp => {
                const option1 = document.createElement('option');
                option1.value = camp.id;
                option1.textContent = camp.name;
                attendanceSelect.appendChild(option1);
                
                const option2 = document.createElement('option');
                option2.value = camp.id;
                option2.textContent = camp.name;
                donationSelect.appendChild(option2);
            });
        }
    })
    .catch(error => {
        console.error('Error loading camp options:', error);
    });
}

// Donation Management
function addDonation() {
    console.log('🎁 Adding donation...');
    
    const camp = document.getElementById('donationCamp').value;
    const type = document.getElementById('donationType').value;
    const quantity = document.getElementById('donationQuantity').value;
    const donor = document.getElementById('donationDonor').value;
    
    console.log('📥 Form values:', { camp, type, quantity, donor });
    
    if (!type || !quantity) {
        alert('⚠️ Please fill in all required fields');
        return;
    }
    
    console.log('📤 Sending request to /api/donations');
    
    fetch('/api/donations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            camp_id: camp || null,
            donation_type: type,
            quantity: quantity,
            donor: donor || 'Anonymous',
            donation_date: new Date().toISOString().split('T')[0]
        })
    })
    .then(response => {
        console.log('📥 Response status:', response.status);
        console.log('📥 Response headers:', response.headers);
        
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || `HTTP ${response.status}`);
            });
        }
        
        return response.json();
    })
    .then(data => {
        console.log('✅ Response data:', data);
        
        if (data.success) {
            alert('✅ Donation added successfully!');
            document.getElementById('donationForm').reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('donationModal'));
            modal.hide();
            loadDonations();
        } else {
            alert('❌ Error: ' + (data.error || 'Failed to add donation'));
        }
    })
    .catch(error => {
        console.error('❌ Full error details:', error);
        console.error('❌ Error stack:', error.stack);
        
        if (error.message.includes('Failed to fetch')) {
            alert('❌ Network error: Cannot connect to server. Please check if server is running.');
        } else if (error.message.includes('HTTP 404')) {
            alert('❌ API endpoint not found. Server may need restart.');
        } else if (error.message.includes('HTTP 500')) {
            alert('❌ Server error: Database connection issue.');
        } else if (error.message.includes('HTTP 401')) {
            alert('❌ Authentication error. Please login again.');
        } else {
            alert('❌ Error: ' + error.message);
        }
    });
}

function loadDonations() {
    fetch('/api/donations')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('donationsTableBody');
        tbody.innerHTML = '';
        
        if (data.donations && data.donations.length > 0) {
            data.donations.forEach(donation => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${donation.type}</td>
                    <td>${donation.quantity}</td>
                    <td>$${donation.amount || 0}</td>
                    <td>${donation.donor_name || 'Anonymous'}</td>
                    <td>${donation.donation_date}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editDonation(${donation.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteDonation(${donation.id})">Delete</button>
                    </td>
                `;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No donations found. Add your first donation!</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading donations:', error);
    });
}

// Attendance Management
function markAttendance() {
    console.log('✅ Marking attendance...');
    
    const volunteerId = document.getElementById('attendanceVolunteer').value;
    const campId = document.getElementById('attendanceCamp').value;
    const date = document.getElementById('attendanceDateModal').value;
    const checkIn = document.getElementById('checkInTime').value;
    const checkOut = document.getElementById('checkOutTime').value;
    const status = document.getElementById('attendanceStatus').value;
    
    if (!volunteerId || !campId || !date || !status || !checkIn) {
        alert('⚠️ Please fill in all required fields');
        return;
    }
    
    fetch('/api/attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            volunteer_id: volunteerId,
            camp_id: campId,
            date: date,
            check_in_time: checkIn,
            check_out_time: checkOut,
            status: status,
            notes: ''
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Attendance marked successfully!');
            document.getElementById('attendanceForm').reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('attendanceModal'));
            modal.hide();
            loadAttendance();
            updateAttendanceStats();
        } else {
            alert('❌ Error: ' + (data.error || 'Failed to mark attendance'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Failed to mark attendance');
    });
}

function loadAttendance() {
    console.log('📊 Loading attendance data...');
    fetch('/api/attendance')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Attendance data loaded:', data);
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        if (data.attendance && data.attendance.length > 0) {
            console.log(`📋 Found ${data.attendance.length} attendance records`);
            data.attendance.forEach(record => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td><i class="fas fa-user me-2"></i>${record.volunteer_name || 'Unknown'}</td>
                    <td><i class="fas fa-campground me-2"></i>${record.camp_name || 'N/A'}</td>
                    <td>${record.attendance_date}</td>
                    <td>${record.check_in_time}</td>
                    <td>${record.check_out_time || 'N/A'}</td>
                    <td><span class="badge bg-${record.status === 'present' ? 'success' : record.status === 'absent' ? 'danger' : record.status === 'late' ? 'warning' : 'info'}">${record.status.charAt(0).toUpperCase() + record.status.slice(1)}</span></td>
                `;
            });
        } else {
            console.log('⚠️ No attendance records found');
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No attendance records found. Mark your first Attendance!</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading attendance:', error);
    });
}

function updateAttendanceStats() {
    // This would be updated based on real data from the server
    console.log('📊 Updating attendance stats...');
}

function showAttendanceModal() {
    console.log('🔧 Opening attendance modal...');
    const modal = new bootstrap.Modal(document.getElementById('attendanceModal'));
    modal.show();
    loadAttendanceOptions();
}

function loadAttendanceOptions() {
    // Set today's date
    document.getElementById('attendanceDateModal').value = new Date().toISOString().split('T')[0];
    console.log('📅 Set today\'s date');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing dashboard...');
    loadVolunteers();
    loadCamps();
    loadDonations();
    loadAttendance();
    console.log('✅ Dashboard ready!');
});

function deleteVolunteer(id) {
    if (confirm('Are you sure you want to delete this volunteer?')) {
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
                alert('Volunteer deleted successfully!');
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
    if (confirm('Are you sure you want to delete this donation?')) {
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
                alert('Donation deleted successfully!');
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

function editVolunteer(id) {
    alert('Edit functionality coming soon!');
}

function editCamp(id) {
    alert('Edit functionality coming soon!');
}

function editDonation(id) {
    alert('Edit functionality coming soon!');
}

function deleteCamp(id) {
    alert('Delete functionality coming soon!');
}
