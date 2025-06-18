<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    // Get form data
    $ownerName = $_POST['ownerName'] ?? '';
    $contactPhone = $_POST['contactPhone'] ?? '';
    $contactEmail = $_POST['contactEmail'] ?? '';
    $contactAddress = $_POST['contactAddress'] ?? '';
    
    // Validate required fields
    if (empty($ownerName) || empty($contactPhone) || empty($contactEmail) || empty($contactAddress)) {
        echo json_encode(['success' => false, 'message' => 'Please fill all required fields']);
        exit;
    }
    
    // Update settings in database
    $settings = [
        'owner_name' => $ownerName,
        'contact_phone' => $contactPhone,
        'contact_email' => $contactEmail,
        'contact_address' => $contactAddress
    ];
    
    foreach ($settings as $key => $value) {
        $stmt = $pdo->prepare("INSERT INTO admin_settings (setting_key, setting_value) VALUES (?, ?) ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value), updated_at = NOW()");
        $stmt->execute([$key, $value]);
    }
    
    echo json_encode(['success' => true, 'message' => 'Settings saved successfully']);
    
} catch (Exception $e) {
    error_log("Save settings error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error saving settings']);
}
?>
