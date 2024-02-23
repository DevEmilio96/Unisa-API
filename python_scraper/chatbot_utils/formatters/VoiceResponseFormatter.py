from chatbot_utils.utils import *

class VoiceResponseFormatter:
    def format_contatti(self, data):
        # Logica per formattare la risposta per la lettura vocale
        nome = data['nome']
        # Inizia a costruire la risposta
        response_parts = [f"Puoi contattare {nome} tramite"]
        
        # Gestione email
        emails = data.get('email')
        if emails:
            if isinstance(emails, list):  # Più email
                emails_str = ", ".join(emails)
            else:  # Singola email
                emails_str = emails
            response_parts.append(f"Email: {emails_str}")
        
        # Gestione telefono
        telefoni = data.get('telefono')
        if telefoni:
            if isinstance(telefoni, list) and telefoni != ["Null"]:  # Più numeri di telefono
                telefoni_str = ", ".join(telefoni)
            elif telefoni != "Null":  # Singolo numero di telefono
                telefoni_str = telefoni
            else:
                telefoni_str = ""
            if telefoni_str:
                if len(response_parts) > 1:  # Se c'è già l'email, aggiungi un congiuntivo
                    response_parts.append("e Telefono:")
                response_parts.append(telefoni_str)

        return " ".join(response_parts) + "."
    
    @staticmethod
    def format_corsi_insegnati(data):
        corsi = data.get("corsi", [])
        if corsi:
            corsi_str = ", ".join([corso["name"] for corso in corsi])
            return f", insegna i seguenti corsi: {corsi_str}."
        else:
            return f"Non sono stati trovati corsi insegnati da {data['nome']}."
        
    def format_tutte_informazioni(self, data):
        info_parts = [f"{data['nome']}"]

        titolo = data.get('titolo')
        if titolo:
            info_parts.append(f"è {titolo}")

        dipartimento = data.get('dipartimento')
        if dipartimento:
            info_parts.append(f"presso il {dipartimento}")

        corsi = self.formatTeachedCourses(data)
        if corsi:
            info_parts.append(corsi)

        contatti = self.formatContacts(data)
        if contatti:
            info_parts.append(contatti)

        orari_ricevimento = format_orari(data.get('orari_di_ricevimento', []))
        if orari_ricevimento:
            info_parts.append(f"È possibile incontrare {data['nome']} nei seguenti orari di ricevimento: {orari_ricevimento}")

        # Rimuove parti vuote e unisce il tutto in una stringa
        return " ".join(filter(None, info_parts))
    
    def format_orari_ricevimento(self,data):
        orari_ricevimento = format_orari(data.get('orari_di_ricevimento', []))
        if orari_ricevimento:
            return f"È possibile incontrare {data['nome']} nei seguenti orari di ricevimento: {orari_ricevimento}"
        else:
            return f"{data['nome']} non ha specificato degli orari di ricevimento."

    def format_dipartimento_campo(self, department_or_field, matched_professors):
        return f"I professori del dipartimento di {department_or_field} sono {len(matched_professors)}: " + ", ".join(matched_professors) + "."
    
    def format_insegnamento(self, course_name,professors_for_course):
        return f"I professori che insegnano {course_name} sono {len(professors_for_course)}: " + ", ".join(professors_for_course) + "."
    #return f"Nessun professore trovato per il dipartimento di {department_or_field}."
    #return f"Nessun professore trovato che insegna {course_name}."


    pass