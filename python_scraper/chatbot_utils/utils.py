import json
import spacy

nlp = spacy.load("it_core_news_sm")

def extract_department_or_field(question):
    """
    Estrae il nome del dipartimento o campo di studio dalla domanda.
    """
    # Qui puoi implementare la logica specifica per estrarre il dipartimento o il campo di studio
    # Questo esempio è semplificato e potrebbe richiedere adattamenti.
    keywords = ["dipartimento di", "insegnano", "insegnare", "insegna"]
    for keyword in keywords:
        if keyword in question.lower():
            start_index = question.lower().find(keyword) + len(keyword) + 1
            return question[start_index:].capitalize().rstrip("?").strip()
    return None

def find_professors_by_department_or_field(department_or_field, professori):
    """
    Trova i professori in base al dipartimento o campo di studio.
    """
    matched_professors = []
    for professor in professori:
        if department_or_field.lower() in professor["dipartimento"].lower():
            matched_professors.append(professor["nome"])
    return matched_professors

def extract_course_name(question):
    # Pulisci la domanda rimuovendo spazi e punti interrogativi alla fine
    question_cleaned = question.rstrip(" ?")
    
    # Dividi la domanda pulita in parole
    tokens = question_cleaned.split()
    
    # Definisci una lista di possibili parole chiave che precedono il nome del corso
    keywords = ["insegnano", "insegna"]
    nome_corso = ""
    
    # Cerca ciascuna parola chiave nella domanda
    for keyword in keywords:
        if keyword in question_cleaned:
            # Il nome del corso segue immediatamente la parola chiave
            indice_inizio_corso = tokens.index(keyword) + 1
            nome_corso = " ".join(tokens[indice_inizio_corso:]).title()
            break  # Uscire dal ciclo una volta trovata la parola chiave
    
    return nome_corso


def extract_prof_name(question):
    doc = nlp(question)
    name_parts = []

    # Precedentemente identificato come nome proprio o candidato nome
    prev_token_is_name = False

    for token in doc:
        if token.pos_ == 'PROPN' or prev_token_is_name:
            name_parts.append(token.text)
            prev_token_is_name = True
        elif token.pos_ != 'PROPN' and prev_token_is_name:
            break  # Interrompe l'aggiunta di parti del nome se non si tratta di un nome proprio consecutivo

    full_name = ' '.join(name_parts)
    return full_name if full_name else None

def find_professors_for_course(course_name, professors):
    professors_for_course = []
    for professor in professors:
        for course in professor.get("corsi", []):
            if course_name.upper() in course["name"].upper():  # Usa upper() per il confronto case-insensitive
                professors_for_course.append(professor["nome"])
                break
    return professors_for_course

def find_professore(nome,professori):
    # Normalizza il nome per la ricerca case-insensitive
    nome_lower = nome.lower()
    # Cerca tra i professori quello con il nome corrispondente
    for professore in professori:
        if nome_lower in professore["nome"].lower():
            return professore
    # Se non viene trovato alcun professore con quel nome
    return None

def format_orari(orari):
    if not orari or all(o["day"] == "Null" for o in orari):
        return "Orari di ricevimento non disponibili."
    else:
        return ", ".join([f"{o['day']} dalle {o['timings']} {o['location']}" for o in orari if o["day"] != "Null"])

def format_corsi(corsi):
    if not corsi:
        return "Nessun corso insegnato."
    else:
        return ", ".join([c["name"] for c in corsi])

def format_contatti(professore):
    contatti = []
    if professore.get("email") and professore["email"] != "Null":
        contatti.append(f"Email: {professore['email']}")
    if professore.get("telefono"):
        if isinstance(professore["telefono"], list):
            telefoni = ", ".join(professore["telefono"])
        else:
            telefoni = professore["telefono"]
        if telefoni != "Null":
            contatti.append(f"Telefono/i: {telefoni}")
    if not contatti:
        return "Contatti non disponibili."
    return ", ".join(contatti)

def carica_docenti(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)