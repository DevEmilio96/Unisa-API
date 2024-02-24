import json
import spacy
import re

nlp = spacy.load("it_core_news_sm")

def extract_department_or_field(question):
    """
    Estrae il nome del dipartimento o campo di studio dalla domanda.
    """
    # Qui puoi implementare la logica specifica per estrarre il dipartimento o il campo di studio
    # Questo esempio è semplificato e potrebbe richiedere adattamenti.
    keywords = ["dipartimento di", "insegnano", "insegnare", "insegna","piano di studi"]
    for keyword in keywords:
        if keyword in question.lower():
            start_index = question.lower().find(keyword) + len(keyword) + 1
            return question[start_index:].capitalize().rstrip("?").strip()
    return None

def find_all_professors_details_by_department_or_field(department_or_field, professori):
    """
    Trova i professori in base al dipartimento o campo di studio.
    """
    matched_professors = []
    for professor in professori:
        if department_or_field.lower() in professor["dipartimento"].lower():
            matched_professors.append(professor)
    return matched_professors


def find_department_by_department_name(department_or_field, dipartimenti, parole_da_ignorare=None):
    """
    Trova i dipartimenti basandosi sul nome del dipartimento, utilizzando spaCy per l'elaborazione del linguaggio naturale,
    ignorando un insieme specifico di parole chiave e gestendo varianti di parole chiave rilevanti.
    """
    if parole_da_ignorare is None:
        parole_da_ignorare = {"di", "in", "su", "il", "la", "del", "della", "piano", "studi","dipartimento"}
    
    # Aggiungi qui eventuali sinonimi o varianti di parole chiave
    varianti_parole_chiave = {
        "informatica": ["informatico", "informatica"],
        # Aggiungi altre varianti di parole chiave se necessario
    }

    doc_query = nlp(department_or_field.lower())
    parole_chiave_query = {token.lemma_ for token in doc_query if not token.is_stop and not token.is_punct and token.lemma_ not in parole_da_ignorare}
    
    # Espandi le parole chiave della query con le loro varianti note
    parole_chiave_query_espanso = set()
    for parola in parole_chiave_query:
        parole_chiave_query_espanso.add(parola)
        if parola in varianti_parole_chiave:
            parole_chiave_query_espanso.update(varianti_parole_chiave[parola])
    
    best_match = None
    max_corrispondenze = 0

    for dipartimento in dipartimenti:
        doc_dipartimento = nlp(dipartimento["nome"].lower())
        parole_chiave_dipartimento = {token.lemma_ for token in doc_dipartimento if not token.is_stop and not token.is_punct and token.lemma_ not in parole_da_ignorare}

        corrispondenze = len(parole_chiave_query_espanso & parole_chiave_dipartimento)
        if corrispondenze > max_corrispondenze:
            max_corrispondenze = corrispondenze
            best_match = dipartimento

    return best_match

def arabic_to_roman(num):
    # Dizionario di conversione per i numeri più comuni trovati nei nomi dei corsi
    conversion_dict = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
        6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X'
    }
    return conversion_dict.get(num, str(num))  # Restituisce il numero romano o il numero originale come stringa

def extract_course_name(question):
    # Pulisci la domanda e crea un documento SpaCy
    question_cleaned = question.rstrip(" ?")
    doc = nlp(question_cleaned)
    
    # Variabili iniziali
    keywords = ["offerta", "scheda", "obiettivi", "prerequisiti", "contenuti", "metodi", "testi", "insegnare", "insegna"]
    ignore_words = ["del", "di", "per", "il", "la", "lo", "i", "gli", "le", "corso", "corsi", "a", "dimmi", "lista", "che", "dei", "professori", "insegnano"]
    nome_corso = ""
    collecting_course_name = False
    
    # Estrazione del nome del corso
    for token in doc:
        if collecting_course_name:
            if token.text.lower() not in ignore_words:
                nome_corso = " ".join([token.text for token in doc[token.i:]]).capitalize()
                break
        elif token.lemma_.lower() in keywords or token.text.lower() in ignore_words:
            collecting_course_name = True
    
    # Conversione da numeri arabi a romani nel nome del corso
    nome_corso_words = nome_corso.split()
    for i, word in enumerate(nome_corso_words):
        if word.isdigit():
            nome_corso_words[i] = arabic_to_roman(int(word))
    
    return " ".join(nome_corso_words)

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
    return re.sub(r"[ ?]+$", "",  full_name) if full_name else None


def find_all_professors_details_for_course(course_name, professors):
    professors_for_course = []
    for professor in professors:
        for course in professor.get("corsi", []):
            if course_name.upper() in course["name"].upper():  # Usa upper() per il confronto case-insensitive
                professors_for_course.append(professor)
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
    # Espressione regolare per validare il formato dell'orario "HH:MM - HH:MM"
    timing_pattern = re.compile(r"\d{2}:\d{2} - \d{2}:\d{2}")

    formatted_orari = []
    for o in orari:
        # Salta l'orario se il giorno non è valido
        if o.get("day") == "Null" or not o.get("day"):
            continue
        
        # Controlla se il formato di 'timings' è corretto
        timings = o.get("timings", "")
        if not timing_pattern.match(timings):
            # Puoi decidere di saltare questo orario, inserire un placeholder, o gestirlo in altro modo
            timings = "con orario non specificato"
        else:
            timings = "dalle " + timings
            timings = timings.replace("-","alle")
        
        # Gestisci la presenza opzionale della location
        location = o.get("location", "Luogo non specificato")
        if location == "Null":
            location = "un luogo non specificato"
        else:
            location = location.replace("-","")
        
        formatted_orari.append(f"{o['day']} {timings} presso {location}")

    # Gestisci il caso in cui tutti gli orari siano stati saltati
    if not formatted_orari:
        return "Orari di ricevimento non disponibili."

    return ", ".join(formatted_orari)

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

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)