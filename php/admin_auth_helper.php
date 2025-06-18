<?php
// Admin authentication helper functions

function requireAdminAuth() {
    session_start();
    
    if (!isset($_SESSION['admin_id']) || !isset($_SESSION['session_token'])) {
        respondUnauthorized();
    }
    
    global $pdo;
    
    // Verify session token in database
    $stmt = $pdo->prepare("SELECT user_id FROM admin_sessions WHERE session_token = ? AND expires_at > NOW()");
    $stmt->execute([$_SESSION['session_token']]);
    $session = $stmt->fetch();
    
    if (!$session || $session['user_id'] != $_SESSION['admin_id']) {
        respondUnauthorized();
    }
    
    return $_SESSION['admin_id'];
}

function respondUnauthorized() {
    if (isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest') {
        // AJAX request
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Not authenticated', 'redirect' => 'login.html']);
    } else {
        // Regular request
        header('Location: ../admin/login.html');
    }
    exit;
}
?>
