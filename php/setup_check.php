<?php
// Database Setup Check and Auto-Fix
header('Content-Type: application/json');

// Include database config
require_once 'db_config.php';

$response = [
    'database_connected' => false,
    'tables_exist' => false,
    'admin_user_exists' => false,
    'setup_required' => false,
    'errors' => [],
    'actions_taken' => []
];

try {
    // Test database connection
    $pdo->query("SELECT 1");
    $response['database_connected'] = true;
    
    // Check if required tables exist
    $required_tables = ['admin_users', 'admin_sessions', 'donations', 'members'];
    $existing_tables = [];
    
    $stmt = $pdo->query("SHOW TABLES");
    $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);
    
    foreach ($required_tables as $table) {
        if (in_array($table, $tables)) {
            $existing_tables[] = $table;
        }
    }
    
    if (count($existing_tables) === count($required_tables)) {
        $response['tables_exist'] = true;
        
        // Check if admin user exists
        $stmt = $pdo->query("SELECT COUNT(*) FROM admin_users");
        $admin_count = $stmt->fetchColumn();
        
        if ($admin_count > 0) {
            $response['admin_user_exists'] = true;
        } else {
            $response['setup_required'] = true;
            $response['errors'][] = 'No admin users found in database';
        }
    } else {
        $response['setup_required'] = true;
        $missing_tables = array_diff($required_tables, $existing_tables);
        $response['errors'][] = 'Missing tables: ' . implode(', ', $missing_tables);
    }
    
} catch (PDOException $e) {
    $response['errors'][] = 'Database error: ' . $e->getMessage();
    
    if (strpos($e->getMessage(), 'Unknown database') !== false) {
        $response['errors'][] = 'Database "seva_connect" does not exist. Please create it first.';
    }
}

// If setup is required, provide instructions
if ($response['setup_required']) {
    $response['setup_instructions'] = [
        '1. Ensure XAMPP is running (Apache + MySQL)',
        '2. Open phpMyAdmin (http://localhost/phpmyadmin)',
        '3. Create database "seva_connect" if it doesn\'t exist',
        '4. Import the SQL file: database/seva_connect.sql',
        '5. Refresh this page to check again'
    ];
}

echo json_encode($response, JSON_PRETTY_PRINT);
?>
