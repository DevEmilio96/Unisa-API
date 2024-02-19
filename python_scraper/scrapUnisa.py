import ast
import requests
from bs4 import BeautifulSoup
import csv
import time
import warnings
from collections import deque
import getUrlDocenti
import json

# Ignora tutti i warning
warnings.filterwarnings("ignore")
def getImgUrl(soup):
    img_link_element = soup.find('img', id='rescue-structure-img')
    if img_link_element:
        img = img_link_element.get('data-original')
        img = "https://docenti.unisa.it" + img[1:]
        return img
    else:
        return None



def get_course_details(didattica_soup):
    # Crea una lista per contenere i dettagli dei corsi
    courses_details = []

    # Trova tutti i pannelli dei corsi
    course_panels = didattica_soup.find_all('div', class_='panel')

    for panel in course_panels:
        # Trova il nome del corso all'interno del pannello
        course_name  = panel.find('a').text.strip()

        # Trova il codice del corso, che potrebbe essere in un <small> tag o in un altro elemento
        course_code = panel.find('small', class_='badge').text.strip()

        # Crea un dizionario per i dettagli del corso
        course_details = {'name': course_name, 'code': course_code}

        # Estrai altre informazioni dalla tabella se necessario
        # Ad esempio, estrarre il dipartimento e il tipo di corso
        table_rows = panel.find('table').find_all('tr')
        for row in table_rows:
            cells = row.find_all('td')
            if len(cells) > 1 and cells[0].get('class', [''])[0] == 'icon':
                icon_class = cells[0].find('span').get('class', [''])[1]
                if 'fa-home' in icon_class:
                    course_details['department'] = cells[1].text.strip()
                elif 'fa-graduation-cap' in icon_class:
                    course_details['degree'] = cells[1].text.strip()
                # Aggiungi qui ulteriori campi se necessario

        # Aggiungi i dettagli del corso alla lista dei corsi
        courses_details.append(course_details)

    return courses_details

def search_courses(soup):
    didattica_link_element = soup.select_one('div#side-menu a[href$="didattica"]')
    if didattica_link_element:
        didattica_link = didattica_link_element.get('href')
        print(f"didattica : {didattica_link}")

        while True:  # Ciclo infinito
            try:
                didattica_response = requests.get(didattica_link, verify=False, timeout=10)

                if didattica_response.status_code == 200:
                    # Analizza la pagina Didattica
                    didattica_soup = BeautifulSoup(didattica_response.text, 'html.parser')
                    
                    # Estrai i dettagli dei corsi
                    courses_details = get_course_details(didattica_soup)
                    return courses_details  # Restituisce i dettagli dei corsi se la richiesta ha avuto successo

            except requests.RequestException as e:
                print(f"Errore durante la richiesta: {e}. Tentativo di nuova connessione.")

            time.sleep(5)  # Attesa di 5 secondi tra i tentativi

            
    
    return  courses_details

def analize_icon(parser, icon):
    results = []

    icons_td = parser.find_all('span', class_=icon)  # Trova tutte le icone
    if icon == "fa fa-calendar":
        icons_td = parser.find_all('i', class_=icon)  # Trova tutte le icone
        if not icons_td :
            result = {'day': "Null",'timings': "Null",'location':"Null"}
            results.append(result)
            return results
        
    

    for icon_td in icons_td:
        icon_td = icon_td.find_parent('td')  # Trova il genitore 'td' dell'icona
        professor_td = icon_td.find_next_sibling('td')  # Vai al prossimo 'td'
        if icon =="fa fa-link":
            a_element = professor_td.find('a')  # Trova l'elemento <a> all'interno del <td>
            result = a_element.get("href")  # Ottieni l'attributo href dell'elemento <a>
        elif icon =="fa fa-calendar":
            tr_element = icon_td.find_parent('tr')  # Trova l'elemento 'tr' che contiene i dati del ricevimento
            if tr_element:
                td_elements = tr_element.find_all('td')  # Trova tutti gli elementi 'td' all'interno del 'tr'
                
                # Estrai i dati del ricevimento (considerando che ci possono essere più orari)
                day = td_elements[1].find('strong').text.strip()
                timings = td_elements[2].find('strong').text.strip()
                location = td_elements[3].text.strip()
                
                result = {
                    'day': day if day else "Null",
                    'timings': timings if timings else "Null",
                    'location': location if location else "Null"
                }

        else:  
            result = professor_td.text.strip() if professor_td else "Null"
        
        if icon == "glyphicon glyphicon-earphone" and not result.startswith("089 96"):
            continue
        results.append(result)

    if icon =="fa fa-calendar":
        return results
    
    if not results:
        return "Null"  # Se non viene trovata alcuna icona, restituisce una stringa "Null"
    elif len(results) == 1:
        return results[0]  # Se viene trovata una sola icona, restituisce la stringa singola
    else:
        unique_results = list(set(results))  # Rimuovi i duplicati dagli array
        #unique_results = results
        if len(unique_results) == 1:
            return unique_results[0]   
        return unique_results  # Restituisce l'array di stringhe senza duplicati


