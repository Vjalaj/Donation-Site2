<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

try {
    $stmt = $pdo->query("SELECT setting_key, setting_value FROM admin_settings");
    $settings = [];
    
    while ($row = $stmt->fetch()) {
        $settings[$row['setting_key']] = $row['setting_value'];
    }
    
    echo json_encode(['success' => true, 'data' => $settings]);
    
} catch (Exception $e) {
    error_log("Settings error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error loading settings']);
}
?>
