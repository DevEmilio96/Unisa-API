from bs4 import BeautifulSoup
import requests
import time
import json

def clean_scheda_and_links(data):
    for corso in data['corsi']:
        # Rimuovi "orari_lezioni_link" se contiene "N/A"
        if 'orari_lezioni_link' in corso and "N/A" in corso['orari_lezioni_link']:
            del corso['orari_lezioni_link']

        # Continua con la logica precedente per pulire "scheda"
        if 'scheda' in corso:
            keys_to_delete = [key for key, value in corso['scheda'].items() if "N/A" in value]
            for key in keys_to_delete:
                del corso['scheda'][key]
            if not corso['scheda']:
                del corso['scheda']
    return data

def clean_json_file(file_path):
    # Legge il file JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Assicurati che json_data sia una lista prima di iterare
    if isinstance(json_data, list):
        cleaned_json_data = [clean_scheda_and_links(item) for item in json_data]
    else:
        # Se json_data non è una lista, applica direttamente clean_scheda_and_links
        cleaned_json_data = clean_scheda_and_links(json_data)

    # Sovrascrive il file JSON con i dati puliti
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(cleaned_json_data, file, indent=4, ensure_ascii=False)

def get_course_details(didattica_soup, base_url="https://docenti.unisa.it"):
    courses_details = []

    course_panels = didattica_soup.find_all('div', class_='panel')

    for panel in course_panels:
        course_link_tag = panel.find('a')
        if course_link_tag:  # Verifica che l'elemento esista
            course_name = course_link_tag.text.strip()
            course_link = base_url + course_link_tag['href']
        else:
            course_name = "N/A"
            course_link = "N/A"

        course_code_tag = panel.find('small', class_='badge')
        course_code = course_code_tag.text.strip() if course_code_tag else "N/A"

        course_details = {'name': course_name, 'code': course_code, 'details_link': course_link, 'scheda': {}}

        response = requests.get(course_link, verify=False)
        course_soup = BeautifulSoup(response.text, 'html.parser')

        scheda_div = course_soup.find(id="insegnamento-collapse-4a")
        if scheda_div:
            tables = scheda_div.find_all('table')
            for table in tables:
                section_th = table.find('th', class_='icon')
                if section_th and section_th.find_next_sibling('th'):  # Aggiunto controllo aggiuntivo qui
                    section_title = section_th.find_next_sibling('th').text.strip()
                    contents = []
                    rows = table.find_all('tr')[1:]  # Salta la riga del titolo
                    for row in rows:
                        for br in row.find_all('br'):
                            br.replace_with("\n")
                        content_td = row.find('td', class_='text-justify')
                        content = content_td.text.strip() if content_td else "N/A"
                        contents.append(content)
                    course_details['scheda'][section_title] = "\n".join(contents)
                    
        # Cerca il link agli orari delle lezioni
        orari_lezioni_tag = course_soup.find('a', class_='btn btn-success', href=True)
        if orari_lezioni_tag and 'orari' in orari_lezioni_tag['href']:
            orari_lezioni_link = base_url + '/' + orari_lezioni_tag['href']
            course_details['orari_lezioni_link'] = orari_lezioni_link
        else:
            course_details['orari_lezioni_link'] = "N/A"

        
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