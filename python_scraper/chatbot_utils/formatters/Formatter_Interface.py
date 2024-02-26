from abc import ABC, abstractmethod

class Formatter_Interface(ABC):
    ########## domande sui professori
    def format_contatti(self, data):
        pass

    def format_corsi_insegnati(data):
        pass

    def format_informazioni_generali(self,professore):
        pass

    def format_tutte_informazioni(self, data):
        pass

    def format_orari_ricevimento(self,data):
        pass

       ########################################### domande sui dipartimenti ###########################################
    @abstractmethod
    def format_dipartimento_campo(self, domanda, professori, keyword=None):
        pass
    @abstractmethod
    def format_offerta_formativa_dipartimento(self, domanda, dipartimenti, keyword=None):
        pass

        ########################################### # domande sui corsi ###########################################
    @abstractmethod
    def format_insegnamento(self, domanda, professori, keyword=None):
        pass
    @abstractmethod
    def format_offerta_formativa_corso(self, domanda, professori, keyword):
        pass
    @abstractmethod
    def invalid(self,subject):
        pass