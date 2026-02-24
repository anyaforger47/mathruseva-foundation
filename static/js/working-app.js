console.log('✅ Mathruseva Foundation App Loaded Successfully!');

let currentSection = 'dashboard';

function showSection(sectionId) {
    console.log('🔄 Switching to section:', sectionId);
    
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
        console.log('✅ Section displayed:', sectionId);
    } else {
        console.error('❌ Section not found:', sectionId);
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
    fetch('/api/volunteers')
    .then(response => response.json())
    .then(data => {
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
            date: date,
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
    const amount = document.getElementById('donationAmount').value;
    const donor = document.getElementById('donationDonor').value;
    
    if (!type || !quantity) {
        alert('⚠️ Please fill in all required fields');
        return;
    }
    
    fetch('/api/donations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            camp_id: camp || null,
            type: type,
            quantity: quantity,
            amount: amount || 0,
            donor: donor || 'Anonymous',
            donation_date: new Date().toISOString().split('T')[0]
        })
    })
    .then(response => response.json())
    .then(data => {
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
        console.error('Error:', error);
        alert('❌ Failed to add donation');
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
                    <td>${donation.donor}</td>
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

function markAttendance() {
    console.log('✅ Marking attendance...');
    
    // Get form values
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

function updateAttendanceStats() {
    const present = parseInt(document.getElementById('totalPresent').textContent);
    document.getElementById('totalPresent').textContent = present + 1;
    
    const total = present + 1 + parseInt(document.getElementById('totalAbsent').textContent) + parseInt(document.getElementById('totalLate').textContent);
    const rate = Math.round(((present + 1) / total) * 100);
    document.getElementById('attendanceRate').textContent = rate + '%';
}

function loadAttendance() {
    console.log('📊 Loading attendance data...');
    fetch('/api/attendance')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        if (data.attendance && data.attendance.length > 0) {
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
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No attendance records found. Mark your first attendance!</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading attendance:', error);
    });
}

function initializeCharts() {
    console.log('📊 Creating charts...');
    
    // Volunteer Performance Chart
    const volunteerCtx = document.getElementById('volunteerPerformanceChart');
    if (volunteerCtx) {
        console.log('✅ Creating volunteer chart...');
        new Chart(volunteerCtx, {
            type: 'doughnut',
            data: {
                labels: ['Active', 'Inactive', 'On Leave', 'New Volunteers'],
                datasets: [{
                    data: [15, 3, 2, 5],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107', '#17a2b8'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: { padding: 20 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + ' volunteers';
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
        console.log('✅ Volunteer chart created');
    }
    
    // Donation Impact Chart
    const donationCtx = document.getElementById('donationImpactChart');
    if (donationCtx) {
        console.log('✅ Creating donation chart...');
        new Chart(donationCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Donations ($)',
                    data: [12000, 19000, 15000, 22000, 18000, 25000],
                    backgroundColor: '#007bff',
                    borderColor: '#0056b3',
                    borderWidth: 2,
                    borderRadius: 8,
                    hoverBackgroundColor: '#0056b3'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Donations: $' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
        console.log('✅ Donation chart created');
    }
    
    // Attendance Trend Chart
    const attendanceCtx = document.getElementById('attendanceTrendChart');
    if (attendanceCtx) {
        console.log('✅ Creating attendance trend chart...');
        new Chart(attendanceCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Attendance Rate (%)',
                    data: [85, 88, 92, 87, 90, 75, 70],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#28a745',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Attendance: ' + context.parsed.y + '%';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
        console.log('✅ Attendance trend chart created');
    }
    
    // Camp Distribution Chart
    const campCtx = document.getElementById('campDistributionChart');
    if (campCtx) {
        console.log('✅ Creating camp distribution chart...');
        new Chart(campCtx, {
            type: 'polarArea',
            data: {
                labels: ['Eye Camps', 'Blood Donation', 'General Health', 'Donation Drives'],
                datasets: [{
                    data: [12, 8, 15, 6],
                    backgroundColor: ['#007bff', '#dc3545', '#28a745', '#ffc107'],
                    borderColor: ['#0056b3', '#c82333', '#1e7e34', '#d39e00'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: { padding: 15 }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
        console.log('✅ Camp distribution chart created');
    }
    
    console.log('🎉 All charts initialized successfully!');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing dashboard...');
    console.log('✅ Dashboard ready!');
});
