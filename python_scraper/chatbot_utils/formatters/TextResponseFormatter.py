from chatbot_utils.utils import *

class TextResponseFormatter:
    ########################################### # domande sui professori ###########################################
    def default(data):
        return {"data" : data, "type" : {"mode" : "professore"}}
    
    ########################################### # domande sui dipartimenti ###########################################
    def format_dipartimento_campo(self, department_or_field, professori, keyword=None):
        matched_professors = find_professors_by_department_or_field(
            department_or_field, professori
        )
        return {"data" : matched_professors, "type" : {"mode" : "professori-per-dipartimento", "value" : department_or_field}}
    
    
    def format_offerta_formativa_dipartimento(self,domanda, dipartimenti, keyword=None):
        dipartimento = find_department_by_department_name(domanda, dipartimenti)
        if dipartimento:
            return {"data" : dipartimento, "type" : {"mode" : "dipartimento"}}
    
    ########################################### # domande sui corsi ###########################################
    def format_insegnamento(self, domanda, professori, keyword=None):
        course_name = extract_course_name(domanda)
        professors_for_course = find_professors_for_course(course_name, professori)
        return {"data" : professors_for_course, "type" : {"mode" : "professori-per-corso", "value" : course_name}}
       
    def format_offerta_formativa_corso(self, domanda, professori, keyword):
        course_name = extract_course_name(domanda)
        professors_for_course = find_professors_for_course(course_name, professori)

        # Inizializza dettagli_corso_cercato a None
        dettagli_corso_cercato = None

        # Assicurati di procedere solo se ci sono professori associati al corso
        if professors_for_course:
            professore = find_professore(professors_for_course[0], professori)

            # Scorri tutti i corsi per trovare quello specifico
            for corso in professore["corsi"]:
                # Usa 'in' per verificare se course_name è una sottostringa di corso["name"]
                if course_name.upper() in corso["name"].upper():  # Confronto case-insensitive
                    dettagli_corso_cercato = corso
                    break  # Interrompi il ciclo una volta trovato il corso

        # Verifica se il corso è stato trovato e se ha una 'scheda'
        if dettagli_corso_cercato and 'scheda' in dettagli_corso_cercato:
            # Se il corso è stato trovato e ha una 'scheda', restituisci i dettagli del corso
            return {"data" : dettagli_corso_cercato, "type" : {"mode" : "corso"}}
        else:
            # Se il corso non è stato trovato o non ha una 'scheda', restituisci None
            return None
    def invalid(self,subject=None):
        return None
    pass