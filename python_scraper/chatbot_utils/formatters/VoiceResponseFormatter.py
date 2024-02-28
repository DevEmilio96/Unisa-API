from chatbot_utils.utils import *
from datetime import datetime
from chatbot_utils.formatters.Formatter_Interface  import Formatter_Interface

class VoiceResponseFormatter(Formatter_Interface):
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

        return {"data":" ".join(response_parts) + ".", "gesture":"happy"}
    
    @staticmethod
    def format_corsi_insegnati(data):
        corsi = data.get("corsi", [])
        if corsi:
            corsi_str = ", ".join([corso["name"] for corso in corsi])
            return {"data":f"{data['nome']}, insegna i seguenti corsi: {corsi_str}.", "gesture":"happy"}
        else:
            return {"data":f"Non sono stati trovati corsi insegnati da {data['nome']}.", "gesture":"ugly"}
        
    def format_informazioni_generali(self,professore):
        return {"data":f"{professore['nome']} è {professore['titolo']} presso {professore['dipartimento']}.", "gesture":"happy"}
        
    def format_tutte_informazioni(self, data):
        info_parts = [f"{data['nome']}"]

        titolo = data.get('titolo')
        if titolo:
            info_parts.append(f"è {titolo}")

        dipartimento = data.get('dipartimento')
        if dipartimento:
            info_parts.append(f"presso il {dipartimento}.")

        if data['corsi']:
            info_parts.append(self.format_corsi_insegnati(data)['data'])

        contatti = self.format_contatti(data)['data']
        if contatti:
            info_parts.append(contatti)

        orari_ricevimento = format_orari(data.get('orari_di_ricevimento', []))
        if orari_ricevimento:
            info_parts.append(f"È possibile incontrare {data['nome']} nei seguenti orari di ricevimento: {orari_ricevimento}")

        # Rimuove parti vuote e unisce il tutto in una stringa
        return {"data":" ".join(filter(None, info_parts)), "gesture":"happy"}
    
    def format_orari_ricevimento(self,data):
        orari_ricevimento = format_orari(data.get('orari_di_ricevimento', []))
        if orari_ricevimento:
            return {"data":f"È possibile incontrare {data['nome']} nei seguenti orari di ricevimento: {orari_ricevimento}", "gesture":"happy"}
        else:
            return {"data":f"{data['nome']} non ha specificato degli orari di ricevimento.", "gesture":"ugly"}

    ########################################### domande sui dipartimenti ###########################################
    def format_dipartimento_campo(self, domanda, professori, keyword=None):
        department_or_field = domanda
        matched_professors = find_all_professors_details_by_department_or_field(
            department_or_field, professori
        )
        if matched_professors:
            # Assumendo che matched_professors sia una lista di dizionari,
            # dove ogni dizionario rappresenta un professore e ha una chiave 'nome'
            professori_nomi = [prof['nome'] for prof in matched_professors]
            if len(matched_professors)>10:
                return {"data": f"I professori del dipartimento di {department_or_field} sono {len(matched_professors)}: " + ", ".join(professori_nomi[:10]) + ", e altri che puoi visualizzare sull'interfaccia.", "gesture":"happy"}
            else:
                return {"data": f"I professori del dipartimento di {department_or_field} sono {len(matched_professors)}: " + ", ".join(professori_nomi) + ".", "gesture":"happy"}
        else:
            return {"data": f"Nessun professore trovato per il dipartimento di {department_or_field}.", "gesture":"ugly"}

    def format_offerta_formativa_dipartimento(self, domanda, dipartimenti, keyword=None):
        # Calcola l'anno corrente
        dipartimento = find_department_by_department_name(domanda, dipartimenti)
        if dipartimento:
            anno_corrente = datetime.now().year
            return {"data":f"Puoi visualizzare sull'interfaccia l'offerta formativa per il percorso di studi di {dipartimento['nome']} per l'anno {anno_corrente-1}-{anno_corrente}. ", "gesture":"happy"}
    
    ########################################### # domande sui corsi ###########################################
    def format_insegnamento(self, domanda, professori, keyword=None):
        course_name = extract_course_name(domanda)
        professors_for_course = find_all_professors_details_for_course(course_name, professori)
        if professors_for_course:
            # Utilizza una list comprehension per estrarre i nomi dei professori
            professori_nomi = [prof['nome'] for prof in professors_for_course]
            if len(professori_nomi)>10:
                return {"data":f"I professori che insegnano {course_name} sono {len(professors_for_course)}: " + ", ".join(professori_nomi[:10]) + ", e altri che puoi visualizzare sull'interfaccia.", "gesture":"happy"}
            else:
                return {"data":f"I professori che insegnano {course_name} sono {len(professors_for_course)}: " + ", ".join(professori_nomi) + ".", "gesture":"happy"}
        else:
            return {"data":f"Nessun professore trovato che insegna {course_name}.", "gesture":"ugly"}

    
    def format_offerta_formativa_corso(self, domanda, professori, keyword):
        
        course_name = extract_course_name(domanda)
        
        professors_for_course = find_all_professors_details_for_course(course_name, professori)
        
        # Inizializza una variabile per tenere traccia del corso cercato
        dettagli_corso_cercato = None

        # Assicurati di procedere solo se ci sono professori associati al corso
        if professors_for_course:
            # Scorri tutti i professori trovati per il corso
            for professor_info in professors_for_course:
                professore = find_professore(professor_info['nome'], professori)
                
                # Scorri tutti i corsi per trovare quello specifico
                for corso in professore["corsi"]:
                    # Usa 'in' per verificare se course_name è una sottostringa di corso["name"]
                    if course_name.upper() == corso["name"].upper():  # Confronto case-insensitive
                        # Controlla se la chiave 'scheda' esiste e contiene il dettaglio cercato
                        if 'scheda' in corso and keyword.lower() in (key.lower() for key in corso['scheda']):
                            dettagli_corso_cercato = corso
                            break  # Interrompi il ciclo se hai trovato il corso con i dettagli richiesti
                        elif 'scheda' in corso:
                            # Se il corso ha una 'scheda' ma non il dettaglio cercato, segna come possibile match
                            dettagli_corso_cercato = corso
                            # Non interrompere il ciclo, continua a cercare un corso migliore
                if dettagli_corso_cercato and 'scheda' in dettagli_corso_cercato:
                    break  # Se hai trovato un corso con i dettagli richiesti, interrompi il ciclo dei professori

            # Verifica il risultato della ricerca
            if not dettagli_corso_cercato:
                return {"data":f"Dettagli non trovati per il corso {course_name}", "gesture":"ugly"}
            elif 'scheda' not in dettagli_corso_cercato:
                return {"data":f"Dettagli '{keyword}' non disponibili per il corso {course_name}", "gesture":"ugly"}

            if keyword in ["obiettivi", "prerequisiti", "contenuti", "metodi didattici", "testi"]:
                # Normalizza la keyword per il confronto
                keyword_normalized = keyword.lower()
                # Se un corso corrispondente è stato trovato, restituisci i dettagli specifici richiesti
                if dettagli_corso_cercato and any(key.lower() == keyword_normalized for key in dettagli_corso_cercato['scheda']):
                    # Se la condizione è soddisfatta, fai qualcosa con i dettagli del corso
                    # Ad esempio, restituisci il valore associato alla keyword nel dizionario 'scheda'
                    for key, value in dettagli_corso_cercato['scheda'].items():
                        if key.lower() == keyword_normalized:
                            return {"data":f"{keyword} per {course_name}: {value}", "gesture":"happy"}
            else:
                return {"data": f"Puoi visualizzare sulla mia interfaccia la scheda del corso per {course_name}", "gesture":"happy"}
        else:
            return {"data": f"Non ho trovato nessun professore che insegna {course_name}", "gesture":"ugly"}
    def invalid(self,subject):
        if subject =="question":
            return {"data":"Non ho ben capito la domanda, puoi dire 'aiuto' per ottenere la lista delle mie funzionalità.", "gesture":"ugly"}
        if subject =="professor":
            return {"data":"Professore non trovato.", "gesture":"ugly"}
    pass