import spacy
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json

# Carica il modello di lingua italiana di spaCy
nlp = spacy.load('it_core_news_lg')

# Carica i file JSON preprocessati
with open('training/json/preprocessed_docenti.json', 'r', encoding='utf-8') as f:
    dataset_docenti = json.load(f)

with open('training/json/preprocessed_corsi.json', 'r', encoding='utf-8') as f:
    dataset_corsi = json.load(f)

# Carica il modello BERT addestrato e il tokenizer
tokenizer_bert = BertTokenizer.from_pretrained('bert-base-uncased')
model_bert = BertForSequenceClassification.from_pretrained('training/json/results/checkpoint-603')

# Funzione per classificare l'intento della domanda con BERT
def classify_intent(question):
    inputs = tokenizer_bert(question, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model_bert(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    intent_label = predictions.item()

    # Mappa l'intento alla classe corrispondente
    intent_map = {
        0: 'domanda_su_corsi', 
        1: 'domanda_su_orari_ricevimento', 
        2: 'domanda_su_contatti', 
        3: 'domanda_su_corso_laurea', 
        4: 'domanda_su_piano_studi'
    }
    return intent_map[intent_label]

# Funzione per estrarre i nomi di persona dalla domanda usando spaCy
def extract_person_names(question):
    doc = nlp(question)
    person_names = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    return person_names

# Funzione per estrarre il nome del dipartimento dalla domanda
def extract_dipartimento(question):
    for corso in dataset_corsi:
        if corso['nome_corso'].lower() in question.lower():
            return corso['nome_corso']
    return None

# Funzione per recuperare le informazioni sui docenti dal dataset JSON
def retrieve_info_docenti(docente_name, intent):
    docente = next((d for d in dataset_docenti if docente_name.lower() in d['nome'].lower()), None)
    
    if not docente:
        return f"Non ho trovato informazioni per il docente {docente_name}."
    
    if intent == 'domanda_su_corsi':
        if docente['corsi_docente'] == 'Corsi non disponibili':
            return f"Non ho informazioni sui corsi di {docente['nome']}."
        else:
            return f"{docente['nome']} insegna i seguenti corsi: {docente['corsi_docente']}."
    elif intent == 'domanda_su_orari_ricevimento':
        if docente['orari_ricevimento'] == 'Orari di ricevimento non disponibili':
            return f"Non ho informazioni sugli orari di ricevimento di {docente['nome']}."
        else:
            return f"Gli orari di ricevimento di {docente['nome']} sono: {docente['orari_ricevimento']}."
    elif intent == 'domanda_su_contatti':
        return f"Puoi contattare {docente['nome']} via email all'indirizzo: {docente['email']}."
    else:
        return "Mi dispiace, non capisco la tua domanda."

# Funzione per recuperare le informazioni sui corsi dal dataset JSON
def retrieve_info_corsi(dipartimento, intent):
    corso = next((c for c in dataset_corsi if c['nome_corso'].lower() == dipartimento.lower()), None)
    
    if not corso:
        return f"Non ho trovato informazioni per il corso di laurea {dipartimento}."
    
    if intent == 'domanda_su_corso_laurea':
        return f"Il corso di laurea in {corso['nome_corso']} ha il seguente piano di studi: {corso['piani_di_studi']}."
    elif intent == 'domanda_su_piano_studi':
        return f"Ecco il piano di studi aggiornato per {corso['nome_corso']}: {corso['piani_di_studi']}."
    else:
        return "Mi dispiace, non capisco la tua domanda."

# Funzione principale per rispondere alle domande
def ask_question(question):
    # Classifica l'intento usando BERT
    intent = classify_intent(question)
    
    # Estrai il nome del docente usando spaCy
    person_names = extract_person_names(question)
    
    if person_names:
        docente_name = person_names[0]  # Prendi il primo nome trovato, se c'è
        info = retrieve_info_docenti(docente_name, intent)
    else:
        # Se non c'è un nome di docente, cerca informazioni sui corsi di laurea
        dipartimento = extract_dipartimento(question)
        if dipartimento:
            info = retrieve_info_corsi(dipartimento, intent)
        else:
            return "Non ho capito il nome del docente o del dipartimento."

    return info

# Esempio di domanda
question1 = "Quali corsi insegna Zizza?"
question2 = "Qual è il piano di studi del corso di laurea in Chimica?"

# Genera le risposte
response1 = ask_question(question1)
response2 = ask_question(question2)

print(response1)
print(response2)
