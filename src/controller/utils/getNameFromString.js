// Funzione che estrapola il nome da una frase
import Papa from 'papaparse';
function estraiNomeDaFrase(frase) {
    const paroleDiRicerca = [
        'chi è',
        'chi è il professore',
        'chi è la professoressa',
        'parlami di',
        'parlami della professoressa',
        'parlami del professore',
        'cosa sai dirmi di',
        'cosa sai dirmi del professore',
        'cosa sai dirmi della professoressa',
        'raccontami qualcosa su',
        'raccontami qualcosa sulla professoressa',
        'raccontami qualcosa sul professore',
        'presentami',
        'presentami la professoressa',
        'presentami il professore',
        'conosci',
        'conosci la professoressa',
        'conosci il professore',
        'mostrami',
        'quali corsi insegna',
        'che corsi insegna'
    ];
    let nomeEstratto = frase.toLowerCase();

    paroleDiRicerca.forEach(parola => {
        nomeEstratto = nomeEstratto.replace(parola, '');
    });

    // Rimuove gli spazi bianchi all'inizio e alla fine della stringa
    nomeEstratto = nomeEstratto.trim();

    return trovaIdProfessore(nomeEstratto);
}

// Funzione che cerca il nome nel file CSV e restituisce l'ID del professore
async function trovaIdProfessore(inputRicerca) {
    try {
        const response = await fetch('./db/professori.csv');
        const csvData = await response.text();
        return new Promise((resolve) => {
            Papa.parse(csvData, {
                header: true,
                complete: function(results) {
                    const inputRicercaLower = inputRicerca.toLowerCase();
                    const corrispondenze = results.data.filter(professore =>
                        professore.nome && professore.nome.toLowerCase().includes(inputRicercaLower) // Aggiunto controllo su professore.nome
                    );
                    const ids = corrispondenze.map(professore => professore.id);
                    resolve(ids.length > 0 ? ids : []);
                },
                error: function() {
                    resolve([]);
                }
            });
        });
    } catch (error) {
        console.error("Errore durante il fetch o l'analisi dei dati:", error);
        return []; // Restituisce un array vuoto in caso di errore
    }
}

export default estraiNomeDaFrase;