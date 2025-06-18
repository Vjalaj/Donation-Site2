<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

try {
    $limit = $_GET['limit'] ?? null;
    $search = $_GET['search'] ?? '';
    $cause = $_GET['cause'] ?? '';
    
    $sql = "SELECT * FROM donations WHERE 1=1";
    $params = [];
    
    if ($search) {
        $sql .= " AND (donor_name LIKE ? OR donor_email LIKE ? OR donor_phone LIKE ?)";
        $searchTerm = "%$search%";
        $params = array_merge($params, [$searchTerm, $searchTerm, $searchTerm]);
    }
    
    if ($cause) {
        $sql .= " AND cause = ?";
        $params[] = $cause;
    }
    
    $sql .= " ORDER BY created_at DESC";
    
    if ($limit) {
        $sql .= " LIMIT ?";
        $params[] = (int)$limit;
    }
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $donations = $stmt->fetchAll();
    
    echo json_encode(['success' => true, 'data' => $donations]);
    
} catch (Exception $e) {
    error_log("Donations error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error loading donations']);
}
?>
