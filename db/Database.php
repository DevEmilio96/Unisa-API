<?php

class Database {
    // Variabile statica privata che conterrà l'istanza della classe Database
    private static $instance;
    // Variabile per la connessione al database
    private $connection;
    // Leggi le configurazioni dal file .ini
    
    //$config = parse_ini_file('conf.ini'); // prod
    $config = parse_ini_file('conf_test.ini'); //test

    // Recupera le configurazioni specifiche del database
    $host = $config['host'];
    $username = $config['username'];
    $password = $config['password'];
    $dbname = $config['dbname'];

    // Metodo privato per impedire la creazione di nuove istanze della classe Database
    private function __construct() {
        // Configura la connessione al database
        $connection = new mysqli($host, $username, $password, $dbname);
        
        // Gestione degli errori di connessione
        if ($this->connection->connect_error) {
            die("Connessione al database fallita: " . $this->connection->connect_error);
        }
    }

    // Metodo pubblico per ottenere l'istanza della classe Database (Singleton)
    public static function getInstance() {
        // Se l'istanza non esiste, creane una nuova
        if (!self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    // Metodo per ottenere la connessione al database
    public function getConnection() {
        return $this->connection;
    }

    // Metodo privato per evitare la duplicazione dell'istanza tramite il clone
    private function __clone() {}

    // Metodo privato per evitare la duplicazione dell'istanza tramite il deserializzazione
    public function __wakeup() {}

    // Metodo per eseguire query sul database
    public function query($sql) {
        return $this->connection->query($sql);
    }

    // Metodo per ottenere il numero di righe interessate dall'ultima query
    public function affectedRows() {
        return $this->connection->affected_rows;
    }

    // Metodo per ottenere l'ID generato automaticamente dall'ultima query INSERT
    public function lastInsertId() {
        return $this->connection->insert_id;
    }
}

?>
