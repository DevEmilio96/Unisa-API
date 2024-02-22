import requests
from bs4 import BeautifulSoup
import time
import warnings
from collections import deque
import python_scraper.functions.getUrlDocenti as getUrlDocenti

# Import delle funzioni personalizzate
from functions.didattica import *
from functions.writers import *
from functions.general_prof_info import *
from functions.corsiDiLaurea import estrai_informazioni_corsi
# Ignora tutti i warning
warnings.filterwarnings("ignore")

def estrai_dati_professore(url_professore):
    try:
        # Esegue una richiesta alla pagina del professore
        response = requests.get(url_professore, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Estrazione dei dati dalla pagina utilizzando selettori adeguati
        nome = soup.find('h1', id='rescue-title').find('span', class_='hidden-xs').text.strip().replace(" |", "")
        titolo = analize_icon(soup, "glyphicon glyphicon-user")  # Estrazione del titolo
        dipartimento = analize_icon(soup, "glyphicon glyphicon-home")  # Estrazione del dipartimento
        telefono = analize_icon(soup, "glyphicon glyphicon-earphone")  # Estrazione del telefono
        email = analize_icon(soup, "glyphicon glyphicon-envelope")  # Estrazione dell'email
        ufficio = analize_icon(soup, "glyphicon glyphicon-map-marker")  # Estrazione dell'ufficio
        personalPageUrl = analize_icon(soup, "fa fa-link")  # Estrazione della pagina personale
        orari_di_ricevimento = analize_icon(soup, "fa fa-calendar")  # Estrazione degli orari di ricevimento
        url_immagine_professore = getImgUrl(soup)  # Estrazione dell'URL dell'immagine del professore
        corsi = search_courses(soup)  # Estrazione dei corsi
        
        url_professore = url_professore
        error = False
    except Exception as e:
        print(f"Errore durante l'elaborazione di {url_professore}: {e}")
        # In caso di errore, assegna valori 'Null' e imposta 'error' a True
        nome = "Null" 
        titolo = "Null" 
        dipartimento = "Null"  
        telefono = "Null"  
        email = "Null"  
        ufficio = "Null"  
        personalPageUrl = "Null"
        orari_di_ricevimento = "Null"
        corsi = "Null"
        url_professore = url_professore
        url_immagine_professore = ""
        error = True

    # Crea un dizionario con i dati estratti
    dati_professore = {
        'nome': nome,
        'titolo': titolo,
        'dipartimento': dipartimento,
        'telefono': telefono,
        'email': email,
        'ufficio': ufficio,
        'pagina_personale' : personalPageUrl,
        'orari_di_ricevimento' : orari_di_ricevimento,
        'corsi' : corsi,
        'url' : url_professore,
        'url_immagine_professore' : url_immagine_professore,
        'error' : error
    }
    
    return dati_professore

# Ottieni i link dei professori
links_professori = getUrlDocenti.getUrlDocenti()

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
write_professors_json(dati_professori, "json/db.json")
estrai_informazioni_corsi("json/degree_courses.json")