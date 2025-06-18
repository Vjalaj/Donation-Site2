<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

try {
    // Get photos from the admin/photos directory
    $photosDir = '../admin/photos/';
    $photos = [];
    
    if (is_dir($photosDir)) {
        $files = scandir($photosDir);
        foreach ($files as $file) {
            if ($file != '.' && $file != '..' && $file != 'README.md') {
                $filePath = $photosDir . $file;
                if (is_file($filePath)) {
                    $photos[] = [
                        'id' => $file,
                        'name' => $file,
                        'path' => 'admin/photos/' . $file,
                        'type' => pathinfo($file, PATHINFO_FILENAME),
                        'size' => filesize($filePath)
                    ];
                }
            }
        }
    }
    
    echo json_encode(['success' => true, 'data' => $photos]);
    
} catch (Exception $e) {
    error_log("Photos error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error loading photos']);
}
?>
