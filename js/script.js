// Theme Management
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-toggle i');
    
    if (body.getAttribute('data-theme') === 'dark') {
        body.removeAttribute('data-theme');
        themeIcon.className = 'fas fa-moon';
        localStorage.setItem('theme', 'light');
    } else {
        body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-sun';
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const body = document.body;
    const themeIcon = document.querySelector('.theme-toggle i');
    
    if (savedTheme === 'dark') {
        body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-sun';
    }
}

// Mobile Navigation
function toggleMobileNav() {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');
    
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
}

// Smooth Scrolling
function scrollTo(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Donation Modal
function openDonationModal(cause) {
    const modal = document.getElementById('donationModal');
    const modalTitle = document.getElementById('modalTitle');
    const donationCause = document.getElementById('donationCause');
    
    const causeNames = {
        'orphanage': 'Orphanage Support',
        'gowshala': 'Gowshala Care',
        'vridha-ashram': 'Vridha Ashram Support',
        'health': 'Health Group Support',
        'samuhik-vivah': 'Samuhik Vivah',
        'pooja-rituals': 'Pooja Path & Rituals',
        'eye-camp': 'Eye Camp Organisation',
        'environment': 'Environmental Protection'
    };
    
    modalTitle.textContent = `Donate to ${causeNames[cause]}`;
    donationCause.value = cause;
    modal.style.display = 'block';
    
    // Close modal when clicking outside
    modal.onclick = function(event) {
        if (event.target === modal) {
            closeDonationModal();
        }
    }
}

function closeDonationModal() {
    const modal = document.getElementById('donationModal');
    modal.style.display = 'none';
}

// Load About Text
async function loadAboutText() {
    try {
        // Add cache-busting parameter to force reload
        const timestamp = new Date().getTime();
        const response = await fetch(`php/get_about.php?t=${timestamp}`);
        const text = await response.text();
        document.getElementById('about-text').innerHTML = text.replace(/\n/g, '<br>');
    } catch (error) {
        console.error('Error loading about text:', error);
        document.getElementById('about-text').innerHTML = `
            <p>Welcome to Seva Connect, a platform dedicated to serving humanity through compassionate giving and community service.</p>
            <p>Our mission is to bridge the gap between those who wish to help and those in need, creating a network of kindness and support that spans across various noble causes.</p>
            <p>Through your generous contributions, we support orphanages, gowshalas, elderly care centers, healthcare initiatives, community events, spiritual activities, eye care programs, and environmental protection efforts.</p>
            <p>Join us in making a positive impact on the world, one act of seva (service) at a time.</p>
        `;
    }
}

// Form Submissions
async function submitDonation(formData) {
    try {
        const response = await fetch('php/process_donation.php', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Thank you for your generous donation! You will receive a confirmation email shortly.', 'success');
            document.getElementById('donationForm').reset();
            closeDonationModal();
        } else {
            showMessage(result.message || 'An error occurred. Please try again.', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please check your connection and try again.', 'error');
    }
}

async function submitMembership(formData) {
    try {
        const response = await fetch('php/process_membership.php', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Welcome to Seva Connect! Your membership certificate will be emailed to you within 24 hours.', 'success');
            document.getElementById('membershipForm').reset();
        } else {
            showMessage(result.message || 'An error occurred. Please try again.', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please check your connection and try again.', 'error');
    }
}

// Show Messages
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert after the form
    const form = document.querySelector('form');
    if (form) {
        form.parentNode.insertBefore(messageDiv, form.nextSibling);
    }
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Certificate Generation
function generateCertificate(memberData, theme = 'light') {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 800;
    canvas.height = 600;
    
    // Background
    if (theme === 'dark') {
        ctx.fillStyle = '#1a1a1a';
    } else {
        ctx.fillStyle = '#ffffff';
    }
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Border
    ctx.strokeStyle = '#ff6b35';
    ctx.lineWidth = 8;
    ctx.strokeRect(20, 20, canvas.width - 40, canvas.height - 40);
    
    // Title
    ctx.fillStyle = theme === 'dark' ? '#ffffff' : '#333333';
    ctx.font = 'bold 36px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('CERTIFICATE OF MEMBERSHIP', canvas.width / 2, 120);
    
    // Seva Connect
    ctx.fillStyle = '#ff6b35';
    ctx.font = 'bold 28px Arial';
    ctx.fillText('SEVA CONNECT', canvas.width / 2, 170);
    
    // Member name
    ctx.fillStyle = theme === 'dark' ? '#ffffff' : '#333333';
    ctx.font = '24px Arial';
    ctx.fillText('This is to certify that', canvas.width / 2, 250);
    
    ctx.font = 'bold 32px Arial';
    ctx.fillStyle = '#ff6b35';
    ctx.fillText(memberData.name.toUpperCase(), canvas.width / 2, 300);
    
    ctx.fillStyle = theme === 'dark' ? '#ffffff' : '#333333';
    ctx.font = '20px Arial';
    ctx.fillText('is now a valued member of our community', canvas.width / 2, 340);
    ctx.fillText('dedicated to serving humanity through compassionate giving', canvas.width / 2, 370);
    
    // Date
    const currentDate = new Date().toLocaleDateString('en-IN');
    ctx.font = '16px Arial';
    ctx.fillText(`Date: ${currentDate}`, canvas.width / 2, 450);
    
    // Signature
    ctx.font = 'italic 18px Arial';
    ctx.fillText('Owner, Seva Connect', canvas.width / 2, 520);
    
    return canvas.toDataURL('image/png');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Load theme and about text
    loadTheme();
    loadAboutText();
    
    // Refresh about text every 30 seconds to catch admin updates
    setInterval(loadAboutText, 30000);
    
    // Mobile navigation
    const hamburger = document.querySelector('.hamburger');
    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileNav);
    }
    
    // Close mobile nav when clicking on links
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const navMenu = document.querySelector('.nav-menu');
            navMenu.classList.remove('active');
        });
    });
    
    // Donation form submission
    const donationForm = document.getElementById('donationForm');
    if (donationForm) {
        donationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            submitDonation(formData);
        });
    }
    
    // Membership form submission
    const membershipForm = document.getElementById('membershipForm');
    if (membershipForm) {
        membershipForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            submitMembership(formData);
        });
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cause cards
    document.querySelectorAll('.cause-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Escape key to close modal
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeDonationModal();
    }
});

// Prevent form submission on enter in text inputs
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && event.target.tagName === 'INPUT' && event.target.type === 'text') {
        event.preventDefault();
    }
});
