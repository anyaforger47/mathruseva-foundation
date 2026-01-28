// Mathruseva Foundation - Frontend JavaScript

// Global variables
let currentSection = 'dashboard';
let charts = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    loadVolunteers();
    loadCamps();
    loadDonations();
    initializeEventListeners();
});

// Navigation and section management
function showSection(sectionId) {
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
        case 'camps':
            loadCamps();
            break;
        case 'donations':
            loadDonations();
            break;
    }
}

// Initialize event listeners
function initializeEventListeners() {
    // Volunteer form submission
    document.getElementById('volunteerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addVolunteer();
    });
    
    // Camp form submission
    document.getElementById('campForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addCamp();
    });
    
    // Donation form submission
    document.getElementById('donationForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addDonation();
    });
    
    // Search functionality
    document.getElementById('volunteerSearch').addEventListener('input', function(e) {
        filterVolunteers(e.target.value);
    });
    
    // Filter functionality
    document.getElementById('campTypeFilter').addEventListener('change', function(e) {
        filterCamps(e.target.value);
    });
    
    document.getElementById('donationTypeFilter').addEventListener('change', function(e) {
        filterDonations(e.target.value);
    });
}

// Dashboard functions
async function loadDashboard() {
    try {
        const response = await fetch('/api/analytics/dashboard');
        const data = await response.json();
        
        // Update stats cards
        document.getElementById('totalVolunteers').textContent = data.total_volunteers;
        document.getElementById('totalCamps').textContent = data.total_camps;
        document.getElementById('totalBeneficiaries').textContent = data.total_beneficiaries;
        document.getElementById('totalDonations').textContent = data.total_donations;
        
        // Update charts
        updateCampTypeChart(data.camp_types);
        updateMonthlyTrendsChart(data.monthly_trends);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    }
}

