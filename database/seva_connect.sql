-- Seva Connect Database Schema
-- Run this SQL script in phpMyAdmin or MySQL command line

-- Create database
CREATE DATABASE IF NOT EXISTS seva_connect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE seva_connect;

-- Create donations table
CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cause VARCHAR(50) NOT NULL,
    donor_name VARCHAR(100) NOT NULL,
    donor_email VARCHAR(100) NOT NULL,
    donor_phone VARCHAR(15) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    message TEXT,
    transaction_id VARCHAR(100) DEFAULT NULL,
    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create members table
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    membership_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    message TEXT NOT NULL,
    membership_fee DECIMAL(10,2) DEFAULT 1111.00,
    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    status ENUM('active', 'inactive') DEFAULT 'active',
    certificate_light_path VARCHAR(255),
    certificate_dark_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create admin_users table for authentication
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role ENUM('admin', 'super_admin') DEFAULT 'admin',
    status ENUM('active', 'inactive') DEFAULT 'active',
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    oauth_provider VARCHAR(50) NULL,
    oauth_id VARCHAR(255) NULL
);

-- Insert default admin user (username: admin, password: admin123)
INSERT INTO admin_users (username, password_hash, email, role) VALUES 
('admin', '$2y$12$LVJGA6uUwvlAjrR/codNMOZjDzGs0PpaU01pu5T3PMU3zS1dFqoCy', 'admin@sevaconnect.org', 'super_admin');

-- Create sessions table for managing login sessions
CREATE TABLE IF NOT EXISTS admin_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE
);

-- Create admin_settings table for managing content
CREATE TABLE IF NOT EXISTS admin_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(50) UNIQUE NOT NULL,
    setting_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default admin settings
INSERT INTO admin_settings (setting_key, setting_value) VALUES
('site_title', 'Seva Connect'),
('site_description', 'A platform for compassionate giving and community service'),
('contact_phone', '+91 XXXXXXXXXX'),
('contact_email', 'info@sevaconnect.org'),
('contact_address', 'Your Address Here'),
('owner_name', 'Owner Name'),
('about_text', 'Welcome to Seva Connect, a platform dedicated to serving humanity through compassionate giving and community service. Our mission is to bridge the gap between those who wish to help and those in need, creating a network of kindness and support that spans across various noble causes.');

-- Create payment orders table for Razorpay
CREATE TABLE IF NOT EXISTS payment_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    razorpay_order_id VARCHAR(255) UNIQUE NOT NULL,
    razorpay_payment_id VARCHAR(255),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    payment_type ENUM('donation', 'membership') NOT NULL,
    status ENUM('created', 'verified', 'failed') DEFAULT 'created',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP NULL
);

-- Create payment refunds table
CREATE TABLE IF NOT EXISTS payment_refunds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    razorpay_refund_id VARCHAR(255) UNIQUE NOT NULL,
    razorpay_payment_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add payment columns to existing tables
ALTER TABLE donations ADD COLUMN razorpay_order_id VARCHAR(255) NULL;
ALTER TABLE donations ADD COLUMN razorpay_payment_id VARCHAR(255) NULL;
ALTER TABLE donations ADD COLUMN payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending';

ALTER TABLE members ADD COLUMN razorpay_order_id VARCHAR(255) NULL;
ALTER TABLE members ADD COLUMN razorpay_payment_id VARCHAR(255) NULL;
ALTER TABLE members ADD COLUMN payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending';

-- Create indexes for payment tables
CREATE INDEX idx_payment_orders_razorpay_order_id ON payment_orders(razorpay_order_id);
CREATE INDEX idx_payment_orders_status ON payment_orders(status);
CREATE INDEX idx_payment_refunds_payment_id ON payment_refunds(razorpay_payment_id);
CREATE INDEX idx_donations_payment_status ON donations(payment_status);
CREATE INDEX idx_members_payment_status ON members(payment_status);

-- Create indexes for better performance
CREATE INDEX idx_donations_cause ON donations(cause);
CREATE INDEX idx_donations_email ON donations(donor_email);
CREATE INDEX idx_donations_date ON donations(created_at);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_members_membership_id ON members(membership_id);
CREATE INDEX idx_members_status ON members(status);

-- Create a view for donation statistics
CREATE VIEW donation_stats AS
SELECT 
    cause,
    COUNT(*) as total_donations,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MAX(amount) as max_amount,
    MIN(amount) as min_amount
FROM donations 
WHERE payment_status = 'completed'
GROUP BY cause;

-- Create a view for monthly donation summary
CREATE VIEW monthly_donations AS
SELECT 
    YEAR(created_at) as year,
    MONTH(created_at) as month,
    MONTHNAME(created_at) as month_name,
    COUNT(*) as total_donations,
    SUM(amount) as total_amount
FROM donations 
WHERE payment_status = 'completed'
GROUP BY YEAR(created_at), MONTH(created_at)
ORDER BY year DESC, month DESC;
