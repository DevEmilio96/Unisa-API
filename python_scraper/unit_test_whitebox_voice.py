import unittest
from chatbot import rispondi_a_domanda

class TestRispostaADomanda_for_voice_format(unittest.TestCase):
    def test_risposte_domande(self):
        domande_risposte = [
            ("parlami di Carmine Gravino", {"data": "Carmine GRAVINO è Professore Associato presso il Dipartimento di Informatica/DI. Carmine GRAVINO, insegna i seguenti corsi: INGEGNERIA DEL SOFTWARE, METRICHE E QUALITÀ DEL SOFTWARE, SOFTWARE ENGINEERING FOR SECURE CLOUD SYSTEMS. Puoi contattare Carmine GRAVINO tramite Email: gravino@unisa.it e Telefono: 089 96 35 03. È possibile incontrare Carmine GRAVINO nei seguenti orari di ricevimento: Giovedì dalle 11:00 alle 13:00 presso Edificio F2 Primo Piano, Stanza 077, Venerdì dalle 9:00 alle 11:00 presso Edificio F2 Primo Piano, Stanza 077", "gesture": "happy"}),
            ("chi è carmine gravino", {"data": "Carmine GRAVINO è Professore Associato presso Dipartimento di Informatica/DI.", "gesture": "happy"}),
            ("scheda del corso di Programmazione I", {"data": "Puoi visualizzare sulla mia interfaccia la scheda del corso per Programmazione I", "gesture": "happy"}),
            ("una domanda a caso", {"data": "Non ho ben capito la domanda, puoi dire 'aiuto' per ottenere la lista delle mie funzionalità.", "gesture": "ugly"}),
            ("scheda del corso di ANATOMIA E ISTOLOGIA PATOLOGICA I?", {"data": "Dettagli non trovati per il corso Anatomia e istologia patologica I", "gesture": "ugly"}),
            ("dammi la lista dei professori che insegnano programmazione", {"data": "I professori che insegnano Programmazione sono 40: Rosalba ZIZZA, Maurizio TUCCI, Luigi TROIANO, Francesco TORTORELLA, Paolo TARTAGLIA POLCINI, CARMINE SPAGNUOLO, Sabrina SENATORE, Simone ROMANO, Alberto POSTIGLIONE, Gennaro PERCANNELLA, e altri che puoi visualizzare sull'interfaccia.", "gesture": "happy"}),
            ("quali professori insegnano PRODUZIONE ASSISTITA DA CALCOLATORE", {"data": "I professori che insegnano Produzione assistita da calcolatore sono 1: Pierpaolo CARLONE.", "gesture": "happy"}),
            ("obiettivi del corso di Programmazione I", {"data": "Obiettivi per Programmazione I: CONOSCENZA E CAPACITÀ DI COMPRENSIONE: CONOSCENZA DEI COSTRUTTI DI UN LINGUAGGIO DI PROGRAMMAZIONE DI TIPO PROCEDURALE DI ALTO LIVELLO PER LA SOLUZIONE DI PROBLEMI DI PICCOLE DIMENSIONI. CONOSCENZA DEI PRINCIPI DI BASE DELLA PROGRAMMAZIONE STRUTTURATA E MODULARE. CONOSCENZA DEI PRINCIPI E DEGLI STRUMENTI RELATIVI ALLA TRADUZIONE DI PROGRAMMI SCRITTI IN LINGUAGGIO AD ALTO LIVELLO IN PROGRAMMI SCRITTI IN LINGUAGGIO MACCHINA. CONOSCENZA DEI PRINCIPALI SCHEMI ALGORITMICI PER LA SCANSIONE DI STRUTTURE LINEARI UTILIZZANDO ARRAY E FILE. CAPACITÀ DI APPLICARE CONOSCENZA E COMPRENSIONE: CAPACITÀ DI UTILIZZARE LE CONOSCENZE ACQUISITE NELLA IDEAZIONE, PROGETTAZIONE, CODIFICA, COMPILAZIONE, ESECUZIONE E VERIFICA DI SEMPLICI PROGETTI DI PROGRAMMAZIONE PER LA SOLUZIONE DI PROBLEMI DI PICCOLE DIMENSIONI.", "gesture": "happy"}),
            ("piano di studi informatica", {"data": "Puoi visualizzare sull'interfaccia l'offerta formativa per il percorso di studi di Informatica per l'anno 2023-2024.", "gesture": "happy"}),
            ("scheda del corso di Programmazione I?", {"data": "Puoi visualizzare sulla mia interfaccia la scheda del corso per Programmazione I", "gesture": "happy"}),
            ("quali sono gli orari di ricevimento di Rita Francese?", {"data": "È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso", "gesture": "happy"}),
            ("tutte le informazioni Rita Francese?", {"data": "Rita FRANCESE è Professore Associato presso il Dipartimento di Informatica/DI. Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB. Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16. È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso", "gesture": "happy"}),
            ("come posso contattare Rita Francese?", {"data": "Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16.", "gesture": "happy"}),
            ("quali sono i contatti telefonici di Carmine PELLEGRINO?", {"data": "Puoi contattare Carmine PELLEGRINO tramite Email: cpellegrino@unisa.it e Telefono: 089 96 21 14, 089 96 30 60.", "gesture": "happy"}),
            ("dimmi i contatti telefonoci di Rita Francese", {"data": "Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16.", "gesture": "happy"}),
            ("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?", {"data": "I professori che insegnano Tecnologie software per il web sono 4: Giuseppe SCANNIELLO, Simone ROMANO, Rita FRANCESE, Gennaro COSTAGLIOLA.", "gesture": "happy"}),
            ("chi insegna Programmazione I", {"data": "I professori che insegnano Programmazione I sono 7: Rosalba ZIZZA, Maurizio TUCCI, Simone ROMANO, Fabio Narducci, Michele NAPPI, Riccardo DISTASI, Gianluca DE MARCO.", "gesture": "happy"}),
            ("cosa insegna Rita Francese?", {"data": "Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB.", "gesture": "happy"}),
            ("dammi la lista dei professori che insegnano Informatica", {"data": "I professori che insegnano Informatica sono 42: Rosalba ZIZZA, ROCCO ZACCAGNINO, Tommaso Maria Giovanni UBERTAZZI, Vincenzo TUCCI, Maurizio TUCCI, Luigi TROIANO, Roberto TAGLIAFERRI, Monica Maria Lucia SEBILLO, Giuseppe SCANNIELLO, Domenico Santaniello, e altri che puoi visualizzare sull'interfaccia.", "gesture": "happy"}),
            ("lista dei professori appartenenti al Dipartimento di Informatica", {"data": "I professori del dipartimento di Informatica sono 68: Rosalba ZIZZA, ROCCO ZACCAGNINO, Giuliana VITIELLO, Ugo VACCARO, Maurizio TUCCI, Genoveffa TORTORA, CARMINE SPAGNUOLO, Monica Maria Lucia SEBILLO, Vittorio SCARANO, Giuseppe SCANNIELLO, e altri che puoi visualizzare sull'interfaccia.", "gesture": "happy"})
        ]

        for domanda, risposta_attesa in domande_risposte:
            with self.subTest(domanda=domanda):
                risposta_ottenuta = rispondi_a_domanda(domanda, formato="voce")
                # Si confronta solo il campo "data" delle risposte, poiché il metodo normalize_text si applica a stringhe
                self.assertEqual(self.normalize_text(risposta_attesa["data"]).lower(), self.normalize_text(risposta_ottenuta["data"]).lower())
    
    def normalize_text(self, text):
        """Rimuove spazi extra e a capo dal testo."""
        return ' '.join(text.split())

