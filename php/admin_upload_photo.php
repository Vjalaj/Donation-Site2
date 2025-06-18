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
    $photoType = $_POST['photoType'] ?? '';
    
    // Validate photo type
    $allowedTypes = ['logo', 'hero', 'gallery'];
    if (!in_array($photoType, $allowedTypes)) {
        echo json_encode(['success' => false, 'message' => 'Invalid photo type']);
        exit;
    }
    
    // Check if file was uploaded
    if (!isset($_FILES['photoFile']) || $_FILES['photoFile']['error'] !== UPLOAD_ERR_OK) {
        echo json_encode(['success' => false, 'message' => 'No file uploaded or upload error']);
        exit;
    }
    
    $file = $_FILES['photoFile'];
    
    // Validate file type
    $allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];
    $fileExtension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    
    if (!in_array($fileExtension, $allowedExtensions)) {
        echo json_encode(['success' => false, 'message' => 'Invalid file type. Only JPG, PNG, and GIF are allowed']);
        exit;
    }
    
    // Validate file size (max 5MB)
    if ($file['size'] > 5 * 1024 * 1024) {
        echo json_encode(['success' => false, 'message' => 'File size too large. Maximum 5MB allowed']);
        exit;
    }
    
    // Create upload directory if it doesn't exist
    $uploadDir = '../admin/photos/';
    if (!file_exists($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }
    
    // Generate filename
    $filename = $photoType . '.' . $fileExtension;
    $uploadPath = $uploadDir . $filename;
    
    // Move uploaded file
    if (move_uploaded_file($file['tmp_name'], $uploadPath)) {
        echo json_encode([
            'success' => true, 
            'message' => 'Photo uploaded successfully',
            'filename' => $filename,
            'path' => 'admin/photos/' . $filename
        ]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to upload photo']);
    }
    
} catch (Exception $e) {
    error_log("Upload photo error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error uploading photo']);
}
?>
