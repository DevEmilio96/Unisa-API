<?php

class Database {
    // Variabile statica privata che conterrà l'istanza della classe Database
    private static $instance;
    // Variabile per la connessione al database
    private $connection;


    // Metodo privato per impedire la creazione di nuove istanze della classe Database
    private function __construct() {
        // Leggi le configurazioni dal file .ini
        $this->config = parse_ini_file('conf_test.ini');

        // Recupera le configurazioni specifiche del database
        $this->host = $this->config['host'];
        $this->username = $this->config['username'];
        $this->password = $this->config['password'];
        $this->dbname = $this->config['dbname'];

        // Configura la connessione al database
        $this->connection = new mysqli($this->host, $this->username, $this->password, $this->dbname);
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
    public function insert($table, $data) {
        $keys = implode(", ", array_keys($data));
        $values = "'" . implode("', '", $data) . "'";
        $sql = "INSERT INTO $table ($keys) VALUES ($values)";
        return $this->query($sql);
    }

    public function update($table, $data, $conditions) {
        $set = [];
        foreach ($data as $key => $value) {
            $set[] = "$key = '$value'";
        }
        $setClause = implode(", ", $set);
        $where = [];
        foreach ($conditions as $key => $value) {
            $where[] = "$key = '$value'";
        }
        $whereClause = implode(" AND ", $where);
        $sql = "UPDATE $table SET $setClause WHERE $whereClause";
        return $this->query($sql);
    }

    public function delete($table, $conditions) {
        $where = [];
        foreach ($conditions as $key => $value) {
            $where[] = "$key = '$value'";
        }
        $whereClause = implode(" AND ", $where);
        $sql = "DELETE FROM $table WHERE $whereClause";
        return $this->query($sql);
    }

    public function select($table, $conditions = []) {
        $where = '';
        if (!empty($conditions)) {
            $where = " WHERE ";
            $where .= implode(" AND ", array_map(function ($key, $value) {
                return "$key = '$value'";
            }, array_keys($conditions), $conditions));
        }
        $sql = "SELECT * FROM $table" . $where;
        return $this->query($sql);
    }
}

?>
