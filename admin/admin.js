// Admin Panel JavaScript

// Global variables
let currentSection = 'dashboard';
let donationsData = [];
let membersData = [];

// Initialize admin panel
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication first
    checkAuthentication()
        .then(() => {
            loadTheme();
            showSection('dashboard');
            loadDashboardData();
            setupEventListeners();
        })
        .catch(() => {
            // Redirect to login if not authenticated
            window.location.href = 'login.html';
        });
});

// Setup event listeners
function setupEventListeners() {
    // About form
    const aboutForm = document.getElementById('aboutForm');
    if (aboutForm) {
        aboutForm.addEventListener('submit', saveAboutText);
    }
    
    // Settings form
    const settingsForm = document.getElementById('settingsForm');
    if (settingsForm) {
        settingsForm.addEventListener('submit', saveSettings);
    }
    
    // Photo upload form
    const photoUploadForm = document.getElementById('photoUploadForm');
    if (photoUploadForm) {
        photoUploadForm.addEventListener('submit', uploadPhoto);
    }
    
    // Certificate form
    const certificateForm = document.getElementById('certificateForm');
    if (certificateForm) {
        certificateForm.addEventListener('submit', generateCertificate);
    }
    
    // Password form
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', changePassword);
    }
    
    // Load initial data
    loadAboutText();
    loadSettings();
    loadPhotos();
    loadAdminInfo();
}

// Section management
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all menu items
    document.querySelectorAll('.admin-menu a').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(sectionName);
    if (section) {
        section.classList.add('active');
    }
    
    // Add active class to menu item
    const menuLink = document.querySelector(`.admin-menu a[href="#${sectionName}"]`);
    if (menuLink) {
        menuLink.classList.add('active');
    }
    
    currentSection = sectionName;
      // Load section-specific data
    switch (sectionName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'donations':
            loadDonations();
            break;
        case 'members':
            loadMembers();
            break;
        case 'certificates':
            loadCertificates();
            break;
        case 'settings':
            loadAdminInfo();
            break;
    }
}

// Dashboard functions
async function loadDashboardData() {
    try {
        // Load statistics
        const statsResponse = await fetch('../php/admin_stats.php');
        const stats = await statsResponse.json();
        
        if (stats.success) {
            document.getElementById('totalDonations').textContent = stats.data.totalDonations || '0';
            document.getElementById('totalAmount').textContent = '₹' + (stats.data.totalAmount || '0');
            document.getElementById('totalMembers').textContent = stats.data.totalMembers || '0';
            document.getElementById('thisMonth').textContent = '₹' + (stats.data.thisMonth || '0');
        }
        
        // Load recent donations
        const donationsResponse = await fetch('../php/admin_donations.php?limit=5');
        const donations = await donationsResponse.json();
        
        if (donations.success) {
            displayRecentDonations(donations.data);
        }
        
        // Load donations by cause
        const causesResponse = await fetch('../php/admin_stats.php?type=causes');
        const causes = await causesResponse.json();
        
        if (causes.success) {
            displayDonationsByCause(causes.data);
        }
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showMessage('Error loading dashboard data', 'error');
    }
}

