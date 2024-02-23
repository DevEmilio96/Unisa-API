from chatbot_utils.utils import *

class TextResponseFormatter:
    ########################################### # domande sui professori ###########################################
    def default(data):
        return data
    
    ########################################### # domande sui dipartimenti ###########################################
    def format_dipartimento_campo(self, department_or_field, professori):
        matched_professors = find_professors_by_department_or_field(
            department_or_field, professori
        )
        return matched_professors
    
    
    def format_offerta_formativa_dipartimento(self,domanda, dipartimenti):
        dipartimento = find_department_by_department_name(domanda, dipartimenti)
        if dipartimento:
            return dipartimento
    
    ########################################### # domande sui corsi ###########################################
    def format_insegnamento(self, domanda, professori):
        course_name = extract_course_name(domanda)
        professors_for_course = find_professors_for_course(course_name, professori)
        return professors_for_course   
       
    def format_offerta_formativa_corso(self, domanda, dipartimenti, keyword):
        course_name = extract_course_name(domanda)
        print(keyword)
    pass