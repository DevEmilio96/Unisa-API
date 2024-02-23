class TextResponseFormatter:
    def default(data):
        # Logica per formattare la risposta come testo
        return data
    
    def format_dipartimento_campo(self, department_or_field, matched_professors):
        return matched_professors
    
    def format_insegnamento(self, course_name,professors_for_course):
        return professors_for_course
    
    def format_offerta_formativa_dipartimento(self,dipartimento):
        return dipartimento
    pass