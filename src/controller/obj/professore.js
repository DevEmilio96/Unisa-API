
import Papa from 'papaparse';
// Funzione per il caricamento di dati da un file CSV tramite Fetch

async function leggiCSVDaFile(filename) {
    try {
        const response = await fetch(filename);
        if (!response.ok) {
            throw new Error(`Errore durante il caricamento di ${filename}`);
        }
        const csvData = await response.text();
        return Papa.parse(csvData, { header: true }).data;
    } catch (error) {
        console.error('Errore durante la lettura di ' + filename, error);
        return [];
    }
}

class Professore {
    constructor(id) {
        // Inizializzazione delle proprietà della classe
        this.id = id;
        this.nome = '';
        this.titolo = '';
        this.dipartimento = '';
        this.email = '';
        this.ufficio = '';
        this.pagina_personale = '';
        this.url = '';
        this.url_immagine_professore = '';
        this.orari_di_ricevimento = [];
        this.corsi = [];
        this.phone = [];
    }

    async caricaDati() {
        try {
            // Carica il file professori.csv
            const professoriArray = await leggiCSVDaFile('./db/professori.csv');

            // Cerca il professore nell'array
            const professoreTrovato = professoriArray.find(
                (row) => row.id === this.id
            );

            if (!professoreTrovato) {
                throw new Error('Professore non trovato');
            }

            // Copia i dati del professore trovato nell'oggetto Professore
            this.nome = professoreTrovato.nome;
            this.titolo = professoreTrovato.titolo;
            this.dipartimento = professoreTrovato.dipartimento;
            this.email = professoreTrovato.email;
            this.ufficio = professoreTrovato.ufficio;
            this.pagina_personale = professoreTrovato.pagina_personale;
            this.url = professoreTrovato.url;
            this.url_immagine_professore = professoreTrovato.url_immagine_professore;

            // Carica gli altri file CSV
            const [orariCSV, corsiCSV, phoneCSV] = await Promise.all([
                leggiCSVDaFile('../db/orari_di_ricevimento.csv'),
                leggiCSVDaFile('../db/corsi.csv'),
                leggiCSVDaFile('../db/phone.csv'),
            ]);

            // Assegna gli array dei dati all'oggetto Professore
            this.orari_di_ricevimento = orariCSV.filter(
                (row) => row.id_professore === this.id
            );
            this.corsi = corsiCSV.filter(
                (row) => row.id_professore === this.id
            );
            this.phone = phoneCSV.filter(
                (row) => row.id_professore === this.id
            );
            // Aggiungi altri dati se necessario

        } catch (error) {
            console.error('Si è verificato un errore:', error);
        }
    }
}

export default Professore;
