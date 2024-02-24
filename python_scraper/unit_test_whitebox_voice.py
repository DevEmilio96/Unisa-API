import unittest
from chatbot import rispondi_a_domanda

class TestRispostaADomanda_for_voice_format(unittest.TestCase):
    def test_risposte_domande(self):
        domande_risposte = [
            ##################### domande sui dipartimenti #####################
            ("lista dei professori appartenenti al Dipartimento di Informatica","I professori del dipartimento di Informatica sono 68: Rosalba ZIZZA, ROCCO ZACCAGNINO, Giuliana VITIELLO, Ugo VACCARO, Maurizio TUCCI, Genoveffa TORTORA, CARMINE SPAGNUOLO, Monica Maria Lucia SEBILLO, Vittorio SCARANO, Giuseppe SCANNIELLO, Simone ROMANO, Marco ROMANO, Adele Anna RESCIGNO, Giuseppe POLESE, Maria Angela Pellegrino, Fabio PALOMBA, Francesco PALMIERI, Marialaura NOCE, Amelia Giuseppina NOBILE, Fabio Narducci, Michele NAPPI, LEILA MORADI, Barbara MASUCCI, Michele MASTROIANNI, Delfina MALANDRINO, Salvatore LA TORRE, Gerardo IOVANE, Carmine GRAVINO, Carmine Grasso, Virginia GIORNO, Luisa GARGANO, Pietro FUSCO, Vittorio FUCCELLA, Rita FRANCESE, Ugo FIORE, Massimo FICCO, Filomena FERRUCCI, ESLAM FARSIMADAN, CHRISTIANCARMINE ESPOSITO, Riccardo DISTASI, DARIO DI NUCCI, Luigi Di Biasi, Vincenzo DEUFEMIA, Alfredo DE SANTIS, Roberto DE PRISCO, Gianluca DE MARCO, Carmen DE MAIO, Andrea DE LUCIA, Clelia DE FELICE, Annalisa DE BONIS, Paolo D'ARCO, Gianni D'ANGELO, Gennaro COSTAGLIOLA, Biagio COSENZA, STEFANO CIRILLO, Martina Cerulli, Giuseppe CATTANEO, Gemma Catolino, Arcangelo CASTIGLIONE, Lucia CASCONE, LOREDANA CARUCCIO, Bruno CARPENTIERI, Andrea BRUNO, Elmo BENEDETTO, Pietro Battistoni, ALESSIA AURIEMMA CITARELLA, Marcella ANSELMO, Andrea Francesco ABATE."),
            ("piano di studi informatica", "Puoi visualizzare sull'interfaccia l'offerta formativa per il percorso di studi di INFORMATICA per l'anno 2023/2024."),
            ##################### domande sui professori #####################
            ("chi è il professor maradona?","Professore non trovato."),
            ("chi è rita francese","Rita FRANCESE è Professore Associato presso Dipartimento di Informatica/DI."),
            ("chi è carmine gravino?","Carmine GRAVINO è Professore Associato presso Dipartimento di Informatica/DI."),
            ("Quali sono gli orari di ricevimento di Rita Francese?", "È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso"),
            ("tutte le informazioni Rita Francese?", "Rita FRANCESE è Professore Associato presso il Dipartimento di Informatica/DI Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB. Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16. È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso"),
            ("Come posso contattare Rita Francese?", "Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16."),
            ("Quali sono i contatti telefonici di Carmine PELLEGRINO?", "Puoi contattare Carmine PELLEGRINO tramite Email: cpellegrino@unisa.it e Telefono: 089 96 21 14, 089 96 30 60."),
            ("Dimmi i contatti telefonoci di Rita Francese?", "Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16."),
            ("cosa insegna Rita Francese?", "Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB."),
            ##################### domande sui corsi #####################
            ("scheda del corso di ANATOMIA E ISTOLOGIA PATOLOGICA I?","Dettagli non trovati per il corso Anatomia e istologia patologica i"),
            ("scheda del corso di Programmazione I?", "Puoi visualizzare sulla mia interfaccia la scheda del corso per Programmazione i"),
            ("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?", "I professori che insegnano Tecnologie software per il web sono 4: Giuseppe SCANNIELLO, Simone ROMANO, Rita FRANCESE, Gennaro COSTAGLIOLA."),
            ("chi insegna Programmazione I", "I professori che insegnano Programmazione I sono 7: Rosalba ZIZZA, Maurizio TUCCI, Simone ROMANO, Fabio Narducci, Michele NAPPI, Riccardo DISTASI, Gianluca DE MARCO."),
            ("dammi la lista dei professori che insegnano programmazione", "I professori che insegnano Programmazione sono 40: Rosalba ZIZZA, Maurizio TUCCI, Luigi TROIANO, Francesco TORTORELLA, Paolo TARTAGLIA POLCINI, CARMINE SPAGNUOLO, Sabrina SENATORE, Simone ROMANO, Alberto POSTIGLIONE, Gennaro PERCANNELLA, Maria Angela Pellegrino, Chiara Maria Annunziata ORREI, Fabio Narducci, Michele NAPPI, Barbara MASUCCI, Delfina MALANDRINO, Salvatore LA TORRE, Luca GRECO, MARIACRISTINA GALLO, Angelo GAETA, Vittorio FUCCELLA, Gianluca FRASCA CACCIA, Lidia FOTIA, Massimo FICCO, CHRISTIANCARMINE ESPOSITO, Riccardo DISTASI, Patricia DIAZ DE ALBA, DARIO DI NUCCI, Vincenzo DEUFEMIA, Gianluca DE MARCO, Carmen DE MAIO, Annalisa DE BONIS, Biagio COSENZA, Dajana CONTE, Gemma Catolino, Aniello CASTIGLIONE, Pierpaolo CARLONE, Angelamaria CARDONE, Matilde CARABELLESE, Carlo BLUNDO."),
            ("quali professori insegnano PRODUZIONE ASSISTITA DA CALCOLATORE", "I professori che insegnano Produzione assistita da calcolatore sono 1: Pierpaolo CARLONE."),
            ("obiettivi del corso di Programmazione I", "Obiettivi per Programmazione I: CONOSCENZA E CAPACITÀ DI COMPRENSIONE: CONOSCENZA DEI COSTRUTTI DI UN LINGUAGGIO DI PROGRAMMAZIONE DI TIPO PROCEDURALE DI ALTO LIVELLO PER LA SOLUZIONE DI PROBLEMI DI PICCOLE DIMENSIONI. CONOSCENZA DEI PRINCIPI DI BASE DELLA PROGRAMMAZIONE STRUTTURATA E MODULARE. CONOSCENZA DEI PRINCIPI E DEGLI STRUMENTI RELATIVI ALLA TRADUZIONE DI PROGRAMMI SCRITTI IN LINGUAGGIO AD ALTO LIVELLO IN PROGRAMMI SCRITTI IN LINGUAGGIO MACCHINA. CONOSCENZA DEI PRINCIPALI SCHEMI ALGORITMICI PER LA SCANSIONE DI STRUTTURE LINEARI UTILIZZANDO ARRAY E FILE. CAPACITÀ DI APPLICARE CONOSCENZA E COMPRENSIONE: CAPACITÀ DI UTILIZZARE LE CONOSCENZE ACQUISITE NELLA IDEAZIONE, PROGETTAZIONE, CODIFICA, COMPILAZIONE, ESECUZIONE E VERIFICA DI SEMPLICI PROGETTI DI PROGRAMMAZIONE PER LA SOLUZIONE DI PROBLEMI DI PICCOLE DIMENSIONI."),
            ##################### domanda non pertinente #####################
            ("una domanda a caso","Non ho ben capito la domanda, puoi usare 'help' per ottenere la lista delle mie funzionalità.")
        ]


        for domanda, risposta_attesa in domande_risposte:
            with self.subTest(domanda=domanda):
                risposta_ottenuta = rispondi_a_domanda(domanda,formato="voce")
                self.assertEqual(self.normalize_text(risposta_attesa).lower(), self.normalize_text(risposta_ottenuta).lower())
    
    def normalize_text(self,text):
        """Rimuove spazi extra e a capo dal testo."""
        return ' '.join(text.split())
# Permette l'esecuzione dei test se questo script viene eseguito direttamente
if __name__ == '__main__':
    unittest.main()
