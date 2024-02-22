from chatbot_utils.utils import *

class VoiceResponseFormatter:
    def formatContacts(self, data):
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
    def formatTeachedCourses(data):
        corsi = data.get("corsi", [])
        if corsi:
            corsi_str = ", ".join([corso["name"] for corso in corsi])
            return f", insegna i seguenti corsi: {corsi_str}."
        else:
            return f"Non sono stati trovati corsi insegnati da {data['nome']}."
        
    def allInfo(self, data):
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
            info_parts.append(f"È possibile parlare con {data['nome']} nei seguenti orari di ricevimento: {orari_ricevimento}")

        # Rimuove parti vuote e unisce il tutto in una stringa
        return " ".join(filter(None, info_parts))

    pass