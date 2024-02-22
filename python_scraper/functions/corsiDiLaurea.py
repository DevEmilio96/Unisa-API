import requests
from bs4 import BeautifulSoup
import time
import json
from itertools import cycle
import threading
import sys
import warnings

# Ignora tutti i warning
warnings.filterwarnings("ignore")

url_base = "https://web.unisa.it"

# Flag globale per gestire lo stato dell'animazione di caricamento
loading = True

# Funzione per mostrare un'animazione di caricamento
def animazione_caricamento(messaggio="Caricamento"):
    global loading
    for char in cycle('|/-\\'):
        if not loading:
            break
        status = f"\r{messaggio} {char}"
        sys.stdout.write(status)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(messaggio) + 2) + '\r')
    sys.stdout.flush()

def estrai_informazioni_corsi(location = "json/degree_courses.json", max_attempts=5, delay=5):
    global loading
    url_corsi = f"{url_base}/didattica/corsi-laurea"
    corsi_info = []
    retry_stack = []

    # Avvia l'animazione di caricamento in un thread separato
    t = threading.Thread(target=animazione_caricamento, args=("Sto estrapolando i dati",))
    t.start()

    try:
        response = requests.get(url_corsi, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\rPagina principale dei corsi caricata con successo.")
    except requests.exceptions.RequestException as e:
        print(f"\rErrore nella richiesta: {e}")
        loading = False
        t.join()
        return

    for a in soup.select('div.searchable td:not(.text-center) > a[href^="https://corsi.unisa.it"]'):
        nome_corso = a.text.strip()
        print(f"\rEstrapolando dati per il corso di laurea: {nome_corso}")
        link_corso_base = a.get('href').replace(" ", "")
        link_piano_di_studi = f"{link_corso_base}/didattica/piano-di-studi"

        corso_info, response_piano_di_studi = make_request_with_retry(link_piano_di_studi, nome_corso, max_attempts, delay)

        if response_piano_di_studi is not None:
            corsi_info.append(corso_info)
        else:
            retry_stack.append((corso_info, link_piano_di_studi))

    # Ferma l'animazione di caricamento
    loading = False
    t.join()

    if retry_stack:
        print("\nRiprova per i link falliti.")
        for corso_info, link in retry_stack:
            print(f"Riprova per: {corso_info['nome']}")
            _, response = make_request_with_retry(link, corso_info['nome'], max_attempts, delay)
            if response is not None:
                corsi_info.append(corso_info)
    
    with open(location, "w", encoding="utf-8") as file_json:
        json.dump(corsi_info, file_json, ensure_ascii=False, indent=4)

    print(f"\nInformazioni sui piani di studio salvate in '{location}'.")

def make_request_with_retry(url, nome_corso, max_attempts, delay):
    link_corso_base = url.replace("/didattica/piano-di-studi", "")
    corso_info = {"nome": nome_corso, "link": link_corso_base, "piano_di_studi": []}
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link_pdf in soup.select('a[href*="__piano-studi-cds"]'):
                    href_pdf = link_pdf.get('href')
                    if href_pdf:
                        pdf_full_url = f"{url_base}{href_pdf}" if href_pdf.startswith('/') else href_pdf
                        corso_info["piano_di_studi"].append({"url": pdf_full_url, "anno_accademico": link_pdf.text.strip()})
                return corso_info, response
            else:
                print(f"\rTentativo {attempt + 1} fallito per {nome_corso}")
        except requests.exceptions.RequestException as e:
            print(f"\rErrore nella richiesta a {nome_corso}: {e}")
        time.sleep(delay)
    print(f"\rMassimo numero di tentativi raggiunto per il corso {nome_corso}.")
    return corso_info, None

# Eseguire la funzione

