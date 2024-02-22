import time
import warnings
from collections import deque

# Import delle funzioni personalizzate
from functions.getUrlDocenti import getUrlDocenti
from functions.didattica import *
from functions.writers import *
from functions.general_prof_info import *
from functions.corsiDiLaurea import estrai_informazioni_corsi

# Ignora tutti i warning
warnings.filterwarnings("ignore")

# Ottieni i link dei professori
links_professori = getUrlDocenti()

# Lista per salvare i dati dei professori
dati_professori = []

# Limita il numero di link per il test
links_professori = links_professori[:3]

# Converti l'elenco dei link in una deque (coda doppia) che funge da stack
stack_links = deque(links_professori)

while stack_links:
    url_professore = stack_links.pop()
    try:
        print(f"Elaborazione di {url_professore}")
        dati_professore = estrai_dati_professore(url_professore)
        if dati_professore.get('error', False):
            # Se c'è stato un errore, rimetti l'URL nello stack
            print(f"Riprovo più tardi: {url_professore}")
            stack_links.appendleft(url_professore)
        else:
            dati_professori.append(dati_professore)
    except Exception as e:
        print(f"Errore durante l'elaborazione di {url_professore}: {e}")
        # Rimetti l'URL nello stack per riprovare
        stack_links.appendleft(url_professore)
    finally:
        # Aspetta per evitare di sovraccaricare il server
        time.sleep(1)

# Scrivi i dati dei professori in formato JSON
print("\n----------------Creo il json con i dati dei professori e dei corsi----------------")
#write_professors_json(dati_professori)


print("\n----------------Creo il json con le offerte formative relative ai corsi di laurea----------------\n")
estrai_informazioni_corsi()
print("\n----------------Json creato correttamente----------------\n")