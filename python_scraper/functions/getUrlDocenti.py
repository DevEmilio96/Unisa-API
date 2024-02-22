import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def getUrlDocenti(popola_filtro=False, dipartimento="Dipartimento di Informatica"):
    urls = []

    if popola_filtro:
        # Configura il WebDriver con webdriver_manager
        service = ChromeService(ChromeDriverManager().install())
        
        # Configura le opzioni per il browser Chrome in modalità headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Creare un oggetto WebDriver con le opzioni configurate
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Apri la pagina web con Selenium
            driver.get('https://docenti.unisa.it/home')

            # Attendi il caricamento dell'elemento di input e inserisci il filtro
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'filter'))
            )
            search_input.send_keys(dipartimento)

            # Attendi l'aggiornamento automatico della pagina
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'tr[style="display: table-row;"]'))
            )

            # Trova tutti gli elementi link nella struttura specificata
            links = driver.find_elements(By.CSS_SELECTOR, 'tr[style="display: table-row;"] a')

            # Estrai gli attributi href
            urls = [link.get_attribute('href') for link in links]

        finally:
            driver.quit()

    else:
        # Usa requests e BeautifulSoup per ottenere e analizzare la pagina
        response = requests.get('https://docenti.unisa.it/home', verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Assumi che tutti i link che ti interessano siano dentro elementi 'a' in 'tr'
            # Modifica il selettore se necessario
            links = soup.select('tr a')
            urls = [link.get('href') for link in links if link.get('href')]
        print(f"il numero di url trovati è {len(urls)}")

    return urls
