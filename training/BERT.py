import json
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import torch

# Carica il file JSON preprocessato
with open('python_scraper/json/preprocessed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Funzione per creare frasi e labels
def create_texts_and_labels(data):
    labels_map = {'domanda_su_corsi': 0, 'domanda_su_orari_ricevimento': 1, 'domanda_su_contatti': 2}
    texts = []
    labels = []

    for docente in data:
        nome = docente['nome']
        
        # Creiamo frasi per ogni intento
        texts.append(f"Quali corsi insegna {nome}?")
        labels.append(labels_map['domanda_su_corsi'])
        
        texts.append(f"Quali sono gli orari di ricevimento di {nome}?")
        labels.append(labels_map['domanda_su_orari_ricevimento'])
        
        texts.append(f"Come posso contattare {nome}?")
        labels.append(labels_map['domanda_su_contatti'])
    
    return texts, labels

# Crea frasi e labels dal dataset preprocessato
texts, labels = create_texts_and_labels(data)

# Dividi il dataset in training e evaluation set (80% addestramento, 20% valutazione)
texts_train, texts_eval, labels_train, labels_eval = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Tokenizer BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenizza i dati di addestramento e valutazione
train_encodings = tokenizer(texts_train, return_tensors='pt', padding=True, truncation=True, max_length=128)
eval_encodings = tokenizer(texts_eval, return_tensors='pt', padding=True, truncation=True, max_length=128)

# Convertiamo le etichette in tensori
train_labels_tensor = torch.tensor(labels_train)
eval_labels_tensor = torch.tensor(labels_eval)

# Creiamo un dataset personalizzato per l'addestramento
class CustomDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

# Creiamo i dataset
train_dataset = CustomDataset(train_encodings, train_labels_tensor)
eval_dataset = CustomDataset(eval_encodings, eval_labels_tensor)

# Modello BERT per la classificazione
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    evaluation_strategy="steps"  # Valutazione periodica durante l'addestramento
)

# Creazione del Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,  # Dataset di addestramento
    eval_dataset=eval_dataset     # Dataset di valutazione
)

# Avvia l'addestramento
trainer.train()

# Valutazione del modello
trainer.evaluate()
