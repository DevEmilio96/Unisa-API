import unittest
from chatbot import rispondi_a_domanda

class TestRispostaADomanda_for_text_format(unittest.TestCase):
    def test_risposte_domande(self):
        domande_risposte_attese = [
            # Domande sui professori con risposta attesa
            ("chi è Rita Francese?", dict),
            ("Dimmi i contatti telefonoci di Rita Francese?", dict),
            ("Quali sono i contatti telefonici di Carmine PELLEGRINO?", dict),
            ("Come posso contattare Rita Francese?", dict),
            
            # Domande sui professori senza una risposta attesa (ad es., Maradona non è riconosciuto come professore nel contesto dato)
            ("chi è Maradona?", None),
            ("Quali sono gli orari di ricevimento di Maradona?", None),
            
            # Domande sui corsi con dettagli specifici attesi come risposta
            ("obiettivi del corso di Programmazione I", dict),
            ("scheda del corso di Programmazione I", dict),
            
            # Lista dei professori che insegnano una materia specifica
            ("dammi la lista dei professori che insegnano Informatica", dict),
            ("lista dei professori che insegnano Informatica", dict),
            
            # Domande specifiche su corsi o materie
            ("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?", dict),
            
            # Domande su corsi non riconosciuti o senza informazioni disponibili
            ("scheda del corso di ANATOMIA E ISTOLOGIA PATOLOGICA I?", None),
            
            # Domande su professori per corsi specifici
            ("quali professori insegnano PRODUZIONE ASSISTITA DA CALCOLATORE", dict),
            ("dammi la lista dei professori che insegnano programmazione", dict),
            
            # Domande sui dipartimenti o piani di studio
            ("piano di studi informatica", dict),
            
            # Domanda non pertinente o non riconosciuta
            ("una domanda a caso", None)
        ]

        for domanda, tipo_risposta_attesa in domande_risposte_attese:
            with self.subTest(domanda=domanda):
                risposta_ottenuta = rispondi_a_domanda(domanda, formato="testo")

                if tipo_risposta_attesa is None:
                    # Se ci si aspetta None, verifica che la risposta sia effettivamente None
                    self.assertIsNone(risposta_ottenuta, "Era attesa una risposta None, ma è stato ottenuto qualcosa d'altro.")
                else:
                    # Altrimenti, procedi con i controlli originali
                    self.assertIsInstance(risposta_ottenuta, dict, "La risposta ottenuta non è un dizionario come atteso.")
                    self.assertIn('data', risposta_ottenuta, "La chiave 'data' non è presente nella risposta.")
                    self.assertIn('type', risposta_ottenuta, "La chiave 'type' non è presente nella risposta.")
                    # Inserisci qui eventuali altri controlli specifici per il tipo di risposta

    def normalize_text(self, text):
        """Rimuove spazi extra e a capo dal testo."""
        return ' '.join(text.split())

if __name__ == '__main__':
    unittest.main()
