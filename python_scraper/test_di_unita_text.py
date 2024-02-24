import unittest
from chatbot import rispondi_a_domanda

class TestRispostaADomanda_for_text_format(unittest.TestCase):
    def test_risposte_domande(self):
        domande_risposte = [
            ##################### domande sui dipartimenti #####################

            ##################### domande sui professori #####################
            ("chi è Rita Francese?",("Rita Francese","professore")),
            ##################### domande sui corsi #####################

            ##################### domanda non pertinente #####################

        ]


        for domanda, risposte_attese in domande_risposte:
            with self.subTest(domanda=domanda):
                risposte_ottenute = rispondi_a_domanda(domanda, formato="testo")

                # Assicurati che entrambe le risposte siano tuple per un confronto elemento per elemento
                self.assertIsInstance(risposte_ottenute, tuple, "La risposta ottenuta non è una tupla")
                self.assertEqual(len(risposte_attese), len(risposte_ottenute), "Le tuple hanno lunghezze diverse")

                for risposta_attesa, risposta_ottenuta in zip(risposte_attese, risposte_ottenute):
                    self.assertEqual(self.normalize_text(risposta_attesa).lower(), self.normalize_text(risposta_ottenuta).lower())

    def normalize_text(self, text):
        """Rimuove spazi extra e a capo dal testo."""
        if not isinstance(text, str):
            raise ValueError("Il testo da normalizzare deve essere una stringa")
        return ' '.join(text.split())

if __name__ == '__main__':
    unittest.main()
