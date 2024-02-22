from flask import Flask, request, jsonify
from chatbot_utils.utils import *

app = Flask(__name__)

# Carica i dati JSON
professori = carica_docenti('json/db.json')

def rispondi_a_domanda(domanda, professori = professori):
    professore_nome = extract_prof_name(domanda)
    print(f"nome professore trovato {professore_nome}")
    department_or_field = extract_department_or_field(domanda)

    # Mappa categorie di domande a liste di frasi chiave
    domande_categorie = {
        "insegnamento": ["quali professori insegnano", "chi insegna", "che insegnano"],
        "orari_ricevimento": ["orari di ricevimento"],
        "tutte_informazioni": ["tutte le informazioni"],
        "contatti": ["contattare", "contatti telefonici", "contatti telefonoci"],
        "corsi_insegnati": ["corsi insegna", "cosa insegna", "che insegna"],
        "informazioni_generali": ["chi è"],
        "dipartimento_campo": ["lista dei professori appartenenti al"]
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
                    return gestisci_categoria_risposta(categoria, professore, domanda)
        else:
            return "Professore non trovato."
    else:
        return "Non sono riuscito a identificare il nome del professore nella domanda."

def gestisci_categoria_risposta(categoria, professore, domanda):
    if categoria == "orari_ricevimento":
        orari = professore.get("orari_di_ricevimento", [])
        if orari:
            orari_str = ", ".join([f"{orario['day']} dalle {orario['timings']} {orario['location']}" for orario in orari if orario["day"] != "Null"])
            return f"Gli orari di ricevimento di {professore['nome']} sono: {orari_str}."
        else:
            return f"Non sono stati trovati orari di ricevimento per {professore['nome']}."
    elif categoria == "tutte_informazioni":
        info_parts = [
            f"Nome: {professore['nome']}",
            f"Titolo: {professore['titolo']}",
            f"Dipartimento: {professore['dipartimento']}",
            f"Corsi insegnati: {format_corsi(professore.get('corsi', []))}",
            f"Contatti: {format_contatti(professore)}",
            f"Orari di ricevimento: {format_orari(professore.get('orari_di_ricevimento', []))}"
        ]
        return " ".join(info_parts)
    elif categoria == "contatti":
        contatti = f"Email: {professore['email']}"
        if isinstance(professore['telefono'], list):
            telefoni = ", ".join(professore['telefono'])
        else:
            telefoni = professore['telefono']
        if telefoni != "Null":
            contatti += f", Telefono/i: {telefoni}"
        return f"Ecco come puoi contattare {professore['nome']}: {contatti}."
    elif categoria == "corsi_insegnati":
        corsi = professore.get("corsi", [])
        if corsi:
            corsi_str = ", ".join([corso["name"] for corso in corsi])
            return f"{professore['nome']} insegna i seguenti corsi: {corsi_str}."
        else:
            return f"Non sono stati trovati corsi insegnati da {professore['nome']}."
    elif categoria == "informazioni_generali":
        return f"{professore['nome']} è {professore['titolo']} presso {professore['dipartimento']}."

    return "Domanda non riconosciuta o categoria non gestita."


@app.route('/chatbot', methods=['POST'])
def chatbot():
    dati_richiesta = request.get_json()
    testo_domanda = dati_richiesta.get("domanda")
    risposta = rispondi_a_domanda(testo_domanda)
    return jsonify({"risposta": risposta})

if __name__ == '__main__':
    print("\nQuali sono gli orari di ricevimento di Rita Francese?")
    print(rispondi_a_domanda("Quali sono gli orari di ricevimento di Rita Francese?"))

    print("\ntutte le informazioni Rita Francese?")
    print(rispondi_a_domanda("tutte le informazioni Rita Francese?"))

    print("\nCome posso contattare Rita Francese?")
    print(rispondi_a_domanda("Come posso contattare Rita Francese?"))

    print("\nQuali sono i contatti telefonici di Rita Francese?")
    print(rispondi_a_domanda("Quali sono i contatti telefonici di Rita Francese?"))

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

    

    app.run(debug=True)


