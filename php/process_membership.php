<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Database connection
require_once 'db_config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {    // Get form data
    $memberName = $_POST['memberName'] ?? '';
    $memberEmail = $_POST['memberEmail'] ?? '';
    $memberPhone = $_POST['memberPhone'] ?? '';
    $memberMessage = $_POST['memberMessage'] ?? '';
    $membershipFee = 1111; // Fixed membership fee
    
    // Validate required fields
    if (empty($memberName) || empty($memberEmail) || empty($memberMessage)) {
        echo json_encode(['success' => false, 'message' => 'Please fill all required fields']);
        exit;
    }
    
    // Validate email
    if (!filter_var($memberEmail, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['success' => false, 'message' => 'Please enter a valid email address']);
        exit;
    }
      // Validate phone number (Indian format) - optional
    if (!empty($memberPhone) && !preg_match('/^[6-9]\d{9}$/', $memberPhone)) {
        echo json_encode(['success' => false, 'message' => 'Please enter a valid 10-digit phone number']);
        exit;
    }
    
    // Check if email already exists
    $checkStmt = $pdo->prepare("SELECT id FROM members WHERE email = ?");
    $checkStmt->execute([$memberEmail]);
    if ($checkStmt->fetch()) {
        echo json_encode(['success' => false, 'message' => 'This email is already registered']);
        exit;
    }
    
    // Generate membership ID
    $membershipId = 'SC' . date('Y') . str_pad(rand(1, 9999), 4, '0', STR_PAD_LEFT);
      // Insert member into database
    $stmt = $pdo->prepare("INSERT INTO members (membership_id, name, email, phone, message, membership_fee, created_at) VALUES (?, ?, ?, ?, ?, ?, NOW())");
    $result = $stmt->execute([$membershipId, $memberName, $memberEmail, $memberPhone, $memberMessage, $membershipFee]);
    
    if ($result) {
        $memberId = $pdo->lastInsertId();
        
        // Generate certificates for both themes
        generateCertificates($memberName, $membershipId, $memberEmail);
        
        // Send membership confirmation email (optional - you can implement this later)
        // sendMembershipConfirmationEmail($memberEmail, $memberName, $membershipId);
        
        echo json_encode([
            'success' => true, 
            'message' => 'Membership created successfully',
            'membership_id' => $membershipId
        ]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to create membership']);
    }
    
} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Database error occurred']);
} catch (Exception $e) {
    error_log("General error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'An error occurred while processing your request']);
}

function generateCertificates($memberName, $membershipId, $email) {
    // Create certificates directory if it doesn't exist
    $certificatesDir = '../certificates/';
    if (!file_exists($certificatesDir)) {
        mkdir($certificatesDir, 0755, true);
    }
    
    // Certificate dimensions
    $width = 800;
    $height = 600;
    
    // Generate light theme certificate (matches the uploaded design)
    $lightCert = imagecreatetruecolor($width, $height);
    
    // Colors for light theme (matching the uploaded certificate)
    $darkBlue = imagecolorallocate($lightCert, 58, 74, 105); // Background color
    $lightBlue = imagecolorallocate($lightCert, 100, 149, 237); // "Certificate of Appreciation" text
    $orange = imagecolorallocate($lightCert, 255, 165, 0); // Border and accents
    $white = imagecolorallocate($lightCert, 255, 255, 255);
    $lightGray = imagecolorallocate($lightCert, 200, 200, 200);
    
    // Fill background
    imagefill($lightCert, 0, 0, $darkBlue);
    
    // Draw decorative border
    imagesetthickness($lightCert, 8);
    imagerectangle($lightCert, 20, 20, $width-20, $height-20, $orange);
    imagesetthickness($lightCert, 3);
    imagerectangle($lightCert, 15, 15, $width-15, $height-15, $orange);
    
    // Add corner decorations
    imagesetthickness($lightCert, 4);
    // Top-left corner
    imageline($lightCert, 40, 40, 100, 40, $orange);
    imageline($lightCert, 40, 40, 40, 100, $orange);
    // Top-right corner
    imageline($lightCert, $width-100, 40, $width-40, 40, $orange);
    imageline($lightCert, $width-40, 40, $width-40, 100, $orange);
    // Bottom-left corner
    imageline($lightCert, 40, $height-40, 100, $height-40, $orange);
    imageline($lightCert, 40, $height-100, 40, $height-40, $orange);
    // Bottom-right corner
    imageline($lightCert, $width-100, $height-40, $width-40, $height-40, $orange);
    imageline($lightCert, $width-40, $height-100, $width-40, $height-40, $orange);
    
    // Add medal/ribbon icon at top center
    $iconX = $width / 2;
    $iconY = 80;
    imagefilledellipse($lightCert, $iconX, $iconY, 40, 40, $orange);
    imagefilledellipse($lightCert, $iconX, $iconY, 25, 25, $darkBlue);
    
    // Add text (using built-in fonts)
    // "Certificate of Appreciation"
    $titleText = "Certificate of Appreciation";
    imagestring($lightCert, 5, ($width - strlen($titleText) * 11) / 2, 120, $titleText, $lightBlue);
    
    // "This certificate is proudly presented to"
    $subtitleText = "This certificate is proudly presented to";
    imagestring($lightCert, 3, ($width - strlen($subtitleText) * 8) / 2, 180, $subtitleText, $white);
    
    // Member name
    imagestring($lightCert, 5, ($width - strlen($memberName) * 11) / 2, 220, $memberName, $orange);
    
    // Draw underline for name
    $nameWidth = strlen($memberName) * 11;
    $underlineStart = ($width - $nameWidth) / 2;
    $underlineEnd = $underlineStart + $nameWidth;
    imageline($lightCert, $underlineStart, 250, $underlineEnd, 250, $orange);
    
    // Appreciation message
    $message1 = "In grateful recognition of your outstanding generosity and unwavering";
    $message2 = "support towards creating a positive impact in our community through";
    $message3 = "SevaConnect.";
    
    imagestring($lightCert, 3, ($width - strlen($message1) * 8) / 2, 290, $message1, $white);
    imagestring($lightCert, 3, ($width - strlen($message2) * 8) / 2, 315, $message2, $white);
    imagestring($lightCert, 3, ($width - strlen($message3) * 8) / 2, 340, $message3, $white);
    
    // Date and signature lines
    imageline($lightCert, 60, 480, 200, 480, $white);
    imageline($lightCert, $width-200, 480, $width-60, 480, $white);
    
    // Date and signature text
    $dateText = "Date: " . date('j F Y');
    imagestring($lightCert, 2, 70, 490, $dateText, $lightGray);
    
    $signatureText = "The SevaConnect Team";
    imagestring($lightCert, 2, $width-190, 490, $signatureText, $lightGray);
    
    // Save light certificate
    $lightFilename = $certificatesDir . 'certificate_light_' . $membershipId . '.png';
    imagepng($lightCert, $lightFilename);
    imagedestroy($lightCert);
    
    // Generate dark theme certificate
    $darkCert = imagecreatetruecolor($width, $height);
    
    // Colors for dark theme
    $darkBg = imagecolorallocate($darkCert, 26, 26, 26);
    $darkBlueText = imagecolorallocate($darkCert, 100, 149, 237);
    $orangeDark = imagecolorallocate($darkCert, 255, 107, 53);
    $whiteText = imagecolorallocate($darkCert, 255, 255, 255);
    $grayText = imagecolorallocate($darkCert, 180, 180, 180);
    
    // Fill background
    imagefill($darkCert, 0, 0, $darkBg);
    
    // Draw decorative border
    imagesetthickness($darkCert, 8);
    imagerectangle($darkCert, 20, 20, $width-20, $height-20, $orangeDark);
    imagesetthickness($darkCert, 3);
    imagerectangle($darkCert, 15, 15, $width-15, $height-15, $orangeDark);
    
    // Add corner decorations
    imagesetthickness($darkCert, 4);
    // Top-left corner
    imageline($darkCert, 40, 40, 100, 40, $orangeDark);
    imageline($darkCert, 40, 40, 40, 100, $orangeDark);
    // Top-right corner
    imageline($darkCert, $width-100, 40, $width-40, 40, $orangeDark);
    imageline($darkCert, $width-40, 40, $width-40, 100, $orangeDark);
    // Bottom-left corner
    imageline($darkCert, 40, $height-40, 100, $height-40, $orangeDark);
    imageline($darkCert, 40, $height-100, 40, $height-40, $orangeDark);
    // Bottom-right corner
    imageline($darkCert, $width-100, $height-40, $width-40, $height-40, $orangeDark);
    imageline($darkCert, $width-40, $height-100, $width-40, $height-40, $orangeDark);
    
    // Add medal/ribbon icon at top center
    imagefilledellipse($darkCert, $iconX, $iconY, 40, 40, $orangeDark);
    imagefilledellipse($darkCert, $iconX, $iconY, 25, 25, $darkBg);
    
    // Add text for dark theme
    imagestring($darkCert, 5, ($width - strlen($titleText) * 11) / 2, 120, $titleText, $darkBlueText);
    imagestring($darkCert, 3, ($width - strlen($subtitleText) * 8) / 2, 180, $subtitleText, $whiteText);
    imagestring($darkCert, 5, ($width - strlen($memberName) * 11) / 2, 220, $memberName, $orangeDark);
    
    // Draw underline for name
    imageline($darkCert, $underlineStart, 250, $underlineEnd, 250, $orangeDark);
    
    // Appreciation message
    imagestring($darkCert, 3, ($width - strlen($message1) * 8) / 2, 290, $message1, $whiteText);
    imagestring($darkCert, 3, ($width - strlen($message2) * 8) / 2, 315, $message2, $whiteText);
    imagestring($darkCert, 3, ($width - strlen($message3) * 8) / 2, 340, $message3, $whiteText);
    
    // Date and signature lines
    imageline($darkCert, 60, 480, 200, 480, $whiteText);
    imageline($darkCert, $width-200, 480, $width-60, 480, $whiteText);
    
    // Date and signature text
    imagestring($darkCert, 2, 70, 490, $dateText, $grayText);
    imagestring($darkCert, 2, $width-190, 490, $signatureText, $grayText);
    
    // Save dark certificate
    $darkFilename = $certificatesDir . 'certificate_dark_' . $membershipId . '.png';
    imagepng($darkCert, $darkFilename);
    imagedestroy($darkCert);
    
    return [$lightFilename, $darkFilename];
}

function sendMembershipConfirmationEmail($email, $name, $membershipId) {
    // Email configuration - you can implement this using PHPMailer or similar
    $subject = "Welcome to Seva Connect - Membership Confirmation";
    $message = "
    Dear $name,
    
    Welcome to Seva Connect! We are delighted to have you as a member of our community.
    
    Your Membership ID: $membershipId
    Registration Date: " . date('Y-m-d H:i:s') . "
    
    Your membership certificates (both light and dark theme) have been generated and will be sent to you within 24 hours.
    
    Thank you for joining us in our mission to serve humanity.
    
    With warm regards,
    Seva Connect Team
    ";
    
    // Uncomment and configure when ready to send emails
    // mail($email, $subject, $message);
}
?>