def estrai_dati_professore(url_professore):
    try:
        # Esegue una richiesta alla pagina del professore
        response = requests.get(url_professore, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Seleziona i dati dal layout della pagina, usando i selettori appropriati
        nome = soup.find('h1', id='rescue-title').find('span', class_='hidden-xs').text.strip()
        # Titolo
        titolo = analize_icon(soup,"glyphicon glyphicon-user")
        # Dipartimento
        dipartimento = analize_icon(soup,"glyphicon glyphicon-home")
        # Telefono
        telefono = analize_icon(soup,"glyphicon glyphicon-earphone")
        # Email
        email = analize_icon(soup,"glyphicon glyphicon-envelope")
        # Ufficio
        ufficio = analize_icon(soup,"glyphicon glyphicon-map-marker")
        # Pagina Personale
        personalPageUrl = analize_icon(soup,"fa fa-link")
        # Orari di Ricevimento
        orari_di_ricevimento = analize_icon(soup,"fa fa-calendar")
       # Url Immagine Professore
        url_immagine_professore = getImgUrl(soup)
        # Corsi
        corsi = search_courses(soup)

        url_professore = url_professore
        error = False
    except Exception as e:
        print(f"Errore durante l'elaborazione di {url_professore}: {e}")
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

    


    # Crea un dizionario con i dati
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


# URL della pagina principale del collegio dei docenti
#url_collegio_docenti = 'https://corsi.unisa.it/88601/collegio-dei-docenti'

# Richiesta HTTP alla pagina principale
#response = requests.get(url_collegio_docenti, verify=False)
#soup = BeautifulSoup(response.text, 'html.parser')

# Trova tutti i link dei professori (modifica il selettore in base alla struttura della pagina)
#links_professori = soup.select('div.clearfix ul li.text-justify a')
# Elimina Duplicati
#links_unici = set(link.get('href') for link in links_professori)  # Converti in set per rimuovere i duplicati
#links_professori = list(links_unici)  # Converti nuovamente in lista per l'iterazione

links_professori = getUrlDocenti.getUrlDocenti()
# Lista per salvare i dati
dati_professori = []

#split array for test
#links_professori = links_professori[:3]
# Converti l'elenco dei link in una deque (coda doppia) che funge da stack
stack_links = deque(links_professori)

# Lista per salvare i dati
dati_professori = []

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
##################################################################################################################################

# Scrivi la stringa JSON in un file
with open('db.json', 'w') as json_file:
    json_file.write('[')  # Inizia con una parentesi quadra aperta
    for index, professore in enumerate(dati_professori):
        # Trasforma ciascun oggetto in una stringa JSON e scrivilo nel file
        json_string = json.dumps(professore, indent=4)
        json_file.write(json_string)
        if index < len(dati_professori) - 1:
            json_file.write(',')  # Aggiungi una virgola se non è l'ultimo oggetto
    json_file.write(']')

def write_professors_csv(professors_data, filename='csv/professori.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Intestazioni del CSV dei professori
        writer.writerow(['id', 'nome', 'titolo', 'dipartimento', 'email', 'ufficio', 'pagina_personale', 'url', 'url_immagine_professore'])
        for id, prof in enumerate(professors_data, start=1):
            writer.writerow([id, prof['nome'], prof['titolo'], prof['dipartimento'], prof['email'], prof['ufficio'], prof['pagina_personale'], prof['url'], prof['url_immagine_professore']])

def write_courses_csv(professors_data, filename='csv/corsi.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Intestazioni del CSV dei corsi
        writer.writerow(['id_professore', 'nome', 'codice', 'dipartimento', 'laurea'])
        for id, prof in enumerate(professors_data, start=1):
            for corso in prof['corsi']:
                writer.writerow([id, corso["name"], corso["code"], corso["department"], corso["degree"]])

def write_phone_csv(professors_data, filename='csv/phone.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Intestazioni del CSV dei corsi
        writer.writerow(['id_professore', 'tel'])
        for id, prof in enumerate(professors_data, start=1):
            if isinstance(prof['telefono'], str):
                if prof['telefono'] == "Null" : continue
                writer.writerow([id, prof['telefono']])

            if isinstance(prof['telefono'], list):
                for telefono in prof['telefono']:
                    writer.writerow([id, telefono])      


def write_reception_hours_csv(professors_data, filename='csv/orari_di_ricevimento.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Intestazioni del CSV degli orari di ricevimento
        writer.writerow(['id_professore', 'giorno', 'orario', 'luogo'])
        for id, prof in enumerate(professors_data, start=1):
            for orario in prof['orari_di_ricevimento']:
                # Controllo sulla lunghezza della tupla
                if orario["day"]!= "Null":
                    giorno = orario["day"]
                    timings = orario["timings"]
                    luogo = orario["location"]

                    writer.writerow([id, giorno, timings, luogo])

# Supponendo che 'dati_professori' sia la lista dei dati dei professori
write_professors_csv(dati_professori)
write_courses_csv(dati_professori)
write_reception_hours_csv(dati_professori)
write_phone_csv(dati_professori)