function displayRecentDonations(donations) {
    const container = document.getElementById('recentDonations');
    if (!donations || donations.length === 0) {
        container.innerHTML = '<p>No recent donations found.</p>';
        return;
    }
    
    const table = `
        <table>
            <thead>
                <tr>
                    <th>Donor</th>
                    <th>Cause</th>
                    <th>Amount</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                ${donations.map(donation => `
                    <tr>
                        <td>${donation.donor_name}</td>
                        <td>${formatCause(donation.cause)}</td>
                        <td>₹${donation.amount}</td>
                        <td>${formatDate(donation.created_at)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = table;
}

function displayDonationsByCause(causes) {
    const container = document.getElementById('donationsByCause');
    if (!causes || causes.length === 0) {
        container.innerHTML = '<p>No donation data available.</p>';
        return;
    }
    
    const chart = causes.map(cause => `
        <div class="cause-stat">
            <div class="cause-name">${formatCause(cause.cause)}</div>
            <div class="cause-amount">₹${cause.total_amount}</div>
            <div class="cause-count">${cause.total_donations} donations</div>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="causes-stats">${chart}</div>`;
}

// Content management functions
async function loadAboutText() {
    try {
        // Add cache-busting parameter to force reload
        const timestamp = new Date().getTime();
        const response = await fetch(`../admin/about.txt?t=${timestamp}`);
        const text = await response.text();
        document.getElementById('aboutText').value = text;
    } catch (error) {
        console.error('Error loading about text:', error);
        showMessage('Error loading about text', 'error');
    }
}

async function saveAboutText(event) {
    event.preventDefault();
    
    const aboutText = document.getElementById('aboutText').value;
    
    try {
        const formData = new FormData();
        formData.append('aboutText', aboutText);
        
        const response = await fetch('../php/admin_save_about.php', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('About text saved successfully! Changes will appear on the website within 30 seconds.', 'success');
        } else {
            showMessage(result.message || 'Error saving about text', 'error');
        }
    } catch (error) {
        console.error('Error saving about text:', error);
        showMessage('Error saving about text', 'error');
    }
}

async function loadSettings() {
    try {
        const response = await fetch('../php/admin_settings.php');
        const result = await response.json();
        
        if (result.success) {
            const settings = result.data;
            document.getElementById('ownerName').value = settings.owner_name || '';
            document.getElementById('contactPhone').value = settings.contact_phone || '';
            document.getElementById('contactEmail').value = settings.contact_email || '';
            document.getElementById('contactAddress').value = settings.contact_address || '';
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

async function saveSettings(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    try {
        const response = await fetch('../php/admin_save_settings.php', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Settings saved successfully!', 'success');
        } else {
            showMessage(result.message || 'Error saving settings', 'error');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showMessage('Error saving settings', 'error');
    }
}

// Photos management functions
async function loadPhotos() {
    try {
        const response = await fetch('../php/admin_photos.php');
        const result = await response.json();
        
        if (result.success) {
            displayPhotos(result.data);
        }
    } catch (error) {
        console.error('Error loading photos:', error);
    }
}

function displayPhotos(photos) {
    const container = document.getElementById('photosGrid');
    
    if (!photos || photos.length === 0) {
        container.innerHTML = '<p>No photos uploaded yet.</p>';
        return;
    }
    
    const photosHTML = photos.map(photo => `
        <div class="photo-item">
            <img src="${photo.path}" alt="${photo.type}">
            <div class="photo-info">${photo.type}</div>
            <div class="photo-actions">
                <button onclick="deletePhoto('${photo.id}')" class="btn-delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = photosHTML;
}

async function uploadPhoto(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    try {
        const response = await fetch('../php/admin_upload_photo.php', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Photo uploaded successfully!', 'success');
            event.target.reset();
            loadPhotos();
        } else {
            showMessage(result.message || 'Error uploading photo', 'error');
        }
    } catch (error) {
        console.error('Error uploading photo:', error);
        showMessage('Error uploading photo', 'error');
    }
}

async function deletePhoto(photoId) {
    if (!confirm('Are you sure you want to delete this photo?')) {
        return;
    }
    
    try {
        const response = await fetch('../php/admin_delete_photo.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ photoId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Photo deleted successfully!', 'success');
            loadPhotos();
        } else {
            showMessage(result.message || 'Error deleting photo', 'error');
        }
    } catch (error) {
        console.error('Error deleting photo:', error);
        showMessage('Error deleting photo', 'error');
    }
}

// Donations management functions
async function loadDonations() {
    try {
        const response = await fetch('../php/admin_donations.php');
        const result = await response.json();
        
        if (result.success) {
            donationsData = result.data;
            displayDonationsTable(donationsData);
        }
    } catch (error) {
        console.error('Error loading donations:', error);
        showMessage('Error loading donations', 'error');
    }
}

function displayDonationsTable(donations) {
    const container = document.getElementById('donationsTable');
    
    if (!donations || donations.length === 0) {
        container.innerHTML = '<p>No donations found.</p>';
        return;
    }
    
    const table = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Donor Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Cause</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${donations.map(donation => `
                    <tr>
                        <td>${donation.id}</td>
                        <td>${donation.donor_name}</td>
                        <td>${donation.donor_email}</td>
                        <td>${donation.donor_phone}</td>
                        <td>${formatCause(donation.cause)}</td>
                        <td>₹${donation.amount}</td>
                        <td><span class="status-badge status-${donation.payment_status}">${donation.payment_status}</span></td>
                        <td>${formatDate(donation.created_at)}</td>
                        <td class="actions">
                            <button onclick="viewDonation(${donation.id})" class="btn-view">View</button>
                            <button onclick="updateDonationStatus(${donation.id})" class="btn-edit">Update</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = table;
}

function filterDonations() {
    const searchTerm = document.getElementById('donationSearch').value.toLowerCase();
    const causeFilter = document.getElementById('causeFilter').value;
    
    let filteredDonations = donationsData;
    
    if (searchTerm) {
        filteredDonations = filteredDonations.filter(donation =>
            donation.donor_name.toLowerCase().includes(searchTerm) ||
            donation.donor_email.toLowerCase().includes(searchTerm) ||
            donation.donor_phone.includes(searchTerm)
        );
    }
    
    if (causeFilter) {
        filteredDonations = filteredDonations.filter(donation =>
            donation.cause === causeFilter
        );
    }
    
    displayDonationsTable(filteredDonations);
}

function exportDonations() {
    if (!donationsData || donationsData.length === 0) {
        showMessage('No donations data to export', 'error');
        return;
    }
    
    const csvContent = [
        ['ID', 'Donor Name', 'Email', 'Phone', 'Cause', 'Amount', 'Status', 'Date'],
        ...donationsData.map(donation => [
            donation.id,
            donation.donor_name,
            donation.donor_email,
            donation.donor_phone,
            donation.cause,
            donation.amount,
            donation.payment_status,
            donation.created_at
        ])
    ].map(row => row.join(',')).join('\n');
    
    downloadCSV(csvContent, 'donations.csv');
}

// Members management functions
async function loadMembers() {
    try {
        const response = await fetch('../php/admin_members.php');
        const result = await response.json();
        
        if (result.success) {
            membersData = result.data;
            displayMembersTable(membersData);
        }
    } catch (error) {
        console.error('Error loading members:', error);
        showMessage('Error loading members', 'error');
    }
}

function displayMembersTable(members) {
    const container = document.getElementById('membersTable');
    
    if (!members || members.length === 0) {
        container.innerHTML = '<p>No members found.</p>';
        return;
    }
    
    const table = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Membership ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Status</th>
                    <th>Join Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${members.map(member => `
                    <tr>
                        <td>${member.id}</td>
                        <td>${member.membership_id}</td>
                        <td>${member.name}</td>
                        <td>${member.email}</td>
                        <td>${member.phone}</td>
                        <td><span class="status-badge status-${member.status}">${member.status}</span></td>
                        <td>${formatDate(member.created_at)}</td>
                        <td class="actions">
                            <button onclick="viewMember(${member.id})" class="btn-view">View</button>
                            <button onclick="toggleMemberStatus(${member.id})" class="btn-edit">Toggle Status</button>
                            <button onclick="downloadCertificate('${member.membership_id}')" class="btn-download">Certificate</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = table;
}

function filterMembers() {
    const searchTerm = document.getElementById('memberSearch').value.toLowerCase();
    
    let filteredMembers = membersData;
    
    if (searchTerm) {
        filteredMembers = filteredMembers.filter(member =>
            member.name.toLowerCase().includes(searchTerm) ||
            member.email.toLowerCase().includes(searchTerm) ||
            member.membership_id.toLowerCase().includes(searchTerm) ||
            member.phone.includes(searchTerm)
        );
    }
    
    displayMembersTable(filteredMembers);
}

function exportMembers() {
    if (!membersData || membersData.length === 0) {
        showMessage('No members data to export', 'error');
        return;
    }
    
    const csvContent = [
        ['ID', 'Membership ID', 'Name', 'Email', 'Phone', 'Status', 'Join Date'],
        ...membersData.map(member => [
            member.id,
            member.membership_id,
            member.name,
            member.email,
            member.phone,
            member.status,
            member.created_at
        ])
    ].map(row => row.join(',')).join('\n');
    
    downloadCSV(csvContent, 'members.csv');
}

// Certificate management functions
async function loadCertificates() {
    try {
        const response = await fetch('../php/admin_certificates.php');
        const result = await response.json();
        
        if (result.success) {
            displayCertificatesList(result.data);
        }
    } catch (error) {
        console.error('Error loading certificates:', error);
    }
}

function displayCertificatesList(certificates) {
    const container = document.getElementById('certificatesList');
    
    if (!certificates || certificates.length === 0) {
        container.innerHTML = '<p>No certificates generated yet.</p>';
        return;
    }
    
    const certificatesHTML = certificates.map(cert => `
        <div class="certificate-item">
            <div class="certificate-info">
                <h4>${cert.name}</h4>
                <p>Membership ID: ${cert.membership_id}</p>
                <p>Generated: ${formatDate(cert.created_at)}</p>
            </div>
            <div class="certificate-actions">
                <button onclick="downloadCertificate('${cert.membership_id}', 'light')" class="btn-download">
                    <i class="fas fa-download"></i> Light
                </button>
                <button onclick="downloadCertificate('${cert.membership_id}', 'dark')" class="btn-download">
                    <i class="fas fa-download"></i> Dark
                </button>
                <button onclick="emailCertificate('${cert.membership_id}')" class="btn-email">
                    <i class="fas fa-envelope"></i> Email
                </button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = certificatesHTML;
}

async function generateCertificate(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    try {
        const response = await fetch('../php/admin_generate_certificate.php', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Certificate generated successfully!', 'success');
            event.target.reset();
            loadCertificates();
        } else {
            showMessage(result.message || 'Error generating certificate', 'error');
        }
    } catch (error) {
        console.error('Error generating certificate:', error);
        showMessage('Error generating certificate', 'error');
    }
}

function downloadCertificate(membershipId, theme = 'light') {
    const filename = `certificate_${theme}_${membershipId}.png`;
    const link = document.createElement('a');
    link.href = `../certificates/${filename}`;
    link.download = filename;
    link.click();
}

async function emailCertificate(membershipId) {
    try {
        const response = await fetch('../php/admin_email_certificate.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ membershipId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Certificate emailed successfully!', 'success');
        } else {
            showMessage(result.message || 'Error emailing certificate', 'error');
        }
    } catch (error) {
        console.error('Error emailing certificate:', error);
        showMessage('Error emailing certificate', 'error');
    }
}

// Authentication functions
async function checkAuthentication() {
    try {
        const response = await fetch('../php/admin_auth.php');
        const data = await response.json();
        
        if (!data.success) {
            throw new Error('Not authenticated');
        }
        
        // Store user info
        sessionStorage.setItem('adminUser', JSON.stringify(data.user));
        return data.user;
    } catch (error) {
        console.error('Authentication check failed:', error);
        throw error;
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        fetch('../php/admin_logout.php')
            .then(() => {
                sessionStorage.clear();
                window.location.href = 'login.html';
            })
            .catch(error => {
                console.error('Logout error:', error);
                // Force redirect even if logout fails
                sessionStorage.clear();
                window.location.href = 'login.html';
            });
    }
}

// Password change functionality
async function changePassword(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Validate passwords match
    if (newPassword !== confirmPassword) {
        showNotification('New passwords do not match!', 'error');
        return;
    }
    
    // Validate password strength
    if (newPassword.length < 6) {
        showNotification('Password must be at least 6 characters long!', 'error');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('currentPassword', currentPassword);
        formData.append('newPassword', newPassword);
        
        const response = await fetch('../php/admin_change_password.php', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Password changed successfully!', 'success');
            document.getElementById('passwordForm').reset();
        } else {
            showNotification(data.message || 'Failed to change password', 'error');
        }
    } catch (error) {
        console.error('Error changing password:', error);
        showNotification('An error occurred while changing password', 'error');
    }
}

// Load admin info
async function loadAdminInfo() {
    try {
        const response = await fetch('../php/admin_auth.php');
        const data = await response.json();
        
        if (data.success) {
            const adminInfo = document.getElementById('adminInfo');
            if (adminInfo) {
                adminInfo.innerHTML = `
                    <p><strong>Username:</strong> <span>${data.user.username}</span></p>
                    <p><strong>Role:</strong> <span>${data.user.role}</span></p>
                    <p><strong>Login Status:</strong> <span class="status-active">Active</span></p>
                `;
            }
        }
    } catch (error) {
        console.error('Error loading admin info:', error);
    }
}

// Show notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Utility functions
function formatCause(cause) {
    const causes = {
        'orphanage': 'Orphanage',
        'gowshala': 'Gowshala',
        'vridha-ashram': 'Vridha Ashram',
        'health': 'Health Group',
        'samuhik-vivah': 'Samuhik Vivah',
        'pooja-rituals': 'Pooja Path & Rituals',
        'eye-camp': 'Eye Camp',
        'environment': 'Environmental Protection'
    };
    return causes[cause] || cause;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.admin-message');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message admin-message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at the top of the main content
    const main = document.querySelector('.admin-main');
    main.insertBefore(messageDiv, main.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Placeholder functions for features that can be implemented later
function viewDonation(donationId) {
    alert(`View donation details for ID: ${donationId}`);
}

function updateDonationStatus(donationId) {
    alert(`Update donation status for ID: ${donationId}`);
}

function viewMember(memberId) {
    alert(`View member details for ID: ${memberId}`);
}

function toggleMemberStatus(memberId) {
    alert(`Toggle member status for ID: ${memberId}`);
}
