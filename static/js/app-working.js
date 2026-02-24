// Mathruseva Foundation - Working JavaScript with Upload
console.log('Working app.js loaded!');

// Global variables
let currentSection = 'dashboard';

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    loadDashboard();
    loadVolunteers();
    loadCamps();
    loadDonations();
    initializeEventListeners();
});

// Navigation and section management
function showSection(sectionId) {
    console.log('Showing section:', sectionId);
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    document.getElementById(sectionId).style.display = 'block';
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[href="#${sectionId}"]`).classList.add('active');
    
    currentSection = sectionId;
    
    // Load section-specific data
    switch(sectionId) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'volunteers':
            loadVolunteers();
            break;
        case 'attendance':
            loadAttendance();
            break;
        case 'camps':
            loadCamps();
            break;
        case 'donations':
            loadDonations();
            break;
        case 'reports':
            loadReports();
            break;
        case 'analytics':
            loadAnalytics();
            break;
    }
}

// Initialize event listeners
function initializeEventListeners() {
    console.log('Initializing event listeners...');
    
    // Volunteer form submission
    const volunteerForm = document.getElementById('volunteerForm');
    if (volunteerForm) {
        volunteerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addVolunteer();
        });
    }
    
    // Camp form submission
    const campForm = document.getElementById('campForm');
    if (campForm) {
        campForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addCamp();
        });
    }
    
    // Donation form submission
    const donationForm = document.getElementById('donationForm');
    if (donationForm) {
        donationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addDonation();
        });
    }
    
    // Search functionality
    const volunteerSearch = document.getElementById('volunteerSearch');
    if (volunteerSearch) {
        volunteerSearch.addEventListener('input', function(e) {
            filterVolunteers(e.target.value);
        });
    }
    
    // Filter functionality
    const campTypeFilter = document.getElementById('campTypeFilter');
    if (campTypeFilter) {
        campTypeFilter.addEventListener('change', function(e) {
            filterCamps(e.target.value);
        });
    }
    
    const donationTypeFilter = document.getElementById('donationTypeFilter');
    if (donationTypeFilter) {
        donationTypeFilter.addEventListener('change', function(e) {
            filterDonations(e.target.value);
        });
    }
}

// Dashboard functions
async function loadDashboard() {
    try {
        console.log('Loading dashboard...');
        // Update stats with sample data for now
        const volunteersCount = document.getElementById('totalVolunteers');
        const campsCount = document.getElementById('totalCamps');
        const donationsCount = document.getElementById('totalDonations');
        
        if (volunteersCount) volunteersCount.textContent = '0';
        if (campsCount) campsCount.textContent = '0';
        if (donationsCount) donationsCount.textContent = '0';
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Volunteer functions
async function loadVolunteers() {
    try {
        console.log('Loading volunteers...');
        const response = await fetch('/api/volunteers');
        const volunteers = await response.json();
        displayVolunteers(volunteers);
    } catch (error) {
        console.error('Error loading volunteers:', error);
    }
}

function displayVolunteers(volunteers) {
    const tbody = document.getElementById('volunteersTableBody');
    if (tbody) {
        tbody.innerHTML = '';
        
        if (volunteers && volunteers.length > 0) {
            volunteers.forEach(volunteer => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${volunteer.name || 'N/A'}</td>
                    <td>${volunteer.email || 'N/A'}</td>
                    <td>${volunteer.phone || 'N/A'}</td>
                    <td><span class="badge bg-primary">${volunteer.role || 'N/A'}</span></td>
                    <td><span class="badge bg-success">${volunteer.status || 'Active'}</span></td>
                    <td>${volunteer.join_date || 'N/A'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editVolunteer(${volunteer.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteVolunteer(${volunteer.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No volunteers found</td></tr>';
        }
    }
}

async function addVolunteer() {
    const formData = {
        name: document.getElementById('volunteerName').value,
        email: document.getElementById('volunteerEmail').value,
        phone: document.getElementById('volunteerPhone').value,
        role: document.getElementById('volunteerRole').value,
        skills: document.getElementById('volunteerSkills').value,
        availability: document.getElementById('volunteerAvailability').value
    };
    
    try {
        const response = await fetch('/api/volunteers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Volunteer added successfully', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('volunteerModal'));
            if (modal) modal.hide();
            document.getElementById('volunteerForm').reset();
            loadVolunteers();
        } else {
            throw new Error('Failed to add volunteer');
        }
    } catch (error) {
        console.error('Error adding volunteer:', error);
        showAlert('Error adding volunteer', 'danger');
    }
}

// Camp functions
async function loadCamps() {
    try {
        console.log('Loading camps...');
        const response = await fetch('/api/camps');
        const camps = await response.json();
        displayCamps(camps);
    } catch (error) {
        console.error('Error loading camps:', error);
    }
}

function displayCamps(camps) {
    const tbody = document.getElementById('campsTableBody');
    if (tbody) {
        tbody.innerHTML = '';
        
        if (camps && camps.length > 0) {
            camps.forEach(camp => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${camp.name || 'N/A'}</td>
                    <td><span class="badge bg-info">${camp.type || 'N/A'}</span></td>
                    <td>${camp.location || 'N/A'}</td>
                    <td>${camp.camp_date || 'N/A'}</td>
                    <td><span class="badge bg-primary">${camp.status || 'Planned'}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editCamp(${camp.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteCamp(${camp.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No camps found</td></tr>';
        }
    }
}

async function addCamp() {
    const formData = {
        name: document.getElementById('campName').value,
        type: document.getElementById('campType').value,
        location: document.getElementById('campLocation').value,
        camp_date: document.getElementById('campDate').value,
        description: document.getElementById('campDescription').value
    };
    
    try {
        const response = await fetch('/api/camps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Camp added successfully', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('campModal'));
            if (modal) modal.hide();
            document.getElementById('campForm').reset();
            loadCamps();
        } else {
            throw new Error('Failed to add camp');
        }
    } catch (error) {
        console.error('Error adding camp:', error);
        showAlert('Error adding camp', 'danger');
    }
}

// Donation functions
async function loadDonations() {
    try {
        console.log('Loading donations...');
        const response = await fetch('/api/donations');
        const donations = await response.json();
        displayDonations(donations);
    } catch (error) {
        console.error('Error loading donations:', error);
    }
}

function displayDonations(donations) {
    const tbody = document.getElementById('donationsTableBody');
    if (tbody) {
        tbody.innerHTML = '';
        
        if (donations && donations.length > 0) {
            donations.forEach(donation => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${donation.donor_name || 'Anonymous'}</td>
                    <td><span class="badge bg-warning">${donation.donation_type || 'N/A'}</span></td>
                    <td>${donation.quantity || '0'}</td>
                    <td>${donation.donation_date || 'N/A'}</td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No donations found</td></tr>';
        }
    }
}

async function addDonation() {
    const formData = {
        camp_id: document.getElementById('donationCamp').value || null,
        donation_type: document.getElementById('donationType').value,
        quantity: document.getElementById('donationQuantity').value,
        donor_name: document.getElementById('donorName').value,
        donation_date: document.getElementById('donationDate').value,
        notes: document.getElementById('donationNotes').value
    };
    
    try {
        const response = await fetch('/api/donations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Donation added successfully', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('donationModal'));
            if (modal) modal.hide();
            document.getElementById('donationForm').reset();
            loadDonations();
        } else {
            throw new Error('Failed to add donation');
        }
    } catch (error) {
        console.error('Error adding donation:', error);
        showAlert('Error adding donation', 'danger');
    }
}

// Media functions
async function loadMedia() {
    try {
        console.log('Loading media...');
        const response = await fetch('/api/media/all');
        const data = await response.json();
        displayMedia(data.media);
    } catch (error) {
        console.error('Error loading media:', error);
    }
}

function displayMedia(mediaItems) {
    const gallery = document.getElementById('mediaGallery');
    if (gallery) {
        gallery.innerHTML = '';
        
        if (mediaItems && mediaItems.length > 0) {
            mediaItems.forEach(media => {
                const mediaCol = document.createElement('div');
                mediaCol.className = 'col-md-4 mb-4';
                
                if (media.media_type === 'photo') {
                    mediaCol.innerHTML = `
                        <div class="card">
                            <img src="${media.media_url}" class="card-img-top" alt="${media.caption || 'Camp photo'}" 
                                 style="height: 200px; object-fit: cover;" onerror="this.src='https://via.placeholder.com/400x200?text=Image+Not+Found'">
                            <div class="card-body">
                                <h6 class="card-title">${media.camp_name || 'General'}</h6>
                                <p class="card-text small text-muted">${media.camp_location || 'Unknown'}</p>
                                <p class="card-text">${media.caption || 'No caption'}</p>
                                <small class="text-muted">${new Date(media.upload_date).toLocaleDateString()}</small>
                                <button class="btn btn-sm btn-outline-danger float-end" onclick="deleteMedia(${media.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    `;
                } else if (media.media_type === 'video') {
                    mediaCol.innerHTML = `
                        <div class="card">
                            <div class="card-img-top d-flex align-items-center justify-content-center bg-light" 
                                 style="height: 200px;">
                                <i class="fas fa-play-circle fa-3x text-primary"></i>
                            </div>
                            <div class="card-body">
                                <h6 class="card-title">${media.camp_name || 'General'}</h6>
                                <p class="card-text small text-muted">${media.camp_location || 'Unknown'}</p>
                                <p class="card-text">${media.caption || 'No caption'}</p>
                                <a href="${media.media_url}" target="_blank" class="btn btn-sm btn-primary">
                                    <i class="fas fa-play"></i> Watch Video
                                </a>
                                <button class="btn btn-sm btn-outline-danger float-end" onclick="deleteMedia(${media.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    `;
                }
                
                gallery.appendChild(mediaCol);
            });
        } else {
            gallery.innerHTML = '<div class="col-12"><p class="text-muted">No media found.</p></div>';
        }
    }
}

