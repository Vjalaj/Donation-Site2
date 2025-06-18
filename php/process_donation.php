<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Database connection
require_once 'db_config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    // Get form data
    $cause = $_POST['cause'] ?? '';
    $donorName = $_POST['donorName'] ?? '';
    $donorEmail = $_POST['donorEmail'] ?? '';
    $donorPhone = $_POST['donorPhone'] ?? '';
    $donationAmount = $_POST['donationAmount'] ?? 0;
    $donationMessage = $_POST['donationMessage'] ?? '';
    
    // Validate required fields
    if (empty($cause) || empty($donorName) || empty($donorEmail) || empty($donorPhone) || $donationAmount <= 0) {
        echo json_encode(['success' => false, 'message' => 'Please fill all required fields']);
        exit;
    }
    
    // Validate email
    if (!filter_var($donorEmail, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['success' => false, 'message' => 'Please enter a valid email address']);
        exit;
    }
    
    // Validate phone number (Indian format)
    if (!preg_match('/^[6-9]\d{9}$/', $donorPhone)) {
        echo json_encode(['success' => false, 'message' => 'Please enter a valid 10-digit phone number']);
        exit;
    }
    
    // Insert donation into database
    $stmt = $pdo->prepare("INSERT INTO donations (cause, donor_name, donor_email, donor_phone, amount, message, created_at) VALUES (?, ?, ?, ?, ?, ?, NOW())");
    $result = $stmt->execute([$cause, $donorName, $donorEmail, $donorPhone, $donationAmount, $donationMessage]);
    
    if ($result) {
        $donationId = $pdo->lastInsertId();
        
        // Send confirmation email (optional - you can implement this later)
        // sendDonationConfirmationEmail($donorEmail, $donorName, $cause, $donationAmount, $donationId);
        
        echo json_encode([
            'success' => true, 
            'message' => 'Donation submitted successfully',
            'donation_id' => $donationId
        ]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to process donation']);
    }
    
} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Database error occurred']);
} catch (Exception $e) {
    error_log("General error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'An error occurred while processing your request']);
}

function sendDonationConfirmationEmail($email, $name, $cause, $amount, $donationId) {
    // Email configuration - you can implement this using PHPMailer or similar
    $subject = "Thank you for your donation - Seva Connect";
    $message = "
    Dear $name,
    
    Thank you for your generous donation of ₹$amount towards $cause.
    
    Donation ID: $donationId
    Date: " . date('Y-m-d H:i:s') . "
    
    Your contribution will make a real difference in the lives of those we serve.
    
    With gratitude,
    Seva Connect Team
    ";
    
    // Uncomment and configure when ready to send emails
    // mail($email, $subject, $message);
}
?>
