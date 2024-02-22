
from functions.didattica import *

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

def getImgUrl(soup):
    img_link_element = soup.find('img', id='rescue-structure-img')
    if img_link_element:
        img = img_link_element.get('data-original')
        img = "https://docenti.unisa.it" + img[1:]
        return img
    else:
        return None




def analize_icon(parser, icon):
    results = []

    icons_td = parser.find_all('span', class_=icon)  # Trova tutte le icone
    if icon == "fa fa-calendar":
        icons_td = parser.find_all('i', class_=icon)  # Trova tutte le icone
        if not icons_td:
            result = {'day': "Null", 'timings': "Null", 'location': "Null"}
            results.append(result)
            return results

    for icon_td in icons_td:
        icon_td = icon_td.find_parent('td')  # Trova il genitore 'td' dell'icona
        professor_td = icon_td.find_next_sibling('td')  # Vai al prossimo 'td'
        if icon == "fa fa-link":
            a_element = professor_td.find('a')  # Trova l'elemento <a> all'interno del <td>
            result = a_element.get("href")  # Ottieni l'attributo href dell'elemento <a>
        elif icon == "fa fa-calendar":
            tr_element = icon_td.find_parent('tr')  # Trova l'elemento 'tr' che contiene i dati del ricevimento
            if tr_element:
                td_elements = tr_element.find_all('td')  # Trova tutti gli elementi 'td' all'interno del 'tr'
                
                # Estrai i dati del ricevimento (considerando che ci possono essere più orari)
                day = clean_text(td_elements[1].find('strong').text)
                timings = clean_text(td_elements[2].find('strong').text)
                location = clean_text(td_elements[3].text)
                
                result = {
                    'day': day if day else "Null",
                    'timings': timings if timings else "Null",
                    'location': location if location else "Null"
                }
        else:
            result = clean_text(professor_td.text) if professor_td else "Null"

        if icon == "glyphicon glyphicon-earphone":
            # Formatta il numero di telefono
            result = format_phone_number(result)
            if not result.startswith("089 96"):
                continue

        results.append(result)

    if icon == "fa fa-calendar":
        return results

    if not results:
        return "Null"
    elif len(results) == 1:
        return results[0]
    else:
        unique_results = list(set(results))
        if len(unique_results) == 1:
            return unique_results[0]
        return unique_results

def clean_text(text):
    """Sostituisce i tag <br> trovati nel testo con uno spazio."""
    cleaned_text = text.replace('<br>', ' ')
    return ' '.join(cleaned_text.split())

def format_phone_number(phone_number):
    """Formatta il numero di telefono nel formato desiderato."""
    # Rimuovi caratteri non numerici
    phone_number = phone_number.replace(" ", "")
    digits = ''.join(filter(str.isdigit, phone_number))
    # Assicurati che la lunghezza dei numeri sia quella attesa (10 cifre)
    if len(digits) == 9:
        # Formatta secondo il pattern desiderato
        formatted = f"{digits[0:3]} {digits[3:5]} {digits[5:7]} {digits[7:10]}"
    else:
        # Restituisci il numero originale se non corrisponde alla lunghezza attesa
        formatted = phone_number
    return formatted

