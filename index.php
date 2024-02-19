<?php
// Includi la classe Singleton per la connessione al database
require_once 'db/Database.php';

// Ora puoi utilizzare la classe Database per ottenere la connessione al database
$db = Database::getInstance();
$connection = $db->getConnection();

// Esempio di utilizzo per eseguire una query
$result = $db->query("SELECT * FROM test");
if ($result) {
    echo var_dump($result);
} else {
    echo "Errore nella query: " . $db->getConnection()->error;
}
?>
