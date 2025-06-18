<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

try {
    $search = $_GET['search'] ?? '';
    
    $sql = "SELECT * FROM members WHERE 1=1";
    $params = [];
    
    if ($search) {
        $sql .= " AND (name LIKE ? OR email LIKE ? OR membership_id LIKE ? OR phone LIKE ?)";
        $searchTerm = "%$search%";
        $params = [$searchTerm, $searchTerm, $searchTerm, $searchTerm];
    }
    
    $sql .= " ORDER BY created_at DESC";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $members = $stmt->fetchAll();
    
    echo json_encode(['success' => true, 'data' => $members]);
    
} catch (Exception $e) {
    error_log("Members error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error loading members']);
}
?>
