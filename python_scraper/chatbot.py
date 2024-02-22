from flask import Flask, request, jsonify
from chatbot_utils.utils import *

app = Flask(__name__)

# Carica i dati JSON
professori = carica_docenti('db.json')

def rispondi_a_domanda(domanda):
    professore_nome = extract_prof_name(domanda)
    print(f"nome professore trovato {professore_nome}")
    department_or_field = extract_department_or_field(domanda)
    # Se è stata identificata una domanda riguardante un corso specifico
    if "quali professori insegnano" in domanda.lower() or "chi insegna" in domanda.lower():
        course_name = extract_course_name(domanda)
        professors_for_course = find_professors_for_course(course_name, professori)
        if professors_for_course:
            response = f"I professori che insegnano {course_name} sono: " + ", ".join(professors_for_course) + "."
        else:
            response = f"Nessun professore trovato che insegna {course_name}."
        return response
    
        # Nuova logica per domande sui dipartimenti o campi di studio
    
    elif department_or_field:
        matched_professors = find_professors_by_department_or_field(department_or_field, professori)
        if matched_professors:
            return f"I professori che insegnano {department_or_field} sono: " + ", ".join(matched_professors) + "."
        else:
            return f"Nessun professore trovato che insegna {department_or_field}."
    
    # Se è stata identificata una domanda riguardante un professore specifico
    elif professore_nome:
        professore = find_professore(professore_nome,professori)
        if professore:
            # Risposta per gli orari di ricevimento
            if "orari di ricevimento" in domanda.lower():
                orari = professore.get("orari_di_ricevimento", [])
                if orari:
                    orari_str = ", ".join([f"{orario['day']} dalle {orario['timings']} {orario['location']}" for orario in orari if orario["day"] != "Null"])
                    return f"Gli orari di ricevimento di {professore['nome']} sono: {orari_str}."
                else:
                    return f"Non sono stati trovati orari di ricevimento per {professore['nome']}."
            # Risposta per tutte le informazioni
            elif "tutte le informazioni" in domanda.lower():
                info_parts = [
                    f"Nome: {professore['nome']}",
                    f"Titolo: {professore['titolo']}",
                    f"Dipartimento: {professore['dipartimento']}",
                    f"Corsi insegnati: {format_corsi(professore.get('corsi', []))}",
                    f"Contatti: {format_contatti(professore)}",
                    f"Orari di ricevimento: {format_orari(professore.get('orari_di_ricevimento', []))}"
                ]
                return " ".join(info_parts)

            # Risposta per i contatti o i contatti telefonici
            elif "contattare" in domanda.lower() or "contatti telefonici" in domanda.lower() or "contatti telefonoci" in domanda.lower():
                contatti = f"Email: {professore['email']}"
                if isinstance(professore['telefono'], list):
                    telefoni = ", ".join(professore['telefono'])
                else:
                    telefoni = professore['telefono']
                if telefoni != "Null":
                    contatti += f", Telefono/i: {telefoni}"
                return f"Ecco come puoi contattare {professore['nome']}: {contatti}."
            # Risposta per i corsi insegnati
            elif "corsi insegna" in domanda.lower() or "cosa insegna" in domanda.lower() or "che insegna" in domanda.lower():
                corsi = professore.get("corsi", [])
                if corsi:
                    corsi_str = ", ".join([corso["name"] for corso in corsi])
                    return f"{professore['nome']} insegna i seguenti corsi: {corsi_str}."
                else:
                    return f"Non sono stati trovati corsi insegnati da {professore['nome']}."
            # Risposta generale sul professore
            elif "chi è" in domanda.lower():
                return f"{professore['nome']} è {professore['titolo']} presso {professore['dipartimento']}."
        else:
            return "Professore non trovato."
    else:
        return "Non sono riuscito a identificare il nome del professore nella domanda."



@app.route('/chatbot', methods=['POST'])
def chatbot():
    dati_richiesta = request.get_json()
    testo_domanda = dati_richiesta.get("domanda")
    risposta = rispondi_a_domanda(testo_domanda)
    return jsonify({"risposta": risposta})

if __name__ == '__main__':
    print("Quali sono gli orari di ricevimento di Rita Francese?")
    print(rispondi_a_domanda("Quali sono gli orari di ricevimento di Rita Francese?"))

    print("tutte le informazioni Rita Francese?")
    print(rispondi_a_domanda("tutte le informazioni Rita Francese?"))

    print("Come posso contattare Rita Francese?")
    print(rispondi_a_domanda("Come posso contattare Rita Francese?"))

    print("Quali sono i contatti telefonici di Rita Francese?")
    print(rispondi_a_domanda("Quali sono i contatti telefonici di Rita Francese?"))

    print("Dimmi i contatti telefonoci di Rita Francese?")
    print(rispondi_a_domanda("Dimmi i contatti telefonoci di Rita Francese"))

    print("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?")
    print(rispondi_a_domanda("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?"))

    print("chi insegna Programmazione I")
    print(rispondi_a_domanda("chi insegna Programmazione I"))

    print("che insegna Rita Francese?")
    print(rispondi_a_domanda("che insegna Rita Francese?"))

    print("dammi la lista dei professori che insegnano matematica")
    print(rispondi_a_domanda("dammi la lista dei professori che insegnano matematica"))

    

    app.run(debug=True)


