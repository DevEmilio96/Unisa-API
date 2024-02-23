from flask import Flask, request, jsonify
from chatbot_utils.utils import *
from chatbot_utils.formatters.TextResponseFormatter import TextResponseFormatter
from chatbot_utils.formatters.VoiceResponseFormatter import VoiceResponseFormatter
import re
app = Flask(__name__)

# Carica i dati JSON
professori = carica_docenti('json/db.json')

def rispondi_a_domanda(domanda, professori = professori, formato="voce"):
    professore_nome = extract_prof_name(domanda)
    print(f"nome professore trovato {professore_nome}")
    department_or_field = extract_department_or_field(domanda)

    # Mappa categorie di domande a liste di frasi chiave
    domande_categorie = {
        "insegnamento": ["quali professori insegnano", "chi insegna", "che insegnano"],
        "orari_ricevimento": ["orari di ricevimento"],
        "tutte_informazioni": ["tutte le informazioni", "cosa sai di", "parlami di"],
        "contatti": ["contattare", "contatti","incontrare"],
        "corsi_insegnati": ["corsi insegna", "cosa insegna", "che insegna"],
        "informazioni_generali": ["chi è"],
        "dipartimento_campo": ["professori appartenenti al"]
    }

    # Gestione domande sull'insegnamento
    if any(frase in domanda.lower() for frase in domande_categorie["insegnamento"]):
        course_name = extract_course_name(domanda)
        professors_for_course = find_professors_for_course(course_name, professori)
        if professors_for_course:
            response = f"I professori che insegnano {course_name} sono {len(professors_for_course)}: " + ", ".join(professors_for_course) + "."
        else:
            response = f"Nessun professore trovato che insegna {course_name}."
        return response

    # Gestione domande sui dipartimenti o campi di studio
    elif any(frase in domanda.lower() for frase in domande_categorie["dipartimento_campo"]) and department_or_field:
        print(f"----------ho trovato {department_or_field}")
        matched_professors = find_professors_by_department_or_field(department_or_field, professori)
        if matched_professors:
            matched_professors = list(set(matched_professors))
            matched_professors = [prof for prof in matched_professors if prof and prof != "Null"]
            return f"I professori che insegnano presso il dipartimento di {department_or_field} sono {len(matched_professors)}: " + ", ".join(matched_professors) + "."
        else:
            return f"Nessun professore trovato che insegna presso il dipartimento di {department_or_field}."

    # Gestione domande su un professore specifico
    elif professore_nome:
        
        professore = find_professore(professore_nome, professori)
        if professore:
            for categoria, frasi in domande_categorie.items():
                if any(frase in domanda.lower() for frase in frasi):
                    return gestisci_categoria_risposta(categoria, professore, formato)
        else:
            return "Professore non trovato."
    else:
        return "Non sono riuscito a identificare il nome del professore nella domanda."

def gestisci_categoria_risposta(categoria, professore, formato):
    if categoria == "orari_ricevimento":
        if formato == 'voce':
            formatter = VoiceResponseFormatter()
            return formatter.formatReceptionHours(professore)
        if formato == 'testo':
            return TextResponseFormatter.default(professore['nome'])

    elif categoria == "tutte_informazioni":
        if formato == 'voce':
            formatter = VoiceResponseFormatter()
            return formatter.allInfo(professore)
        if formato == 'testo':
            return TextResponseFormatter.default(professore['nome'])

    elif categoria == "contatti":
        if formato == 'voce':
            formatter = VoiceResponseFormatter()
            return formatter.formatContacts(professore)
        if formato == 'testo':
            return TextResponseFormatter.default(professore['nome'])

    elif categoria == "corsi_insegnati":
        if formato == 'testo':
            return TextResponseFormatter.default(professore['nome'])
        if formato == 'voce':
            formatter = VoiceResponseFormatter()
            return formatter.formatTeachedCourses(professore)
        
    elif categoria == "informazioni_generali":
        return f"{professore['nome']} è {professore['titolo']} presso {professore['dipartimento']}."

    return "Domanda non riconosciuta o categoria non gestita."


@app.route('/chatbot', methods=['POST'])
def chatbot():
    dati_richiesta = request.get_json()
    testo_domanda = dati_richiesta.get("domanda")
    formato_risposta = dati_richiesta.get("formato", "voce")  # Default a "testo" se non specificato
    risposta = rispondi_a_domanda(testo_domanda, formato=formato_risposta)
    return jsonify({"risposta": risposta})

if __name__ == '__main__':
    print("\nQuali sono gli orari di ricevimento di Rita Francese?")
    print(rispondi_a_domanda("Quali sono gli orari di ricevimento di Rita Francese?"))
    '''
    print("\nQuali sono gli orari di ricevimento di Rita Francese?")
    print(rispondi_a_domanda("Quali sono gli orari di ricevimento di Rita Francese?"))

    print("\ntutte le informazioni Rita Francese?")
    print(rispondi_a_domanda("tutte le informazioni Rita Francese?"))

    print("\nCome posso contattare Rita Francese?")
    print(rispondi_a_domanda("Come posso contattare Rita Francese?"))

    print("\nQuali sono i contatti telefonici di Carmine PELLEGRINO?")
    print(rispondi_a_domanda("Quali sono i contatti telefonici di Carmine PELLEGRINO?"))

    print("\nDimmi i contatti telefonoci di Rita Francese?")
    print(rispondi_a_domanda("Dimmi i contatti telefonoci di Rita Francese"))

    print("\nquali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?")
    print(rispondi_a_domanda("quali professori insegnano TECNOLOGIE SOFTWARE PER IL WEB?"))

    print("\nchi insegna Programmazione I")
    print(rispondi_a_domanda("chi insegna Programmazione I"))
    
    print("\ncosa insegna Rita Francese?")
    print(rispondi_a_domanda("cosa insegna Rita Francese?"))
    
    print("\ndammi la lista dei professori che insegnano Informatica")
    print(rispondi_a_domanda("dammi la lista dei professori che insegnano Informatica"))

    print("\n lista dei professori appartenenti al Dipartimento di Informatica")
    print(rispondi_a_domanda("lista dei professori appartenenti al Dipartimento di Informatica"))
    '''
    

    app.run(debug=True)


