<?php
session_start();
header('Content-Type: application/json');

require_once 'db_config.php';

// Check if user is logged in
function isLoggedIn() {
    if (!isset($_SESSION['admin_id']) || !isset($_SESSION['session_token'])) {
        return false;
    }
    
    global $pdo;
    
    // Verify session token in database
    $stmt = $pdo->prepare("SELECT user_id FROM admin_sessions WHERE session_token = ? AND expires_at > NOW()");
    $stmt->execute([$_SESSION['session_token']]);
    $session = $stmt->fetch();
    
    if (!$session || $session['user_id'] != $_SESSION['admin_id']) {
        return false;
    }
    
    return true;
}

// If not logged in, redirect to login
if (!isLoggedIn()) {
    if (isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest') {
        // AJAX request
        echo json_encode(['success' => false, 'message' => 'Not authenticated', 'redirect' => 'login.html']);
    } else {
        // Regular request
        header('Location: login.html');
    }
    exit;
}

// Return user info if authenticated
echo json_encode([
    'success' => true,
    'user' => [
        'id' => $_SESSION['admin_id'],
        'username' => $_SESSION['admin_username'],
        'role' => $_SESSION['admin_role']
    ]
]);
?>