// Upload Media Function
async function uploadMedia() {
    console.log('uploadMedia function called');
    
    try {
        const fileInput = document.getElementById('mediaFile');
        const campId = document.getElementById('mediaCamp').value;
        const caption = document.getElementById('mediaCaption').value;
        
        if (!campId) {
            showAlert('Please select a camp', 'warning');
            return;
        }
        
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
            showAlert('Please select a file', 'warning');
            return;
        }
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('mediaFile', file);
        formData.append('camp_id', campId);
        formData.append('caption', caption);
        
        const response = await fetch('/api/media/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Media uploaded successfully', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('mediaModal'));
            if (modal) modal.hide();
            document.getElementById('mediaUploadForm').reset();
            loadMedia(); // Reload media gallery
        } else {
            throw new Error('Failed to upload media');
        }
        
    } catch (error) {
        console.error('Error uploading media:', error);
        showAlert('Error uploading media: ' + error.message, 'danger');
    }
}

// Delete media function
async function deleteMedia(mediaId) {
    if (confirm('Are you sure you want to delete this media?')) {
        try {
            const response = await fetch(`/api/media/${mediaId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Media deleted successfully', 'success');
                loadMedia();
            } else {
                throw new Error('Failed to delete media');
            }
        } catch (error) {
            console.error('Error deleting media:', error);
            showAlert('Error deleting media', 'danger');
        }
    }
}

// Load camps for media upload dropdown
async function loadCampsForMedia() {
    try {
        const response = await fetch('/api/camps');
        const camps = await response.json();
        
        const select = document.getElementById('mediaCamp');
        if (select) {
            select.innerHTML = '<option value="">Select Camp</option>';
            
            if (camps && camps.length > 0) {
                camps.forEach(camp => {
                    const option = document.createElement('option');
                    option.value = camp.id;
                    option.textContent = `${camp.name} - ${camp.location}`;
                    select.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading camps for media:', error);
    }
}

// Filter functions
function filterVolunteers(searchTerm) {
    console.log('Filtering volunteers:', searchTerm);
}

function filterCamps(type) {
    console.log('Filtering camps:', type);
}

function filterDonations(type) {
    console.log('Filtering donations:', type);
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function getStatusColor(status) {
    switch(status) {
        case 'Active': return 'success';
        case 'Completed': return 'success';
        case 'Planned': return 'primary';
        case 'In Progress': return 'warning';
        default: return 'secondary';
    }
}

function showAlert(message, type) {
    console.log('Alert:', message, type);
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.parentElement.removeChild(alertDiv);
        }
    }, 3000);
}

// Load Reports
async function loadReports() {
    console.log('Loading reports...');
    try {
        // Initialize progress bars with animations
        initializeProgressBars();
    } catch (error) {
        console.error('Error loading reports:', error);
    }
}

// Initialize Progress Bars
function initializeProgressBars() {
    // Eye Camp Progress
    const eyeCampProgress = document.getElementById('eyeCampProgress');
    if (eyeCampProgress) {
        eyeCampProgress.innerHTML = `
            <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: 0%; background: var(--gradient-primary);" 
                     aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">75%</div>
            </div>
        `;
        // Animate progress bar
        setTimeout(() => {
            eyeCampProgress.querySelector('.progress-bar').style.width = '75%';
        }, 500);
    }
    
    // Blood Donation Progress
    const bloodDonationProgress = document.getElementById('bloodDonationProgress');
    if (bloodDonationProgress) {
        bloodDonationProgress.innerHTML = `
            <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: 0%; background: var(--gradient-success);" 
                     aria-valuenow="60" aria-valuemin="0" aria-valuemax="100">60%</div>
            </div>
        `;
        // Animate progress bar
        setTimeout(() => {
            bloodDonationProgress.querySelector('.progress-bar').style.width = '60%';
        }, 700);
    }
}

// Load Analytics
async function loadAnalytics() {
    console.log('Loading analytics...');
    try {
        // Initialize charts and analytics
        initializeCharts();
        initializeMaps();
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Initialize Charts
function initializeCharts() {
    console.log('Initializing charts...');
    
    // Volunteer Performance Chart
    const volunteerCtx = document.getElementById('volunteerPerformanceChart');
    if (volunteerCtx) {
        new Chart(volunteerCtx, {
            type: 'doughnut',
            data: {
                labels: ['Active', 'Inactive', 'On Leave', 'New Volunteers'],
                datasets: [{
                    data: [65, 20, 15, 12],
                    backgroundColor: [
                        'rgba(39, 174, 96, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(243, 156, 18, 0.8)',
                        'rgba(52, 152, 219, 0.8)'
                    ],
                    borderColor: [
                        'rgba(39, 174, 96, 1)',
                        'rgba(231, 76, 60, 1)',
                        'rgba(243, 156, 18, 1)',
                        'rgba(52, 152, 219, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
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
    }
    
    // Donation Impact Chart
    const donationCtx = document.getElementById('donationImpactChart');
    if (donationCtx) {
        new Chart(donationCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Donations ($)',
                    data: [12000, 19000, 15000, 22000, 18000, 25000],
                    backgroundColor: 'rgba(74, 144, 226, 0.8)',
                    borderColor: 'rgba(74, 144, 226, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    hoverBackgroundColor: 'rgba(74, 144, 226, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
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
    }
    
    // Attendance Trend Chart (if element exists)
    const attendanceCtx = document.getElementById('attendanceTrendChart');
    if (attendanceCtx) {
        new Chart(attendanceCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Attendance Rate',
                    data: [85, 88, 92, 87, 90, 75, 70],
                    borderColor: 'rgba(39, 174, 96, 1)',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(39, 174, 96, 1)',
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
                    legend: {
                        display: false
                    },
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
    }
    
    // Camp Distribution Chart (if element exists)
    const campCtx = document.getElementById('campDistributionChart');
    if (campCtx) {
        new Chart(campCtx, {
            type: 'polarArea',
            data: {
                labels: ['Eye Camps', 'Blood Donation', 'General Health', 'Donation Drives'],
                datasets: [{
                    data: [12, 8, 15, 6],
                    backgroundColor: [
                        'rgba(74, 144, 226, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(39, 174, 96, 0.8)',
                        'rgba(243, 156, 18, 0.8)'
                    ],
                    borderColor: [
                        'rgba(74, 144, 226, 1)',
                        'rgba(231, 76, 60, 1)',
                        'rgba(39, 174, 96, 1)',
                        'rgba(243, 156, 18, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: {
                                size: 11
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
    }
}

// Initialize Maps
function initializeMaps() {
    console.log('Initializing maps...');
    
    const mapElement = document.getElementById('campLocationsMap');
    if (mapElement && typeof L !== 'undefined') {
        const map = L.map('campLocationsMap').setView([20.5937, 78.9629], 5);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Add sample camp locations
        const camps = [
            {name: 'Mumbai Camp', lat: 19.0760, lng: 72.8777},
            {name: 'Delhi Camp', lat: 28.7041, lng: 77.1025},
            {name: 'Bangalore Camp', lat: 12.9716, lng: 77.5946}
        ];
        
        camps.forEach(camp => {
            L.marker([camp.lat, camp.lng])
                .addTo(map)
                .bindPopup(camp.name);
        });
    }
}

// Load Attendance
async function loadAttendance() {
    console.log('Loading attendance...');
    try {
        // Set today's date as default
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('attendanceDate').value = today;
        document.getElementById('attendanceDateModal').value = today;
        
        // Load attendance data
        await loadAttendanceData();
        await loadAttendanceStats();
        await loadCampsForAttendance();
        await loadVolunteersForAttendance();
    } catch (error) {
        console.error('Error loading attendance:', error);
    }
}

// Load Attendance Data
async function loadAttendanceData() {
    try {
        const response = await fetch('/api/volunteer/attendance');
        const attendance = await response.json();
        
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        if (attendance && attendance.length > 0) {
            attendance.forEach(record => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${record.volunteer_name}</td>
                    <td>${record.camp_name}</td>
                    <td>${formatDate(record.attendance_date)}</td>
                    <td>${record.check_in_time || '-'}</td>
                    <td>${record.check_out_time || '-'}</td>
                    <td><span class="attendance-status ${record.status}">${record.status.toUpperCase()}</span></td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editAttendance(${record.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteAttendance(${record.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center">No attendance records found</td></tr>';
        }
    } catch (error) {
        console.error('Error loading attendance data:', error);
    }
}

// Load Attendance Stats
async function loadAttendanceStats() {
    try {
        const response = await fetch('/api/volunteer/attendance/stats');
        const stats = await response.json();
        
        document.getElementById('totalPresent').textContent = stats.present || 0;
        document.getElementById('totalAbsent').textContent = stats.absent || 0;
        document.getElementById('totalLate').textContent = stats.late || 0;
        document.getElementById('attendanceRate').textContent = stats.rate || '0%';
    } catch (error) {
        console.error('Error loading attendance stats:', error);
        // Set default values
        document.getElementById('totalPresent').textContent = '0';
        document.getElementById('totalAbsent').textContent = '0';
        document.getElementById('totalLate').textContent = '0';
        document.getElementById('attendanceRate').textContent = '0%';
    }
}

// Load Camps for Attendance
async function loadCampsForAttendance() {
    try {
        const response = await fetch('/api/camps');
        const camps = await response.json();
        
        const select = document.getElementById('attendanceCamp');
        const filterSelect = document.getElementById('campFilter');
        
        if (select && filterSelect) {
            select.innerHTML = '<option value="">Select Camp</option>';
            filterSelect.innerHTML = '<option value="">All Camps</option>';
            
            if (camps && camps.length > 0) {
                camps.forEach(camp => {
                    const option1 = document.createElement('option');
                    option1.value = camp.id;
                    option1.textContent = camp.name;
                    select.appendChild(option1);
                    
                    const option2 = document.createElement('option');
                    option2.value = camp.id;
                    option2.textContent = camp.name;
                    filterSelect.appendChild(option2);
                });
            }
        }
    } catch (error) {
        console.error('Error loading camps for attendance:', error);
    }
}

// Load Volunteers for Attendance
async function loadVolunteersForAttendance() {
    try {
        const response = await fetch('/api/volunteers');
        const volunteers = await response.json();
        
        const select = document.getElementById('attendanceVolunteer');
        if (select) {
            select.innerHTML = '<option value="">Select Volunteer</option>';
            
            if (volunteers && volunteers.length > 0) {
                volunteers.forEach(volunteer => {
                    const option = document.createElement('option');
                    option.value = volunteer.id;
                    option.textContent = volunteer.name;
                    select.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading volunteers for attendance:', error);
    }
}

// Mark Attendance
async function markAttendance() {
    try {
        const volunteerId = document.getElementById('attendanceVolunteer').value;
        const campId = document.getElementById('attendanceCamp').value;
        const date = document.getElementById('attendanceDateModal').value;
        const checkInTime = document.getElementById('checkInTime').value;
        const checkOutTime = document.getElementById('checkOutTime').value;
        const status = document.getElementById('attendanceStatus').value;
        const notes = document.getElementById('attendanceNotes').value;
        
        if (!volunteerId || !campId || !date || !checkInTime || !status) {
            alert('Please fill in all required fields');
            return;
        }
        
        const attendanceData = {
            volunteer_id: volunteerId,
            camp_id: campId,
            date: date,
            check_in_time: checkInTime,
            check_out_time: checkOutTime,
            status: status,
            notes: notes
        };
        
        const response = await fetch('/api/volunteer/attendance/mark', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(attendanceData)
        });
        
        if (response.ok) {
            alert('Attendance marked successfully!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('attendanceModal'));
            if (modal) modal.hide();
            document.getElementById('attendanceForm').reset();
            loadAttendanceData();
            loadAttendanceStats();
        } else {
            throw new Error('Failed to mark attendance');
        }
        
    } catch (error) {
        console.error('Error marking attendance:', error);
        alert('Error marking attendance: ' + error.message);
    }
}

// Generate Attendance Report
function generateAttendanceReport() {
    alert('Attendance report will be generated and downloaded!');
}

// Edit Attendance
function editAttendance(id) {
    alert('Edit attendance functionality for ID: ' + id);
}

// Delete Attendance
async function deleteAttendance(id) {
    if (confirm('Are you sure you want to delete this attendance record?')) {
        try {
            const response = await fetch(`/api/volunteer/attendance/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert('Attendance record deleted successfully!');
                loadAttendanceData();
                loadAttendanceStats();
            } else {
                throw new Error('Failed to delete attendance record');
            }
        } catch (error) {
            console.error('Error deleting attendance:', error);
            alert('Error deleting attendance: ' + error.message);
        }
    }
}
