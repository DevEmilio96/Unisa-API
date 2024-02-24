import unittest
from chatbot import rispondi_a_domanda

class TestRispostaADomanda_for_text_format(unittest.TestCase):
    def test_risposte_domande(self):
        domande_risposte = [
            # Domande sui professori
            ("chi è Rita Francese?", ("Rita Francese", "professore")),
            ("chi è Maradona?", None),
            # Domanda non pertinente
            ("una domanda a caso", None)
        ]

        for domanda, risposta_attesa in domande_risposte:
            with self.subTest(domanda=domanda):
                risposta_ottenuta = rispondi_a_domanda(domanda, formato="testo")

                # Gestione di risposte non-stringa (es. None)
                risposta_ottenuta = risposta_ottenuta if isinstance(risposta_ottenuta, str) else str(risposta_ottenuta)
                risposta_attesa = risposta_attesa if isinstance(risposta_attesa, str) else str(risposta_attesa)

                self.assertEqual(self.normalize_text(risposta_attesa).lower(), self.normalize_text(risposta_ottenuta).lower())

    def normalize_text(self, text):
        """Rimuove spazi extra e a capo dal testo."""
        return ' '.join(text.split())

if __name__ == '__main__':
    unittest.main()