function updateCampTypeChart(campTypes) {
    const ctx = document.getElementById('campTypeChart').getContext('2d');
    
    if (charts.campType) {
        charts.campType.destroy();
    }
    
    charts.campType = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: campTypes.map(type => type.type),
            datasets: [{
                data: campTypes.map(type => type.count),
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateMonthlyTrendsChart(monthlyTrends) {
    const ctx = document.getElementById('monthlyTrendsChart').getContext('2d');
    
    if (charts.monthlyTrends) {
        charts.monthlyTrends.destroy();
    }
    
    charts.monthlyTrends = new Chart(ctx, {
        type: 'line',
        data: {
            labels: monthlyTrends.map(trend => trend.month),
            datasets: [{
                label: 'Number of Camps',
                data: monthlyTrends.map(trend => trend.camps),
                borderColor: '#36A2EB',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Volunteer functions
async function loadVolunteers() {
    try {
        const response = await fetch('/api/volunteers');
        const volunteers = await response.json();
        displayVolunteers(volunteers);
    } catch (error) {
        console.error('Error loading volunteers:', error);
        showAlert('Error loading volunteers', 'danger');
    }
}

function displayVolunteers(volunteers) {
    const tbody = document.getElementById('volunteersTableBody');
    tbody.innerHTML = '';
    
    volunteers.forEach(volunteer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${volunteer.name}</td>
            <td>${volunteer.email}</td>
            <td>${volunteer.phone || 'N/A'}</td>
            <td><span class="badge bg-primary">${volunteer.role}</span></td>
            <td><span class="badge bg-${volunteer.status === 'Active' ? 'success' : 'secondary'}">${volunteer.status}</span></td>
            <td>${formatDate(volunteer.join_date)}</td>
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
}

async function addVolunteer() {
    const formData = {
        name: document.getElementById('volunteerName').value,
        email: document.getElementById('volunteerEmail').value,
        phone: document.getElementById('volunteerPhone').value,
        role: document.getElementById('volunteerRole').value
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
            bootstrap.Modal.getInstance(document.getElementById('volunteerModal')).hide();
            document.getElementById('volunteerForm').reset();
            resetVolunteerModal();
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
        const response = await fetch('/api/camps');
        const camps = await response.json();
        displayCamps(camps);
        populateCampDropdown(camps);
    } catch (error) {
        console.error('Error loading camps:', error);
        showAlert('Error loading camps', 'danger');
    }
}

function displayCamps(camps) {
    const tbody = document.getElementById('campsTableBody');
    tbody.innerHTML = '';
    
    camps.forEach(camp => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${camp.name}</td>
            <td><span class="badge bg-info">${camp.type}</span></td>
            <td>${camp.location}</td>
            <td>${formatDate(camp.camp_date)}</td>
            <td><span class="badge bg-${getStatusColor(camp.status)}">${camp.status}</span></td>
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
}

function populateCampDropdown(camps) {
    const select = document.getElementById('donationCamp');
    select.innerHTML = '<option value="">Select Camp</option>';
    
    camps.forEach(camp => {
        const option = document.createElement('option');
        option.value = camp.id;
        option.textContent = `${camp.name} - ${camp.location}`;
        select.appendChild(option);
    });
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
            bootstrap.Modal.getInstance(document.getElementById('campModal')).hide();
            document.getElementById('campForm').reset();
            resetCampModal();
            loadCamps();
        } else {
            throw new Error('Failed to add camp');
        }
    } catch (error) {
        console.error('Error adding camp:', error);
        showAlert('Error adding camp', 'danger');
    }
}

function resetCampModal() {
    document.getElementById('campForm').reset();
    document.querySelector('#campModal .modal-title').textContent = 'Add Camp';
    document.querySelector('#campModal .btn-primary').textContent = 'Add Camp';
    document.querySelector('#campModal .btn-primary').onclick = addCamp;
}

// Donation functions
async function loadDonations() {
    try {
        const response = await fetch('/api/donations');
        const donations = await response.json();
        displayDonations(donations);
    } catch (error) {
        console.error('Error loading donations:', error);
        showAlert('Error loading donations', 'danger');
    }
}

function displayDonations(donations) {
    const tbody = document.getElementById('donationsTableBody');
    tbody.innerHTML = '';
    
    donations.forEach(donation => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${donation.camp_name || 'General'}</td>
            <td><span class="badge bg-warning">${donation.donation_type}</span></td>
            <td>${donation.quantity}</td>
            <td>${donation.donor_name || 'Anonymous'}</td>
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
            bootstrap.Modal.getInstance(document.getElementById('donationModal')).hide();
            document.getElementById('donationForm').reset();
            resetDonationModal();
            loadDonations();
        } else {
            throw new Error('Failed to add donation');
        }
    } catch (error) {
        console.error('Error adding donation:', error);
        showAlert('Error adding donation', 'danger');
    }
}

function resetDonationModal() {
    document.getElementById('donationForm').reset();
    document.querySelector('#donationModal .modal-title').textContent = 'Add Donation';
    document.querySelector('#donationModal .btn-primary').textContent = 'Add Donation';
    document.querySelector('#donationModal .btn-primary').onclick = addDonation;
}

function editDonation(id) {
    console.log('Edit donation called with ID:', id);
    
    // Fetch donation data and populate modal
    fetch('/api/donations')
        .then(response => response.json())
        .then(donations => {
            console.log('Donations received:', donations);
            const donation = donations.find(d => d.id === id);
            console.log('Found donation:', donation);
            
            if (donation) {
                document.getElementById('donationCamp').value = donation.camp_id || '';
                document.getElementById('donationType').value = donation.donation_type;
                document.getElementById('donationQuantity').value = donation.quantity;
                document.getElementById('donorName').value = donation.donor_name || '';
                document.getElementById('donationDate').value = donation.donation_date;
                document.getElementById('donationNotes').value = donation.notes || '';
                
                console.log('Modal populated with donation data');
                
                // Change modal title and button
                document.querySelector('#donationModal .modal-title').textContent = 'Edit Donation';
                document.querySelector('#donationModal .btn-primary').textContent = 'Update Donation';
                document.querySelector('#donationModal .btn-primary').onclick = () => updateDonation(id);
                
                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('donationModal'));
                modal.show();
                console.log('Modal should be visible now');
            } else {
                console.error('Donation not found with ID:', id);
                showAlert('Donation not found', 'danger');
            }
        })
        .catch(error => {
            console.error('Error fetching donation:', error);
            showAlert('Error fetching donation data', 'danger');
        });
}

async function updateDonation(id) {
    // Get form values
    const camp_id = document.getElementById('donationCamp').value;
    const donation_type = document.getElementById('donationType').value;
    const quantity = document.getElementById('donationQuantity').value;
    const donor_name = document.getElementById('donorName').value;
    const donation_date = document.getElementById('donationDate').value;
    const notes = document.getElementById('donationNotes').value;
    
    // Validate required fields
    if (!donation_type || !quantity || !donation_date) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }
    
    const formData = {
        camp_id: camp_id || null,
        donation_type: donation_type.trim(),
        quantity: parseInt(quantity),
        donor_name: donor_name.trim(),
        donation_date: donation_date,
        notes: notes.trim()
    };
    
    console.log('Updating donation with data:', formData);
    
    try {
        const response = await fetch(`/api/donations/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        console.log('Response status:', response.status);
        
        if (response.ok) {
            showAlert('Donation updated successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('donationModal')).hide();
            resetDonationModal();
            loadDonations();
        } else {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            showAlert('Failed to update donation: ' + errorText, 'danger');
        }
    } catch (error) {
        console.error('Error updating donation:', error);
        showAlert('Error updating donation: ' + error.message, 'danger');
    }
}

async function deleteDonation(id) {
    console.log('Delete donation called with ID:', id);
    
    if (confirm('Are you sure you want to delete this donation?')) {
        console.log('User confirmed deletion');
        
        try {
            const response = await fetch(`/api/donations/${id}`, {
                method: 'DELETE'
            });
            
            console.log('Delete response status:', response.status);
            
            if (response.ok) {
                showAlert('Donation deleted successfully', 'success');
                loadDonations();
            } else {
                const errorText = await response.text();
                console.error('Delete error response:', errorText);
                showAlert('Failed to delete donation: ' + errorText, 'danger');
            }
        } catch (error) {
            console.error('Error deleting donation:', error);
            showAlert('Error deleting donation: ' + error.message, 'danger');
        }
    } else {
        console.log('User cancelled deletion');
    }
}

// Utility functions
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function getStatusColor(status) {
    switch(status) {
        case 'Completed': return 'success';
        case 'Ongoing': return 'warning';
        case 'Planned': return 'info';
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
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Filter functions
function filterVolunteers(searchTerm) {
    const rows = document.querySelectorAll('#volunteersTableBody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm.toLowerCase()) ? '' : 'none';
    });
}

function filterCamps(type) {
    const rows = document.querySelectorAll('#campsTableBody tr');
    rows.forEach(row => {
        if (!type) {
            row.style.display = '';
        } else {
            const campType = row.querySelector('td:nth-child(2)').textContent.trim();
            row.style.display = campType.includes(type) ? '' : 'none';
        }
    });
}

function filterDonations(type) {
    const rows = document.querySelectorAll('#donationsTableBody tr');
    rows.forEach(row => {
        if (!type) {
            row.style.display = '';
        } else {
            const donationType = row.querySelector('td:nth-child(2)').textContent.trim();
            row.style.display = donationType.includes(type) ? '' : 'none';
        }
    });
}

// Report generation
async function generatePDFReport() {
    try {
        showAlert('Generating PDF report...', 'info');
        
        const response = await fetch('/api/reports/generate-pdf');
        
        if (response.ok) {
            // Create a download link for the PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `impact_report_${new Date().toISOString().split('T')[0]}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showAlert('PDF report downloaded successfully!', 'success');
        } else {
            const errorData = await response.json();
            showAlert('Failed to generate PDF report: ' + errorData.error, 'danger');
        }
    } catch (error) {
        console.error('Error generating PDF report:', error);
        showAlert('Error generating PDF report: ' + error.message, 'danger');
    }
}

function showAnalytics() {
    showSection('dashboard');
}

// Placeholder functions for edit/delete operations
async function editVolunteer(id) {
    try {
        // Fetch volunteer data
        const response = await fetch(`/api/volunteers`);
        const volunteers = await response.json();
        const volunteer = volunteers.find(v => v.id === id);
        
        if (volunteer) {
            // Populate the modal with volunteer data
            document.getElementById('volunteerName').value = volunteer.name;
            document.getElementById('volunteerEmail').value = volunteer.email;
            document.getElementById('volunteerPhone').value = volunteer.phone || '';
            document.getElementById('volunteerRole').value = volunteer.role;
            
            // Change modal title and button
            document.querySelector('#volunteerModal .modal-title').textContent = 'Edit Volunteer';
            document.querySelector('#volunteerModal .btn-primary').textContent = 'Update Volunteer';
            document.querySelector('#volunteerModal .btn-primary').onclick = () => updateVolunteer(id);
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('volunteerModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error fetching volunteer:', error);
        showAlert('Error fetching volunteer data', 'danger');
    }
}

async function updateVolunteer(id) {
    const formData = {
        name: document.getElementById('volunteerName').value,
        email: document.getElementById('volunteerEmail').value,
        phone: document.getElementById('volunteerPhone').value,
        role: document.getElementById('volunteerRole').value,
        status: 'Active' // Default status
    };
    
    try {
        const response = await fetch(`/api/volunteers/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Volunteer updated successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('volunteerModal')).hide();
            resetVolunteerModal();
            loadVolunteers();
        } else {
            throw new Error('Failed to update volunteer');
        }
    } catch (error) {
        console.error('Error updating volunteer:', error);
        showAlert('Error updating volunteer', 'danger');
    }
}

function resetVolunteerModal() {
    document.getElementById('volunteerForm').reset();
    document.querySelector('#volunteerModal .modal-title').textContent = 'Add Volunteer';
    document.querySelector('#volunteerModal .btn-primary').textContent = 'Add Volunteer';
    document.querySelector('#volunteerModal .btn-primary').onclick = addVolunteer;
}

async function deleteVolunteer(id) {
    if (confirm('Are you sure you want to delete this volunteer?')) {
        try {
            const response = await fetch(`/api/volunteers/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Volunteer deleted successfully', 'success');
                loadVolunteers();
            } else {
                throw new Error('Failed to delete volunteer');
            }
        } catch (error) {
            console.error('Error deleting volunteer:', error);
            showAlert('Error deleting volunteer', 'danger');
        }
    }
}

function editCamp(id) {
    // Fetch camp data and populate modal
    fetch('/api/camps')
        .then(response => response.json())
        .then(camps => {
            const camp = camps.find(c => c.id === id);
            if (camp) {
                document.getElementById('campName').value = camp.name;
                document.getElementById('campType').value = camp.type;
                document.getElementById('campLocation').value = camp.location;
                document.getElementById('campDate').value = camp.camp_date;
                document.getElementById('campDescription').value = camp.description || '';
                
                // Change modal title and button
                document.querySelector('#campModal .modal-title').textContent = 'Edit Camp';
                document.querySelector('#campModal .btn-primary').textContent = 'Update Camp';
                document.querySelector('#campModal .btn-primary').onclick = () => updateCamp(id);
                
                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('campModal'));
                modal.show();
            }
        })
        .catch(error => {
            console.error('Error fetching camp:', error);
            showAlert('Error fetching camp data', 'danger');
        });
}

async function updateCamp(id) {
    // Get form values
    const name = document.getElementById('campName').value;
    const type = document.getElementById('campType').value;
    const location = document.getElementById('campLocation').value;
    const camp_date = document.getElementById('campDate').value;
    const description = document.getElementById('campDescription').value;
    
    // Validate required fields
    if (!name || !type || !location || !camp_date) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }
    
    const formData = {
        name: name.trim(),
        type: type.trim(),
        location: location.trim(),
        camp_date: camp_date,
        description: description.trim(),
        status: 'Planned'
    };
    
    console.log('Updating camp with data:', formData);
    
    try {
        const response = await fetch(`/api/camps/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        console.log('Response status:', response.status);
        
        if (response.ok) {
            showAlert('Camp updated successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('campModal')).hide();
            resetCampModal();
            loadCamps();
        } else {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            showAlert('Failed to update camp: ' + errorText, 'danger');
        }
    } catch (error) {
        console.error('Error updating camp:', error);
        showAlert('Error updating camp: ' + error.message, 'danger');
    }
}

async function deleteCamp(id) {
    if (confirm('Are you sure you want to delete this camp?')) {
        try {
            const response = await fetch(`/api/camps/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Camp deleted successfully', 'success');
                loadCamps();
            } else {
                throw new Error('Failed to delete camp');
            }
        } catch (error) {
            console.error('Error deleting camp:', error);
            showAlert('Error deleting camp', 'danger');
        }
    }
}

// Media Management Functions
async function loadMedia() {
    try {
        const response = await fetch('/api/media/all');
        const data = await response.json();
        
        if (response.ok) {
            displayMedia(data.media);
        } else {
            console.error('Failed to load media:', data.error);
        }
    } catch (error) {
        console.error('Error loading media:', error);
    }
}

function displayMedia(mediaItems) {
    const gallery = document.getElementById('mediaGallery');
    const filter = document.getElementById('mediaFilter').value;
    
    // Filter media based on selected filter
    const filteredMedia = filter ? mediaItems.filter(item => item.media_type === filter) : mediaItems;
    
    gallery.innerHTML = '';
    
    if (filteredMedia.length === 0) {
        gallery.innerHTML = '<div class="col-12"><p class="text-muted">No media found.</p></div>';
        return;
    }
    
    filteredMedia.forEach(media => {
        const mediaCol = document.createElement('div');
        mediaCol.className = 'col-md-4 mb-4';
        
        if (media.media_type === 'photo') {
            mediaCol.innerHTML = `
                <div class="card">
                    <img src="${media.media_url}" class="card-img-top" alt="${media.caption || 'Camp photo'}" 
                         style="height: 200px; object-fit: cover;" onerror="this.src='https://via.placeholder.com/400x200?text=Image+Not+Found'">
                    <div class="card-body">
                        <h6 class="card-title">${media.camp_name}</h6>
                        <p class="card-text small text-muted">${media.camp_location}</p>
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
                        <h6 class="card-title">${media.camp_name}</h6>
                        <p class="card-text small text-muted">${media.camp_location}</p>
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
}

async function uploadMedia() {
    const formData = {
        camp_id: document.getElementById('mediaCamp').value,
        media_type: document.getElementById('mediaType').value,
        media_url: document.getElementById('mediaUrl').value,
        caption: document.getElementById('mediaCaption').value
    };
    
    try {
        const response = await fetch('/api/media/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Media uploaded successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('mediaUploadModal')).hide();
            document.getElementById('mediaUploadForm').reset();
            loadMedia(); // Reload media gallery
        } else {
            const errorData = await response.json();
            showAlert('Failed to upload media: ' + errorData.error, 'danger');
        }
    } catch (error) {
        console.error('Error uploading media:', error);
        showAlert('Error uploading media: ' + error.message, 'danger');
    }
}

async function deleteMedia(mediaId) {
    if (confirm('Are you sure you want to delete this media?')) {
        try {
            const response = await fetch(`/api/media/${mediaId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Media deleted successfully', 'success');
                loadMedia(); // Reload media gallery
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
        select.innerHTML = '<option value="">Select Camp</option>';
        
        camps.forEach(camp => {
            const option = document.createElement('option');
            option.value = camp.id;
            option.textContent = `${camp.name} - ${camp.location}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading camps for media:', error);
    }
}

// Filter media
document.getElementById('mediaFilter').addEventListener('change', loadMedia);

