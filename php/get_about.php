<?php
header('Content-Type: text/plain');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

$aboutFile = '../admin/about.txt';

if (file_exists($aboutFile)) {
    echo file_get_contents($aboutFile);
} else {
    echo "Welcome to Seva Connect, a platform dedicated to serving humanity through compassionate giving and community service.";
}
?>
