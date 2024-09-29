from transformers import GPT2LMHeadModel, GPT2Tokenizer, BertTokenizer, BertForSequenceClassification
import torch
import json

# Carica il file JSON preprocessato
with open('python_scraper/json/preprocessed_data.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Carica il modello GPT-2 e il tokenizer
model_gpt2 = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained('gpt2')

# Aggiungi il token di padding (usando il token di fine sequenza come padding)
tokenizer_gpt2.pad_token = tokenizer_gpt2.eos_token

# Carica il modello BERT addestrato e il tokenizer
tokenizer_bert = BertTokenizer.from_pretrained('bert-base-uncased')
model_bert = BertForSequenceClassification.from_pretrained('python_scraper/json/results/checkpoint-576')

# Funzione per classificare l'intento della domanda con BERT
def classify_intent(question):
    inputs = tokenizer_bert(question, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model_bert(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    intent_label = predictions.item()

    # Mappa l'intento alla classe corrispondente
    intent_map = {0: 'domanda_su_corsi', 1: 'domanda_su_orari_ricevimento', 2: 'domanda_su_contatti'}
    return intent_map[intent_label]

# Funzione per generare una risposta con GPT-2 con contesto strutturato
def generate_response_with_control(context):
    # Forniamo a GPT-2 un contesto più strutturato e chiaro
    structured_context = f"Rispondi alla domanda basata su queste informazioni: {context}."

    inputs = tokenizer_gpt2(structured_context, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model_gpt2.generate(
        inputs['input_ids'], 
        attention_mask=inputs['attention_mask'],
        max_length=150, 
        num_return_sequences=1, 
        do_sample=True, 
        temperature=0.7,  
        top_k=50,         
        top_p=0.9,        
        pad_token_id=tokenizer_gpt2.eos_token_id
    )
    
    generated_text = tokenizer_gpt2.decode(outputs[0], skip_special_tokens=True)
    
    return generated_text

# Funzione per recuperare le informazioni dal dataset JSON
def retrieve_info(docente_name, intent):
    docente = next((d for d in dataset if d['nome'].lower() == docente_name.lower()), None)
    
    if not docente:
        return f"Non ho trovato informazioni per il docente {docente_name}."
    
    if intent == 'domanda_su_corsi':
        if docente['corsi'] == 'Corsi non disponibili':
            return f"Non ho informazioni sui corsi di {docente['nome']}."
        else:
            return f"{docente['nome']} insegna i seguenti corsi: {docente['corsi']}."
    elif intent == 'domanda_su_orari_ricevimento':
        if docente['orari_ricevimento'] == 'Orari di ricevimento non disponibili':
            return f"Non ho informazioni sugli orari di ricevimento di {docente['nome']}."
        else:
            return f"Gli orari di ricevimento di {docente['nome']} sono: {docente['orari_ricevimento']}."
    elif intent == 'domanda_su_contatti':
        return f"Puoi contattare {docente['nome']} via email all'indirizzo: {docente['email']}."
    else:
        return "Mi dispiace, non capisco la tua domanda."

# Funzione per estrarre il nome del docente
def extract_docente_name(question):
    for docente in dataset:
        if docente['nome'].lower() in question.lower():
            return docente['nome']
    return None

def ask_question(question):
    # Classifica l'intento usando BERT
    intent = classify_intent(question)
    
    # Estrai il nome del docente dalla domanda
    docente_name = extract_docente_name(question)
    
    if not docente_name:
        return "Non ho capito il nome del docente."

    # Recupera le informazioni dal dataset JSON
    info = retrieve_info(docente_name, intent)
    
    # Genera una risposta utilizzando GPT-2 basata sulle informazioni recuperate
    response = generate_response_with_control(info)
    return response

# Esempio di domanda
question = "Quali corsi insegna la professoressa Rosalba Zizza?"

# Genera la risposta
response = ask_question(question)
print(response)
