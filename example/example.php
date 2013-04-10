<?php

/**
 * Example usage of the PHP Client Lib
 */

include '../client_libs/php/crushr.php';

$client = new Crushr\Client();
// $client->serve_compressed(false);
print_r($client->css('homepage'));
print_r($client->js('homepage'));
exit;
