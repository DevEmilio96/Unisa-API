from flask import Flask, request, jsonify
from chatbot_utils.utils import *
from chatbot_utils.formatters.TextResponseFormatter import TextResponseFormatter
from chatbot_utils.formatters.VoiceResponseFormatter import VoiceResponseFormatter
import re

app = Flask(__name__)

# Carica i dati JSON
professori = load_json("json/db.json")
dipartimenti = load_json("json/degree_courses.json")

def rispondi_a_domanda(domanda, professori=professori, formato="voce"):
    professore_nome = extract_prof_name(domanda)
    print(f"nome professore trovato: {professore_nome}")
    department_or_field = extract_department_or_field(domanda)

    domande_categorie = {
        # domande sui corsi
        "insegnamento": ["quali professori insegnano", "chi insegna", "che insegnano"],
        "offerta_formativa_corso": ["offerta formativa del corso","scheda", "obiettivi", "preprequisiti","contenuti","metodi didattici","testi"],
        # domande sui dipartimenti
        "dipartimento_campo": ["professori appartenenti al"],
        "offerta_formativa_dipartimento": ["offerta formativa del dipartimento","offerta formativa di","piano di studi"],
        # domande sui professori
        "orari_ricevimento": ["orari di ricevimento"],
        "tutte_informazioni": ["tutte le informazioni", "cosa sai di", "parlami di"],
        "contatti": ["contattare", "contatti", "incontrare"],
        "corsi_insegnati": ["corsi insegna", "cosa insegna", "che insegna"],
        "informazioni_generali": ["chi è"],
        #help
        "aiuto":["cosa sai fare","help","cosa posso chiederti","aiutami"]
    }

    # Categorizza la domanda e trova la risposta appropriata
    for categoria, frasi in domande_categorie.items():
        if any(frase in domanda.lower() for frase in frasi):
            if categoria == "dipartimento_campo" and department_or_field:
                return gestisci_categoria_risposta_sui_dipartimenti(
                    department_or_field, professori, formato, categoria
                )
            elif categoria == "insegnamento":
                return handle_query_with_format(domanda, professori, formato, categoria)
            elif categoria == "offerta_formativa_corso":
                frase_trovata = next((frase for frase in frasi if frase in domanda.lower()), None)
                return offerta_formativa_corso(frase_trovata)
            elif categoria =="offerta_formativa_dipartimento":
                return offerta_formativa_dipartimento(domanda, formato)
            elif categoria =="aiuto":
                return how_to_use_this_chat_bot()
            elif professore_nome:
                professore = find_professore(professore_nome, professori)
                if professore:
                    return gestisci_categoria_risposta_sui_professori(categoria, professore, formato)
                else:
                    return "Professore non trovato."
            break
    return "Non ho ben capito la domanda, puoi usare 'help' per ottenere la lista delle mie funzionalità."
def how_to_use_this_chat_bot():
    help_text = """
        Benvenuto nell'assistente virtuale dell'Università di Salerno! Ecco alcune categorie di domande che puoi farmi, con relativi esempi:

        1. **Insegnamento**
        - Quali professori insegnano Programmazione I?
        - Chi insegna il corso di Matematica?
        - Che insegnano nel corso di Grafica?

        2. **Offerta Formativa del Corso**
        - Qual è l'offerta formativa del corso di Informatica?
        - Potresti mostrarmi la scheda del corso di Fisica?
        - Quali sono gli obiettivi del corso di Chimica?

        3. **Dipartimento**
        - Quali professori appartengono al dipartimento di Ingegneria Informatica?
        - Qual è l'offerta formativa del dipartimento di Matematica?

        4. **Professori**
        - Quali sono gli orari di ricevimento del professor Rossi?
        - Puoi darmi tutte le informazioni su professor Bianchi?
        - Come posso contattare professor Verdi?
        - Quali corsi insegna professor Neri?
        - Chi è Rita Francese?
            """
    
    return help_text
def offerta_formativa_corso(frase_trovata):
    print(f"-----------{frase_trovata}")

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
    if categoria == "insegnamento":
        course_name = extract_course_name(query)
        professors_for_course = find_professors_for_course(course_name, professori)
        if professors_for_course:
            return formatter.format_insegnamento(course_name, professors_for_course)
        else:
            return f"Nessun professore trovato che insegna {course_name}."
        
def gestisci_categoria_risposta_sui_dipartimenti(domanda, professori, formato, categoria):
    print("----------------------------------")
    formatter = (
        VoiceResponseFormatter() if formato == "voce" else TextResponseFormatter()
    )
    if categoria in ["dipartimento_campo", "insegnamento"]:
        if hasattr(formatter, f"format_{categoria}"):
            return getattr(formatter, f"format_{categoria}")(domanda,professori)

    
    # Risposta per categorie non gestite
    return "Non ho ben capito la domanda, puoi usare 'help' per ottenere la lista delle mie funzionalità."
#################################### domande sui professori ####################################
def gestisci_categoria_risposta_sui_professori(categoria, professore, formato):
    # Scelta del formatter in base al formato
    if formato == "voce":
        formatter = VoiceResponseFormatter()
    else:
        formatter = TextResponseFormatter.default(professore["nome"])
    
    # Gestione delle categorie con metodi specifici o default
    if categoria in ["orari_ricevimento", "tutte_informazioni", "contatti", "corsi_insegnati","informazioni_generali"]:
        # Se la categoria corrisponde, usa il metodo specifico se esiste per il formato 'voce',
        # altrimenti usa il metodo 'default' per qualsiasi altro formato
        if hasattr(formatter, f"format_{categoria}"):
            return getattr(formatter, f"format_{categoria}")(professore)
        else:
            return formatter
    
    # Risposta per categorie non gestite
    return "Non ho ben capito la domanda, puoi usare 'help' per ottenere la lista delle mie funzionalità."


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
    print("\n lista dei professori appartenenti al Dipartimento di Informatica")
    print(rispondi_a_domanda("lista dei professori appartenenti al Dipartimento di Informatica"))
    """
    print("\nscheda del corso di Programmazione I?")
    print(
        rispondi_a_domanda("scheda del corso di Programmazione I")
    )

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
