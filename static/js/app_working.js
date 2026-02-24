console.log('🚀 Mathruseva Foundation Admin Dashboard Loading...');

let currentSection = 'dashboard';
let charts = {};

// Global navigation function
function showSection(sectionId) {
    console.log('🔄 Switching to section:', sectionId);
    
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('onclick') === `showSection('${sectionId}')`) {
            link.classList.add('active');
        }
    });
    
    // Load section-specific content
    if (sectionId === 'volunteers') {
        loadVolunteers();
    } else if (sectionId === 'camps') {
        loadCamps();
    } else if (sectionId === 'donations') {
        loadDonations();
    } else if (sectionId === 'gallery') {
        loadGallery();
    } else if (sectionId === 'attendance') {
        loadAttendance();
    } else if (sectionId === 'analytics') {
        loadAnalytics();
    }
    
    currentSection = sectionId;
    console.log('📍 Current section is now:', sectionId);
}

// Modal functions - SIMPLE AND WORKING
function openVolunteerModal() {
    console.log('Opening volunteer modal...');
    try {
        const modalElement = document.getElementById('addVolunteerModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            console.error('Volunteer modal not found');
        }
    } catch (error) {
        console.error('Error opening volunteer modal:', error);
        alert('Error opening volunteer modal');
    }
}

function openCampModal() {
    console.log('Opening camp modal...');
    try {
        const modalElement = document.getElementById('addCampModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            console.error('Camp modal not found');
        }
    } catch (error) {
        console.error('Error opening camp modal:', error);
        alert('Error opening camp modal');
    }
}

function openDonationModal() {
    console.log('Opening donation modal...');
    try {
        const modalElement = document.getElementById('addDonationModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            console.error('Donation modal not found');
        }
    } catch (error) {
        console.error('Error opening donation modal:', error);
        alert('Error opening donation modal');
    }
}

function openMediaModal() {
    console.log('Opening media modal...');
    try {
        const modalElement = document.getElementById('addMediaModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            console.error('Media modal not found');
        }
    } catch (error) {
        console.error('Error opening media modal:', error);
        alert('Error opening media modal');
    }
}

function openAttendanceModal() {
    console.log('Opening attendance modal...');
    try {
        const modalElement = document.getElementById('addAttendanceModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            console.error('Attendance modal not found');
        }
    } catch (error) {
        console.error('Error opening attendance modal:', error);
        alert('Error opening attendance modal');
    }
}

// Save functions
function saveVolunteer() {
    const name = document.getElementById('volunteerName').value;
    const email = document.getElementById('volunteerEmail').value;
    const phone = document.getElementById('volunteerPhone').value;
    
    fetch('/api/volunteers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            phone: phone
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Volunteer added successfully!');
            bootstrap.Modal.getInstance(document.getElementById('addVolunteerModal')).hide();
            loadVolunteers();
        } else {
            alert('❌ Error: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error adding volunteer');
    });
}

function saveCamp() {
    const name = document.getElementById('campName').value;
    const location = document.getElementById('campLocation').value;
    const date = document.getElementById('campDate').value;
    const type = document.getElementById('campType').value;
    
    fetch('/api/camps', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            location: location,
            camp_date: date,
            type: type
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Camp added successfully!');
            bootstrap.Modal.getInstance(document.getElementById('addCampModal')).hide();
            loadCamps();
        } else {
            alert('❌ Error: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error adding camp');
    });
}

function saveDonation() {
    const donorName = document.getElementById('donorName').value;
    const amount = document.getElementById('donationAmount').value;
    const type = document.getElementById('donationType').value;
    
    fetch('/api/donations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            donor_name: donorName,
            amount: amount,
            type: type
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Donation added successfully!');
            bootstrap.Modal.getInstance(document.getElementById('addDonationModal')).hide();
            loadDonations();
        } else {
            alert('❌ Error: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error adding donation');
    });
}

