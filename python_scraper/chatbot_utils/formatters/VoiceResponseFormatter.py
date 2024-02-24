from chatbot_utils.utils import *
from datetime import datetime

class VoiceResponseFormatter:
    ########################################### domande sui professori ###########################################
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
            return f"{data['nome']}, insegna i seguenti corsi: {corsi_str}."
        else:
            return f"Non sono stati trovati corsi insegnati da {data['nome']}."
        
    def format_informazioni_generali(professore):
        return f"{professore['nome']} è {professore['titolo']} presso {professore['dipartimento']}."
        
    def format_tutte_informazioni(self, data):
        info_parts = [f"{data['nome']}"]

        titolo = data.get('titolo')
        if titolo:
            info_parts.append(f"è {titolo}")

        dipartimento = data.get('dipartimento')
        if dipartimento:
            info_parts.append(f"presso il {dipartimento}")

        if data['corsi']:
            info_parts.append(self.format_corsi_insegnati(data))

        contatti = self.format_contatti(data)
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

    ########################################### domande sui dipartimenti ###########################################
    def format_dipartimento_campo(self, domanda, professori, keyword=None):
        department_or_field = domanda
        matched_professors = find_professors_by_department_or_field(
            department_or_field, professori
        )
        if matched_professors:
            return f"I professori del dipartimento di {department_or_field} sono {len(matched_professors)}: " + ", ".join(matched_professors) + "."
        else:
            return f"Nessun professore trovato per il dipartimento di {department_or_field}."
        
    
    def format_offerta_formativa_dipartimento(self, domanda, dipartimenti, keyword=None):
        # Calcola l'anno corrente
        dipartimento = find_department_by_department_name(domanda, dipartimenti)
        if dipartimento:
            anno_corrente = datetime.now().year
            return f"Puoi visualizzare sull'interfaccia l'offerta formativa per il percorso di studi di {dipartimento['nome']} per l'anno {anno_corrente-1}/{anno_corrente}. "
    
    ########################################### # domande sui corsi ###########################################
    def format_insegnamento(self, domanda, professori, keyword=None):
        course_name = extract_course_name(domanda)
        print(f"nome corso: {course_name}")
        professors_for_course = find_professors_for_course(course_name, professori)
        if professors_for_course:
                # Preparazione della parte iniziale della frase in base al numero di professori
            if len(professors_for_course) == 0:
                return f"Non ci sono professori che insegnano {course_name}."
            elif len(professors_for_course) == 1:
                intro = f"Il professore che insegna {course_name} è: "
            else:
                intro = f"I professori che insegnano {course_name} sono {len(professors_for_course)}: "
    
                # Costruzione della frase finale
            professors_list = ", ".join(professors_for_course)
            return intro + professors_list + "."
        else:
            return f"Nessun professore trovato che insegna {course_name}."
        
    
    def format_offerta_formativa_corso(self, domanda, professori, keyword):
        
        course_name = extract_course_name(domanda)
        professors_for_course = find_professors_for_course(course_name, professori)
        
        # Assicurati di procedere solo se ci sono professori associati al corso
        if professors_for_course:
            professore = find_professore(professors_for_course[0], professori)
            dettagli_corso_cercato = None
            # Scorri tutti i corsi per trovare quello specifico
            for corso in professore["corsi"]:
                # Usa 'in' per verificare se course_name è una sottostringa di corso["name"]
                if course_name.upper() in corso["name"].upper():  # Confronto case-insensitive
                    dettagli_corso_cercato = corso
                    break  # Interrompi il ciclo una volta trovato il corso

            if not dettagli_corso_cercato:
                return f"Dettagli non trovati per il corso {course_name}"
            
            if 'scheda' not in dettagli_corso_cercato or keyword.lower() not in (key.lower() for key in dettagli_corso_cercato['scheda']):
                return f"Dettaglio '{keyword}' non disponibile per il corso {course_name}"

            if keyword in ["obiettivi", "prerequisiti", "contenuti", "metodi didattici", "testi"]:
                # Normalizza la keyword per il confronto
                keyword_normalized = keyword.lower()
                # Se un corso corrispondente è stato trovato, restituisci i dettagli specifici richiesti
                if dettagli_corso_cercato and any(key.lower() == keyword_normalized for key in dettagli_corso_cercato['scheda']):
                    # Se la condizione è soddisfatta, fai qualcosa con i dettagli del corso
                    # Ad esempio, restituisci il valore associato alla keyword nel dizionario 'scheda'
                    for key, value in dettagli_corso_cercato['scheda'].items():
                        if key.lower() == keyword_normalized:
                            return f"{keyword} per {course_name}: {value}"
            else:
                return f"Puoi visualizzare sulla mia interfaccia la scheda del corso per {course_name}"
        else:
            return f"Non ho trovato nessun professore che insegna {course_name}"
    pass