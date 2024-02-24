from flask import Flask, request, jsonify
from chatbot_utils.utils import *
from chatbot_utils.formatters.TextResponseFormatter import TextResponseFormatter
from chatbot_utils.formatters.VoiceResponseFormatter import VoiceResponseFormatter
import re
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Carica i dati JSON
professori = load_json("json/db.json")
dipartimenti = load_json("json/degree_courses.json")

def rispondi_a_domanda(domanda, formato="testo"):
    professore_nome = extract_prof_name(domanda)
    department_or_field = extract_department_or_field(domanda)
    formatter = (
        VoiceResponseFormatter() if formato == "voce" else TextResponseFormatter()
    )
    domande_categorie = {
        # domande sui corsi
        "insegnamento": ["quali professori insegnano", "chi insegna", "che insegnano"],
        "offerta_formativa_corso": ["offerta formativa del corso","scheda", "obiettivi", "prerequisiti","contenuti","metodi didattici","testi"],
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
                return gestisci_categoria_risposta(department_or_field, professori, formato, categoria)
            
            elif categoria == "insegnamento":
                return gestisci_categoria_risposta(domanda, professori, formato, categoria)
            
            elif categoria == "offerta_formativa_corso":
                keyword = next((frase for frase in frasi if frase in domanda.lower()), None)
                return  gestisci_categoria_risposta(domanda, professori, formato, categoria, keyword)
            
            elif categoria =="offerta_formativa_dipartimento":
                return gestisci_categoria_risposta(domanda, dipartimenti, formato, categoria)
            
            elif categoria =="aiuto":
                return how_to_use_this_chat_bot()
            
            elif professore_nome:
                professore = find_professore(professore_nome, professori)
                if professore:
                    return gestisci_categoria_risposta_sui_professori(categoria, professore, formato)
                else:
                    return formatter.invalid("professor")
            break

    return formatter.invalid("question")
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
     
def gestisci_categoria_risposta(domanda, data, formato, categoria, keyword=None):
    formatter = (
        VoiceResponseFormatter() if formato == "voce" else TextResponseFormatter()
    )
    if categoria in ["dipartimento_campo", "insegnamento","offerta_formativa_dipartimento","offerta_formativa_corso"]:
        if hasattr(formatter, f"format_{categoria}"):
            return getattr(formatter, f"format_{categoria}")(domanda, data, keyword)

    
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
@cross_origin()
def chatbot():
    dati_richiesta = request.get_json()
    testo_domanda = dati_richiesta.get("domanda")
    formato_risposta = dati_richiesta.get(
        "formato", "voce"
    )  # Default a "testo" se non specificato
    risposta = rispondi_a_domanda(testo_domanda, formato=formato_risposta)
    return jsonify({"risposta": risposta})

CORS(app)
if __name__ == "__main__":

    print("\nscheda del corso di Programmazione I")
    print(rispondi_a_domanda("scheda del corso di Programmazione I"))

    '''
    print("\nscheda del corso di Programmazione I")
    print(rispondi_a_domanda("scheda del corso di Programmazione I"))

    print("\nuna domanda a caso")
    print(rispondi_a_domanda("una domanda a caso"))
    
    print("\nscheda del corso di ANATOMIA E ISTOLOGIA PATOLOGICA I?")
    print(rispondi_a_domanda("scheda del corso di ANATOMIA E ISTOLOGIA PATOLOGICA I"))

    print("\ndammi la lista dei professori che insegnano programmazione")
    print(rispondi_a_domanda("dammi la lista dei professori che insegnano programmazione"))

    print("\nquali professori insegnano PRODUZIONE ASSISTITA DA CALCOLATORE")
    print(rispondi_a_domanda("quali professori insegnano PRODUZIONE ASSISTITA DA CALCOLATORE"))

    print("\nobiettivi del corso di Programmazione I")
    print(rispondi_a_domanda("obiettivi del corso di Programmazione I"))

    print("\npiano di studi informatica")
    print(rispondi_a_domanda("piano di studi informatica"))

    print("\nscheda del corso di Programmazione I?")
    print(rispondi_a_domanda("scheda del corso di Programmazione I"))

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