// Load functions
function loadVolunteers() {
    console.log('📋 Loading volunteers...');
    fetch('/api/volunteers')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Volunteers loaded:', data);
        const tbody = document.getElementById('volunteersTableBody');
        tbody.innerHTML = '';
        
        if (data.volunteers && data.volunteers.length > 0) {
            data.volunteers.forEach(volunteer => {
                const row = `
                    <tr>
                        <td>${volunteer.name}</td>
                        <td>${volunteer.email}</td>
                        <td>${volunteer.phone}</td>
                        <td>
                            <button class="btn btn-sm btn-primary btn-action" onclick="editVolunteer(${volunteer.id})">Edit</button>
                            <button class="btn btn-sm btn-danger btn-action" onclick="deleteVolunteer(${volunteer.id})">Delete</button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No volunteers found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading volunteers:', error);
        document.getElementById('volunteersTableBody').innerHTML = '<tr><td colspan="4" class="text-center">Error loading volunteers</td></tr>';
    });
}

function loadCamps() {
    console.log('🏥 Loading camps...');
    fetch('/api/camps')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Camps loaded:', data);
        const tbody = document.getElementById('campsTableBody');
        tbody.innerHTML = '';
        
        if (data.camps && data.camps.length > 0) {
            data.camps.forEach(camp => {
                const row = `
                    <tr>
                        <td>${camp.name}</td>
                        <td>${camp.location}</td>
                        <td>${camp.camp_date}</td>
                        <td>${camp.type}</td>
                        <td>
                            <button class="btn btn-sm btn-primary btn-action" onclick="editCamp(${camp.id})">Edit</button>
                            <button class="btn btn-sm btn-danger btn-action" onclick="deleteCamp(${camp.id})">Delete</button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No camps found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading camps:', error);
        document.getElementById('campsTableBody').innerHTML = '<tr><td colspan="5" class="text-center">Error loading camps</td></tr>';
    });
}

function loadDonations() {
    console.log('💰 Loading donations...');
    fetch('/api/donations')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Donations loaded:', data);
        const tbody = document.getElementById('donationsTableBody');
        tbody.innerHTML = '';
        
        if (data.donations && data.donations.length > 0) {
            data.donations.forEach(donation => {
                const row = `
                    <tr>
                        <td>${donation.donor_name}</td>
                        <td>$${donation.amount}</td>
                        <td>${donation.type}</td>
                        <td>${donation.date}</td>
                        <td>
                            <button class="btn btn-sm btn-primary btn-action" onclick="editDonation(${donation.id})">Edit</button>
                            <button class="btn btn-sm btn-danger btn-action" onclick="deleteDonation(${donation.id})">Delete</button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No donations found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading donations:', error);
        document.getElementById('donationsTableBody').innerHTML = '<tr><td colspan="5" class="text-center">Error loading donations</td></tr>';
    });
}

function loadGallery() {
    console.log('🖼️ Loading gallery...');
    fetch('/api/media')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Gallery loaded:', data);
        const grid = document.getElementById('galleryGrid');
        grid.innerHTML = '';
        
        if (data.media && data.media.length > 0) {
            data.media.forEach(item => {
                const mediaItem = `
                    <div class="col-md-4 mb-3">
                        <div class="card media-item">
                            <img src="${item.file_path}" class="card-img-top" alt="${item.title}" style="height: 200px; object-fit: cover;">
                            <div class="card-body">
                                <h5 class="card-title">${item.title}</h5>
                                <p class="card-text"><small class="text-muted">${item.type}</small></p>
                                <button class="btn btn-sm btn-danger" onclick="deleteMedia(${item.id})">Delete</button>
                            </div>
                        </div>
                    </div>
                `;
                grid.innerHTML += mediaItem;
            });
        } else {
            grid.innerHTML = '<div class="col-12 text-center"><p class="text-muted">No media found</p></div>';
        }
    })
    .catch(error => {
        console.error('Error loading gallery:', error);
        document.getElementById('galleryGrid').innerHTML = '<div class="col-12 text-center"><p class="text-muted">Error loading gallery</p></div>';
    });
}

function loadAttendance() {
    console.log('📋 Loading attendance...');
    fetch('/api/attendance')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Attendance loaded:', data);
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        if (data.attendance && data.attendance.length > 0) {
            data.attendance.forEach(record => {
                const row = `
                    <tr>
                        <td>${record.volunteer_name}</td>
                        <td>${record.camp_name || 'N/A'}</td>
                        <td>${record.date}</td>
                        <td>${record.check_in || 'N/A'}</td>
                        <td>${record.check_out || 'N/A'}</td>
                        <td><span class="badge bg-${record.status === 'present' ? 'success' : record.status === 'absent' ? 'danger' : 'warning'}">${record.status}</span></td>
                        <td>
                            <button class="btn btn-sm btn-primary btn-action" onclick="editAttendance(${record.id})">Edit</button>
                            <button class="btn btn-sm btn-danger btn-action" onclick="deleteAttendance(${record.id})">Delete</button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center">No attendance records found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading attendance:', error);
        document.getElementById('attendanceTableBody').innerHTML = '<tr><td colspan="7" class="text-center">Error loading attendance</td></tr>';
    });
}

function loadAnalytics() {
    console.log('📊 Loading analytics...');
    fetch('/api/analytics')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Analytics loaded:', data);
        
        // Update dashboard stats
        document.getElementById('totalVolunteers').textContent = data.total_volunteers || 0;
        document.getElementById('totalCamps').textContent = data.total_camps || 0;
        document.getElementById('totalDonations').textContent = '$' + (data.total_donations || 0);
        document.getElementById('presentToday').textContent = data.present_today || 0;
        document.getElementById('activeVolunteers').textContent = data.active_volunteers || 0;
        document.getElementById('monthlyDonations').textContent = '$' + (data.monthly_donations || 0);
        
        // Destroy existing charts
        Object.values(charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        
        // Camp Types Chart
        const campCtx = document.getElementById('campChart').getContext('2d');
        charts.camp = new Chart(campCtx, {
            type: 'doughnut',
            data: {
                labels: data.camp_stats?.map(s => s.type) || [],
                datasets: [{
                    data: data.camp_stats?.map(s => s.count) || [],
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#FF9F40'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error loading analytics:', error);
    });
}

function generatePDFReport() {
    console.log('📄 Generating PDF report...');
    fetch('/api/reports/pdf')
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'mathruseva_foundation_report.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        console.log('✅ PDF report generated and downloaded');
    })
    .catch(error => {
        console.error('Error generating PDF:', error);
        alert('❌ Error generating PDF report');
    });
}

// Delete functions
function deleteVolunteer(volunteerId) {
    if (confirm('Are you sure you want to delete this volunteer?')) {
        fetch(`/api/volunteers/${volunteerId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Volunteer deleted successfully!');
                loadVolunteers();
            } else {
                alert('❌ Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting volunteer:', error);
            alert('❌ Error deleting volunteer');
        });
    }
}

function deleteCamp(campId) {
    if (confirm('Are you sure you want to delete this camp?')) {
        fetch(`/api/camps/${campId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Camp deleted successfully!');
                loadCamps();
            } else {
                alert('❌ Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting camp:', error);
            alert('❌ Error deleting camp');
        });
    }
}

function deleteDonation(donationId) {
    if (confirm('Are you sure you want to delete this donation?')) {
        fetch(`/api/donations/${donationId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Donation deleted successfully!');
                loadDonations();
            } else {
                alert('❌ Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting donation:', error);
            alert('❌ Error deleting donation');
        });
    }
}

function deleteMedia(mediaId) {
    if (confirm('Are you sure you want to delete this media?')) {
        fetch(`/api/media/${mediaId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Media deleted successfully!');
                loadGallery();
            } else {
                alert('❌ Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting media:', error);
            alert('❌ Error deleting media');
        });
    }
}

function deleteAttendance(attendanceId) {
    if (confirm('Are you sure you want to delete this attendance record?')) {
        fetch(`/api/attendance/${attendanceId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Attendance record deleted successfully!');
                loadAttendance();
            } else {
                alert('❌ Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting attendance:', error);
            alert('❌ Error deleting attendance record');
        });
    }
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Dashboard ready!');
    loadAnalytics();
});
