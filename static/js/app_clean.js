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
    });
    
    // Find and activate the clicked nav link
    const activeLink = document.querySelector(`[onclick*="showSection('${sectionId}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
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
    
    console.log('📍 Current section is now:', sectionId);
}

// Modal functions
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
            donation_type: type
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
    fetch('/api/volunteers')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('volunteersTableBody');
        tbody.innerHTML = '';
        
        if (data.volunteers && data.volunteers.length > 0) {
            data.volunteers.forEach(volunteer => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${volunteer.name}</td>
                    <td>${volunteer.email}</td>
                    <td>${volunteer.phone}</td>
                    <td>Volunteer</td>
                    <td><span class="badge bg-success">Active</span></td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="deleteVolunteer(${volunteer.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No volunteers found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading volunteers:', error);
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
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${camp.name}</td>
                    <td>${camp.location}</td>
                    <td>${camp.camp_date}</td>
                    <td>${camp.type}</td>
                    <td><span class="badge bg-primary">Upcoming</span></td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="deleteCamp(${camp.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No camps found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading camps:', error);
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
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${donation.donor_name}</td>
                    <td>$${donation.amount}</td>
                    <td>${donation.donation_type}</td>
                    <td>${donation.donation_date}</td>
                    <td>-</td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="deleteDonation(${donation.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No donations found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading donations:', error);
    });
}

function loadGallery() {
    fetch('/api/media')
    .then(response => response.json())
    .then(data => {
        const gallery = document.getElementById('mediaGallery');
        gallery.innerHTML = '';
        
        if (data.media && data.media.length > 0) {
            data.media.forEach(item => {
                const col = document.createElement('div');
                col.className = 'col-md-4 mb-3';
                col.innerHTML = `
                    <div class="card">
                        <img src="${item.file_path}" class="card-img-top" alt="${item.description}">
                        <div class="card-body">
                            <p class="card-text">${item.description}</p>
                        </div>
                    </div>
                `;
                gallery.appendChild(col);
            });
        } else {
            gallery.innerHTML = '<div class="col-12 text-center"><p class="text-muted">No media found</p></div>';
        }
    })
    .catch(error => {
        console.error('Error loading gallery:', error);
    });
}

function loadAttendance() {
    fetch('/api/attendance')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        if (data.attendance && data.attendance.length > 0) {
            data.attendance.forEach(record => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${record.volunteer_name}</td>
                    <td>${record.camp_name}</td>
                    <td>${record.attendance_date}</td>
                    <td><span class="badge bg-success">${record.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="deleteAttendance(${record.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No attendance records found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error loading attendance:', error);
    });
}

function loadAnalytics() {
    fetch('/api/analytics')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Analytics loaded:', data);
        
        // Destroy existing charts
        Object.values(charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        
        // Camp Statistics Chart
        const campCtx = document.getElementById('campChart');
        if (campCtx) {
            const campData = data.camp_stats || [];
            const labels = campData.map(s => s.type) || [];
            const counts = campData.map(s => s.count) || [];
            
            charts.camp = new Chart(campCtx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: counts,
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#FF9F40'],
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
        }
        
        // Volunteer Trends Chart
        const volunteerCtx = document.getElementById('volunteerChart');
        if (volunteerCtx) {
            const volunteerData = data.volunteer_trends || [];
            const labels = volunteerData.map(t => t.month) || [];
            const counts = volunteerData.map(t => t.count) || [];
            
            charts.volunteer = new Chart(volunteerCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'New Volunteers',
                        data: counts,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // Donation Trends Chart
        const donationCtx = document.getElementById('donationChart');
        if (donationCtx) {
            const donationData = data.donation_trends || [];
            const labels = donationData.map(t => t.month) || [];
            const amounts = donationData.map(t => t.total) || [];
            
            charts.donation = new Chart(donationCtx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Donation Amount ($)',
                        data: amounts,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
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
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    })
    .catch(error => {
        console.error('Error loading analytics:', error);
    });
}

// Delete functions
function deleteVolunteer(id) {
    if (confirm('Are you sure you want to delete this volunteer?')) {
        fetch(`/api/volunteers/${id}`, {
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
            console.error('Error:', error);
            alert('❌ Error deleting volunteer');
        });
    }
}

function deleteCamp(id) {
    if (confirm('Are you sure you want to delete this camp?')) {
        fetch(`/api/camps/${id}`, {
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
            console.error('Error:', error);
            alert('❌ Error deleting camp');
        });
    }
}

function deleteDonation(id) {
    if (confirm('Are you sure you want to delete this donation?')) {
        fetch(`/api/donations/${id}`, {
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
            console.error('Error:', error);
            alert('❌ Error deleting donation');
        });
    }
}

function deleteAttendance(id) {
    if (confirm('Are you sure you want to delete this attendance record?')) {
        fetch(`/api/attendance/${id}`, {
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
            console.error('Error:', error);
            alert('❌ Error deleting attendance record');
        });
    }
}

// PDF Report function
function generatePDFReport() {
    fetch('/api/reports/pdf', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('PDF generation failed');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'mathruseva_foundation_report.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error generating PDF:', error);
        alert('❌ Error generating PDF report');
    });
}

// Analytics functions
function refreshAnalytics() {
    console.log('🔄 Refreshing analytics...');
    loadAnalytics();
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing dashboard...');
    
    // Load dashboard overview data
    fetch('/api/analytics')
    .then(response => response.json())
    .then(data => {
        // Update dashboard metrics
        if (data.total_volunteers) {
            document.getElementById('totalVolunteers').textContent = data.total_volunteers;
        }
        if (data.total_camps) {
            document.getElementById('totalCamps').textContent = data.total_camps;
        }
        if (data.total_donations) {
            document.getElementById('totalDonations').textContent = data.total_donations;
        }
        if (data.upcoming_camps) {
            document.getElementById('upcomingCamps').textContent = data.upcoming_camps;
        }
        if (data.active_volunteers) {
            document.getElementById('activeVolunteers').textContent = data.active_volunteers;
        }
        if (data.monthly_donations) {
            document.getElementById('monthlyDonations').textContent = data.monthly_donations;
        }
    })
    .catch(error => {
        console.error('Error loading dashboard data:', error);
    });
    
    // Media file preview
    const mediaFileInput = document.getElementById('mediaFile');
    if (mediaFileInput) {
        mediaFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const preview = document.getElementById('mediaPreview');
            
            if (file && preview) {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.innerHTML = `<img src="${e.target.result}" class="img-fluid" style="max-height: 200px;">`;
                    };
                    reader.readAsDataURL(file);
                } else if (file.type.startsWith('video/')) {
                    preview.innerHTML = `<div class="alert alert-info"><i class="fas fa-video me-2"></i>Video selected: ${file.name}</div>`;
                }
            }
        });
    }
    
    // Set today's date as default for donation date
    const donationDateInput = document.getElementById('donationDate');
    if (donationDateInput) {
        donationDateInput.value = new Date().toISOString().split('T')[0];
    }
    
    // Set today's date as default for camp date
    const campDateInput = document.getElementById('campDate');
    if (campDateInput) {
        campDateInput.value = new Date().toISOString().split('T')[0];
    }
    
    console.log('✅ Dashboard ready!');
});
