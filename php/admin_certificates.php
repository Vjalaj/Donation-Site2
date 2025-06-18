<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

try {
    $stmt = $pdo->query("SELECT * FROM members ORDER BY created_at DESC LIMIT 20");
    $certificates = $stmt->fetchAll();
    
    echo json_encode(['success' => true, 'data' => $certificates]);
    
} catch (Exception $e) {
    error_log("Certificates error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error loading certificates']);
}
?>
