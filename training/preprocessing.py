import json

# Carica i file JSON
with open('training/json/db.json', 'r', encoding='utf-8') as f:
    data_docenti = json.load(f)

with open('training/json/degree_courses.json', 'r', encoding='utf-8') as f:
    data_corsi = json.load(f)

# Funzione per il preprocessing dei dati dei docenti
def preprocess_docenti(docenti_data):
    processed_docenti = []
    
    for docente in docenti_data:
        # Estrai le informazioni principali del docente
        nome = docente.get('nome', 'Informazione non disponibile')
        titolo = docente.get('titolo', 'Informazione non disponibile')
        dipartimento = docente.get('dipartimento', 'Informazione non disponibile')
        email = docente.get('email', 'Informazione non disponibile')
        corsi_docente = docente.get('corsi', [])
        orari_ricevimento = docente.get('orari_di_ricevimento', [])
        
        # Gestisci il caso in cui non ci sono corsi del docente
        corsi_text = 'Corsi non disponibili' if not corsi_docente else ', '.join([corso['name'] for corso in corsi_docente])
        
        # Gestisci il caso in cui non ci sono orari di ricevimento
        orari_text = 'Orari di ricevimento non disponibili' if not orari_ricevimento else ', '.join([f"{orario['day']}: {orario['timings']}" for orario in orari_ricevimento if orario['day'] != 'Null'])

        # Creiamo una frase riassuntiva per ogni docente
        docente_info = {
            "nome": nome,
            "titolo": titolo,
            "dipartimento": dipartimento,
            "email": email,
            "corsi_docente": corsi_text,
            "orari_ricevimento": orari_text
        }
        
        # Aggiungi al dataset preprocessato
        processed_docenti.append(docente_info)

    return processed_docenti

# Funzione per il preprocessing dei dati dei corsi di laurea
def preprocess_corsi(corsi_data):
    processed_corsi = []
    
    for corso in corsi_data:
        nome_corso = corso.get('nome', 'Informazione non disponibile')
        link_corso = corso.get('link', 'Link non disponibile')
        piano_di_studi = corso.get('piano_di_studi', [])
        
        # Gestisci il caso in cui non ci sono piani di studi
        piani_studi_text = 'Piani di studi non disponibili' if not piano_di_studi else ', '.join([f"{p['anno_accademico']}: {p['url']}" for p in piano_di_studi])

        # Creiamo una frase riassuntiva per ogni corso di laurea
        corso_info = {
            "nome_corso": nome_corso,
            "link_corso": link_corso,
            "piani_di_studi": piani_studi_text
        }
        
        # Aggiungi al dataset preprocessato
        processed_corsi.append(corso_info)

    return processed_corsi

# Preprocessa i dati dei docenti e dei corsi
processed_docenti = preprocess_docenti(data_docenti)
processed_corsi = preprocess_corsi(data_corsi)

# Salva i dati preprocessati in file JSON separati
with open('training/json/preprocessed_docenti.json', 'w', encoding='utf-8') as f:
    json.dump(processed_docenti, f, ensure_ascii=False, indent=4)

with open('training/json/preprocessed_corsi.json', 'w', encoding='utf-8') as f:
    json.dump(processed_corsi, f, ensure_ascii=False, indent=4)

print("Preprocessing completato: i dati sono stati salvati nei file 'preprocessed_docenti.json' e 'preprocessed_corsi.json'.")
