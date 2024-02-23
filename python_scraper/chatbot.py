from flask import Flask, request, jsonify
from chatbot_utils.utils import *
from chatbot_utils.formatters.TextResponseFormatter import TextResponseFormatter
from chatbot_utils.formatters.VoiceResponseFormatter import VoiceResponseFormatter
import re

app = Flask(__name__)

# Carica i dati JSON
professori = load_json("json/db.json")
dipartimenti = load_json("json/degree_courses.json")

def rispondi_a_domanda(domanda, professori=professori, formato="testo"):
    professore_nome = extract_prof_name(domanda)
    print(f"nome professore trovato: {professore_nome}")
    department_or_field = extract_department_or_field(domanda)

    domande_categorie = {
        # domande sui corsi
        "insegnamento": ["quali professori insegnano", "chi insegna", "che insegnano"],
        "offerta_formativa_corso": ["offerta formativa del corso","scheda del corso", "obbiettivi del corso", "preprequisiti del corso","Contenuti del corso","metodi didattici del corso","testi del corso"],
        # domande sui dipartimenti
        "dipartimento_campo": ["professori appartenenti al"],
        "offerta_formativa_dipartimento": ["offerta formativa del dipartimento","offerta formativa di","piano di studi"],
        # domande sui professori
        "orari_ricevimento": ["orari di ricevimento"],
        "tutte_informazioni": ["tutte le informazioni", "cosa sai di", "parlami di"],
        "contatti": ["contattare", "contatti", "incontrare"],
        "corsi_insegnati": ["corsi insegna", "cosa insegna", "che insegna"],
        "informazioni_generali": ["chi è"],
    }

    # Categorizza la domanda e trova la risposta appropriata
    for categoria, frasi in domande_categorie.items():
        if any(frase in domanda.lower() for frase in frasi):
            if categoria == "dipartimento_campo" and department_or_field:
                return handle_query_with_format(
                    department_or_field, professori, formato, categoria
                )
            elif categoria == "insegnamento":
                return handle_query_with_format(domanda, professori, formato, categoria)
            elif categoria =="offerta_formativa_dipartimento":
                return offerta_formativa_dipartimento(domanda, formato)
            elif professore_nome:
                professore = find_professore(professore_nome, professori)
                if professore:
                    return gestisci_categoria_risposta(categoria, professore, formato)
                else:
                    return "Professore non trovato."
            break
    return "Domanda non riconosciuta."

def offerta_formativa_dipartimento(domanda, formato):
    formatter = (
        VoiceResponseFormatter() if formato == "voce" else TextResponseFormatter()
    )
    # Trova il corso nei dati caricati
    dipartimento = find_department_by_department_name(domanda, dipartimenti)
    if dipartimento:
        # Formatta e restituisce la risposta
        return formatter.format_offerta_formativa_dipartimento(dipartimento)
    else:
        return "Corso di studi non trovato."
    
def handle_query_with_format(query, professori, formato, categoria):
    formatter = (
        VoiceResponseFormatter() if formato == "voce" else TextResponseFormatter()
    )
    if categoria == "dipartimento_campo":
        department_or_field = query
        matched_professors = find_professors_by_department_or_field(
            department_or_field, professori
        )
        if matched_professors:
            return formatter.format_dipartimento_campo(
                department_or_field, matched_professors
            )
        else:
            return f"Nessun professore trovato per il dipartimento di {department_or_field}."
    elif categoria == "insegnamento":
        course_name = extract_course_name(query)
        professors_for_course = find_professors_for_course(course_name, professori)
        if professors_for_course:
            return formatter.format_insegnamento(course_name, professors_for_course)
        else:
            return f"Nessun professore trovato che insegna {course_name}."
        


def gestisci_categoria_risposta(categoria, professore, formato):
    formatter = (
        VoiceResponseFormatter()
        if formato == "voce"
        else TextResponseFormatter.default(professore["nome"])
    )
    if categoria in [
        "orari_ricevimento",
        "tutte_informazioni",
        "contatti",
        "corsi_insegnati",
    ]:
        return getattr(formatter, f"format_{categoria}")(professore)
    elif categoria == "informazioni_generali":
        return f"{professore['nome']} è {professore['titolo']} presso {professore['dipartimento']}."

    return "Domanda non riconosciuta o categoria non gestita."


@app.route("/chatbot", methods=["POST"])
def chatbot():
    dati_richiesta = request.get_json()
    testo_domanda = dati_richiesta.get("domanda")
    formato_risposta = dati_richiesta.get(
        "formato", "voce"
    )  # Default a "testo" se non specificato
    risposta = rispondi_a_domanda(testo_domanda, formato=formato_risposta)
    return jsonify({"risposta": risposta})


if __name__ == "__main__":
    print("\npiano di studi informatica")
    print(
        rispondi_a_domanda("offerta formativa del dipartimento di managment dei sistemi turistici")
    )
    """
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
    """

    app.run(debug=True)
