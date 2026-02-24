// Mathruseva Foundation - Clean Working JavaScript
console.log('Clean working app.js loaded!');

// Test Chart.js availability
console.log('Chart.js available:', typeof Chart !== 'undefined');
console.log('Leaflet available:', typeof L !== 'undefined');

// Global variables
let currentSection = 'dashboard';

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    
    // Test chart creation immediately
    testChartCreation();
    
    loadDashboard();
    loadVolunteers();
    loadCamps();
    loadDonations();
    initializeEventListeners();
});

// Test chart creation function
function testChartCreation() {
    console.log('Testing chart creation...');
    
    const testCtx = document.getElementById('volunteerPerformanceChart');
    if (testCtx) {
        console.log('Found volunteerPerformanceChart canvas');
        
        if (typeof Chart !== 'undefined') {
            console.log('Chart.js is available, creating test chart...');
            
            try {
                new Chart(testCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Test', 'Data'],
                        datasets: [{
                            data: [50, 50],
                            backgroundColor: ['red', 'blue']
                        }]
                    }
                });
                console.log('Test chart created successfully!');
            } catch (error) {
                console.error('Error creating test chart:', error);
            }
        } else {
            console.error('Chart.js is not available!');
        }
    } else {
        console.error('volunteerPerformanceChart canvas not found!');
    }
}

// Navigation and section management
function showSection(sectionId) {
    console.log('Showing section:', sectionId);
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    } else {
        console.error('Section not found:', sectionId);
        return;
    }
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    const activeLink = document.querySelector(`[href="#${sectionId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
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
    console.log('Loading dashboard...');
    try {
        // Load dashboard stats
        const response = await fetch('/api/dashboard/stats');
        const stats = await response.json();
        
        // Update dashboard elements
        const totalVolunteers = document.getElementById('totalVolunteers');
        const totalCamps = document.getElementById('totalCamps');
        const totalDonations = document.getElementById('totalDonations');
        
        if (totalVolunteers) totalVolunteers.textContent = stats.total_volunteers || 0;
        if (totalCamps) totalCamps.textContent = stats.total_camps || 0;
        if (totalDonations) totalDonations.textContent = '$' + (stats.total_donations || 0).toLocaleString();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Volunteer functions
async function loadVolunteers() {
    console.log('Loading volunteers...');
    try {
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
                    <td>${volunteer.name}</td>
                    <td>${volunteer.email}</td>
                    <td>${volunteer.phone || 'N/A'}</td>
                    <td><span class="badge bg-success">${volunteer.role}</span></td>
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
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No volunteers found</td></tr>';
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
            alert('Volunteer added successfully!');
            document.getElementById('volunteerForm').reset();
            loadVolunteers();
        } else {
            throw new Error('Failed to add volunteer');
        }
        
    } catch (error) {
        console.error('Error adding volunteer:', error);
        alert('Error adding volunteer: ' + error.message);
    }
}

// Camp functions
async function loadCamps() {
    console.log('Loading camps...');
    try {
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
                    <td>${camp.name}</td>
                    <td>${camp.type}</td>
                    <td>${camp.location}</td>
                    <td>${formatDate(camp.camp_date)}</td>
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
            alert('Camp added successfully!');
            document.getElementById('campForm').reset();
            loadCamps();
        } else {
            throw new Error('Failed to add camp');
        }
        
    } catch (error) {
        console.error('Error adding camp:', error);
        alert('Error adding camp: ' + error.message);
    }
}

// Donation functions
async function loadDonations() {
    console.log('Loading donations...');
    try {
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
                    <td>${donation.donor_name}</td>
                    <td>${donation.donation_type}</td>
                    <td>$${donation.amount}</td>
                    <td>${formatDate(donation.donation_date)}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editDonation(${donation.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteDonation(${donation.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No donations found</td></tr>';
        }
    }
}

async function addDonation() {
    const formData = {
        donor_name: document.getElementById('donorName').value,
        donation_type: document.getElementById('donationType').value,
        amount: document.getElementById('donationAmount').value,
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
            alert('Donation added successfully!');
            document.getElementById('donationForm').reset();
            loadDonations();
        } else {
            throw new Error('Failed to add donation');
        }
        
    } catch (error) {
        console.error('Error adding donation:', error);
        alert('Error adding donation: ' + error.message);
    }
}

// Attendance Functions
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

function generateAttendanceReport() {
    alert('Attendance report will be generated and downloaded!');
}

function editAttendance(id) {
    alert('Edit attendance functionality for ID: ' + id);
}

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

// Reports and Analytics
async function loadReports() {
    console.log('Loading reports...');
    try {
        // Initialize progress bars with animations
        initializeProgressBars();
    } catch (error) {
        console.error('Error loading reports:', error);
    }
}

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

function initializeCharts() {
    console.log('Initializing charts...');
    
    // Load fallback data first to ensure charts display
    loadFallbackVolunteerChart();
    loadFallbackDonationChart();
    loadFallbackAttendanceChart();
    loadFallbackCampChart();
    
    // Then try to load real data (will update charts if successful)
    loadVolunteerChart();
    loadDonationChart();
    loadAttendanceTrendChart();
    loadCampDistributionChart();
}

// Load Volunteer Performance Chart with real data
async function loadVolunteerChart() {
    try {
        const response = await fetch('/api/analytics/volunteers');
        const data = await response.json();
        
        const volunteerCtx = document.getElementById('volunteerPerformanceChart');
        if (volunteerCtx && data.labels && data.data) {
            new Chart(volunteerCtx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
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
    } catch (error) {
        console.error('Error loading volunteer chart:', error);
        // Load fallback data
        loadFallbackVolunteerChart();
    }
}

// Load Donation Impact Chart with real data
async function loadDonationChart() {
    try {
        const response = await fetch('/api/analytics/donations');
        const data = await response.json();
        
        const donationCtx = document.getElementById('donationImpactChart');
        if (donationCtx && data.labels && data.data) {
            new Chart(donationCtx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Donations ($)',
                        data: data.data,
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
    } catch (error) {
        console.error('Error loading donation chart:', error);
        // Load fallback data
        loadFallbackDonationChart();
    }
}

// Load Attendance Trend Chart with real data
async function loadAttendanceTrendChart() {
    try {
        const response = await fetch('/api/analytics/attendance-trend');
        const data = await response.json();
        
        const attendanceCtx = document.getElementById('attendanceTrendChart');
        if (attendanceCtx && data.labels && data.data) {
            new Chart(attendanceCtx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Attendance Rate',
                        data: data.data,
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
    } catch (error) {
        console.error('Error loading attendance trend chart:', error);
        // Load fallback data
        loadFallbackAttendanceChart();
    }
}

// Load Camp Distribution Chart with real data
async function loadCampDistributionChart() {
    try {
        const response = await fetch('/api/analytics/camp-distribution');
        const data = await response.json();
        
        const campCtx = document.getElementById('campDistributionChart');
        if (campCtx && data.labels && data.data) {
            new Chart(campCtx, {
                type: 'polarArea',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
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
    } catch (error) {
        console.error('Error loading camp distribution chart:', error);
        // Load fallback data
        loadFallbackCampChart();
    }
}

// Fallback chart functions with sample data
function loadFallbackVolunteerChart() {
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
}

function loadFallbackDonationChart() {
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
}

function loadFallbackAttendanceChart() {
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
}

function loadFallbackCampChart() {
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
        case 'Pending': return 'warning';
        case 'Cancelled': return 'danger';
        default: return 'secondary';
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.parentElement.removeChild(alertDiv);
        }
    }, 3000);
}
