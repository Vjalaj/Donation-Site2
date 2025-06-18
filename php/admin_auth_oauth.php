<?php
session_start();
header('Content-Type: application/json');

require_once 'db_config.php';

// Check if user is logged in via traditional auth or OAuth
function isLoggedIn() {
    // Check traditional session
    if (isset($_SESSION['admin_id']) && isset($_SESSION['session_token'])) {
        return verifyTraditionalSession();
    }
    
    // Check JWT token from OAuth
    if (isset($_GET['token']) || isset($_POST['token'])) {
        $token = $_GET['token'] ?? $_POST['token'];
        return verifyJWTToken($token);
    }
    
    // Check Authorization header
    $headers = getallheaders();
    if (isset($headers['Authorization'])) {
        $token = str_replace('Bearer ', '', $headers['Authorization']);
        return verifyJWTToken($token);
    }
    
    return false;
}

function verifyTraditionalSession() {
    global $pdo;
    
    $stmt = $pdo->prepare("SELECT user_id FROM admin_sessions WHERE session_token = ? AND expires_at > NOW()");
    $stmt->execute([$_SESSION['session_token']]);
    $session = $stmt->fetch();
    
    if (!$session || $session['user_id'] != $_SESSION['admin_id']) {
        return false;
    }
    
    return true;
}

function verifyJWTToken($token) {
    try {
        // Simple JWT verification (in production, use a proper JWT library)
        $parts = explode('.', $token);
        if (count($parts) !== 3) {
            return false;
        }
        
        $header = json_decode(base64_decode($parts[0]), true);
        $payload = json_decode(base64_decode($parts[1]), true);
        
        // Check expiration
        if (isset($payload['exp']) && $payload['exp'] < time()) {
            return false;
        }
        
        // Verify user exists
        if (isset($payload['user_id'])) {
            global $pdo;
            $stmt = $pdo->prepare("SELECT id, username, email, role FROM admin_users WHERE id = ? AND status = 'active'");
            $stmt->execute([$payload['user_id']]);
            $user = $stmt->fetch();
            
            if ($user) {
                // Set session variables for compatibility
                $_SESSION['admin_id'] = $user['id'];
                $_SESSION['admin_username'] = $user['username'];
                $_SESSION['admin_email'] = $user['email'];
                $_SESSION['admin_role'] = $user['role'];
                $_SESSION['auth_type'] = 'oauth';
                
                return true;
            }
        }
        
        return false;
    } catch (Exception $e) {
        error_log("JWT verification error: " . $e->getMessage());
        return false;
    }
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
        'username' => $_SESSION['admin_username'] ?? 'OAuth User',
        'email' => $_SESSION['admin_email'] ?? '',
        'role' => $_SESSION['admin_role'] ?? 'admin',
        'auth_type' => $_SESSION['auth_type'] ?? 'traditional'
    ]
]);
?>
