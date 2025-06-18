<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'db_config.php';
require_once 'admin_auth_helper.php';

// Require admin authentication
requireAdminAuth();

try {
    $type = $_GET['type'] ?? 'general';
    
    if ($type === 'causes') {
        // Get donations by cause
        $stmt = $pdo->query("
            SELECT 
                cause,
                COUNT(*) as total_donations,
                SUM(amount) as total_amount
            FROM donations 
            WHERE payment_status = 'completed'
            GROUP BY cause
            ORDER BY total_amount DESC
        ");
        $data = $stmt->fetchAll();
        
    } else {
        // Get general statistics
        $totalDonationsStmt = $pdo->query("SELECT COUNT(*) as count FROM donations WHERE payment_status = 'completed'");
        $totalDonations = $totalDonationsStmt->fetch()['count'];
        
        $totalAmountStmt = $pdo->query("SELECT SUM(amount) as total FROM donations WHERE payment_status = 'completed'");
        $totalAmount = $totalAmountStmt->fetch()['total'] ?? 0;
        
        $totalMembersStmt = $pdo->query("SELECT COUNT(*) as count FROM members WHERE status = 'active'");
        $totalMembers = $totalMembersStmt->fetch()['count'];
        
        $thisMonthStmt = $pdo->query("
            SELECT SUM(amount) as total 
            FROM donations 
            WHERE payment_status = 'completed'
            AND YEAR(created_at) = YEAR(CURDATE())
            AND MONTH(created_at) = MONTH(CURDATE())
        ");
        $thisMonth = $thisMonthStmt->fetch()['total'] ?? 0;
        
        $data = [
            'totalDonations' => $totalDonations,
            'totalAmount' => number_format($totalAmount, 2),
            'totalMembers' => $totalMembers,
            'thisMonth' => number_format($thisMonth, 2)
        ];
    }
    
    echo json_encode(['success' => true, 'data' => $data]);
    
} catch (Exception $e) {
    error_log("Stats error: " . $e->getMessage());
    echo json_encode(['success' => false, 'message' => 'Error loading statistics']);
}
?>
