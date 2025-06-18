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
    $aboutText = $_POST['aboutText'] ?? '';
    
    if (empty($aboutText)) {
        echo json_encode(['success' => false, 'message' => 'About text cannot be empty']);
        exit;
    }
    
    $aboutFile = '../admin/about.txt';
    $result = file_put_contents($aboutFile, $aboutText);
    
    if ($result !== false) {
        echo json_encode(['success' => true, 'message' => 'About text saved successfully']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to save about text']);
    }
    
} catch (Exception $e) {
    error_log("Save about text error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error saving about text']);
}
?>
