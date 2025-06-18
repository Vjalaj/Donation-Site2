<?php
session_start();
header('Content-Type: application/json');

require_once 'db_config.php';

// Remove session from database
if (isset($_SESSION['session_token'])) {
    $stmt = $pdo->prepare("DELETE FROM admin_sessions WHERE session_token = ?");
    $stmt->execute([$_SESSION['session_token']]);
}

// Clear session
session_destroy();

// Clear cookie
setcookie('admin_session', '', time() - 3600, '/');

echo json_encode(['success' => true, 'message' => 'Logged out successfully']);
?>