# Permette l'esecuzione dei test se questo script viene eseguito direttamente
if __name__ == '__main__':
    unittest.main()

'''
("piano di studi informatica", "Puoi visualizzare sull'interfaccia l'offerta formativa per il percorso di studi di INFORMATICA per l'anno 2023-2024."),
##################### domande sui professori #####################
("chi è il professor maradona?","Professore non trovato."),
("chi è rita francese","Rita FRANCESE è Professore Associato presso Dipartimento di Informatica/DI."),
("parlami di rita francese","Rita FRANCESE è Professore Associato presso il Dipartimento di Informatica/DI. Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB. Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16. È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso  Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso"),
("chi è carmine gravino?","Carmine GRAVINO è Professore Associato presso Dipartimento di Informatica/DI."),
("Quali sono gli orari di ricevimento di Rita Francese?", "È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso"),
("tutte le informazioni Rita Francese?", "Rita FRANCESE è Professore Associato presso il Dipartimento di Informatica/DI. Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB. Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16. È possibile incontrare Rita FRANCESE nei seguenti orari di ricevimento: Lunedì con orario non specificato presso  Microsoft teams codice corso: amhccqo, Martedì dalle 15:00 alle 16:30 presso piattaforma teams del corso, Venerdì dalle 15:00 alle 16:30 presso piattaforma teams del corso"),
("Come posso contattare Rita Francese?", "Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16."),
("Quali sono i contatti telefonici di Carmine PELLEGRINO?", "Puoi contattare Carmine PELLEGRINO tramite Email: cpellegrino@unisa.it e Telefono: 089 96 21 14, 089 96 30 60."),
("Dimmi i contatti telefonoci di Rita Francese?", "Puoi contattare Rita FRANCESE tramite Email: francese@unisa.it e Telefono: 089 96 33 16."),
("cosa insegna Rita Francese?", "Rita FRANCESE, insegna i seguenti corsi: ENTERPRISE MOBILE APPLICATION DEVELOPMENT, TECNOLOGIE SOFTWARE PER IL WEB."),
##################### domande sui corsi #####################
("scheda del corso di ANATOMIA E ISTOLOGIA PATOLOGICA I?","Dettagli non trovati per il corso Anatomia e istologia patologica i"),
("scheda del corso di Programmazione I?", "Puoi visualizzare sulla mia interfaccia la scheda del corso per Programmazione i"),
("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?", "I professori che insegnano Tecnologie software per il web sono 4: Giuseppe SCANNIELLO, Simone ROMANO, Rita FRANCESE, Gennaro COSTAGLIOLA."),
("chi insegna Programmazione I", "I professori che insegnano Programmazione I sono 7: Rosalba ZIZZA, Maurizio TUCCI, Simone ROMANO, Fabio Narducci, Michele NAPPI, Riccardo DISTASI, Gianluca DE MARCO."),
("dammi la lista dei professori che insegnano programmazione I", "I professori che insegnano Programmazione sono 40: Rosalba ZIZZA, Maurizio TUCCI, Luigi TROIANO, Francesco TORTORELLA, Paolo TARTAGLIA POLCINI, CARMINE SPAGNUOLO, Sabrina SENATORE, Simone ROMANO, Alberto POSTIGLIONE, Gennaro PERCANNELLA, Maria Angela Pellegrino, Chiara Maria Annunziata ORREI, Fabio Narducci, Michele NAPPI, Barbara MASUCCI, Delfina MALANDRINO, Salvatore LA TORRE, Luca GRECO, MARIACRISTINA GALLO, Angelo GAETA, Vittorio FUCCELLA, Gianluca FRASCA CACCIA, Lidia FOTIA, Massimo FICCO, CHRISTIANCARMINE ESPOSITO, Riccardo DISTASI, Patricia DIAZ DE ALBA, DARIO DI NUCCI, Vincenzo DEUFEMIA, Gianluca DE MARCO, Carmen DE MAIO, Annalisa DE BONIS, Biagio COSENZA, Dajana CONTE, Gemma Catolino, Aniello CASTIGLIONE, Pierpaolo CARLONE, Angelamaria CARDONE, Matilde CARABELLESE, Carlo BLUNDO."),
("quali professori insegnano PRODUZIONE ASSISTITA DA CALCOLATORE", "I professori che insegnano Produzione assistita da calcolatore sono 1: Pierpaolo CARLONE."),
("obiettivi del corso di Programmazione I", "Obiettivi per Programmazione I: CONOSCENZA E CAPACITÀ DI COMPRENSIONE: CONOSCENZA DEI COSTRUTTI DI UN LINGUAGGIO DI PROGRAMMAZIONE DI TIPO PROCEDURALE DI ALTO LIVELLO PER LA SOLUZIONE DI PROBLEMI DI PICCOLE DIMENSIONI. CONOSCENZA DEI PRINCIPI DI BASE DELLA PROGRAMMAZIONE STRUTTURATA E MODULARE. CONOSCENZA DEI PRINCIPI E DEGLI STRUMENTI RELATIVI ALLA TRADUZIONE DI PROGRAMMI SCRITTI IN LINGUAGGIO AD ALTO LIVELLO IN PROGRAMMI SCRITTI IN LINGUAGGIO MACCHINA. CONOSCENZA DEI PRINCIPALI SCHEMI ALGORITMICI PER LA SCANSIONE DI STRUTTURE LINEARI UTILIZZANDO ARRAY E FILE. CAPACITÀ DI APPLICARE CONOSCENZA E COMPRENSIONE: CAPACITÀ DI UTILIZZARE LE CONOSCENZE ACQUISITE NELLA IDEAZIONE, PROGETTAZIONE, CODIFICA, COMPILAZIONE, ESECUZIONE E VERIFICA DI SEMPLICI PROGETTI DI PROGRAMMAZIONE PER LA SOLUZIONE DI PROBLEMI DI PICCOLE DIMENSIONI."),
##################### domanda non pertinente #####################
("una domanda a caso","Non ho ben capito la domanda, puoi dire 'aiuto' per ottenere la lista delle mie funzionalità.")
'''
