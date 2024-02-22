from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time 

def getUrlDocenti():
    # Configura il WebDriver con webdriver_manager
    service = ChromeService(ChromeDriverManager().install())
    
    # Configura le opzioni per il browser Chrome in modalità headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Creare un oggetto WebDriver con le opzioni configurate
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Apri la pagina web con Selenium
    driver.get('https://docenti.unisa.it/home')
    try:
        # Attendi il caricamento dell'elemento di input
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'filter'))
        )

        # Inserisci "Dipartimento di Informatica" nel campo di ricerca
        search_input.send_keys('Dipartimento di Informatica')

        # Attendi l'aggiornamento automatico della pagina in base al testo inserito
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr[style="display: table-row;"]'))
        )

        # Trova tutti gli elementi link nella struttura specificata
        links = driver.find_elements(By.CSS_SELECTOR, 'tr[style="display: table-row;"] a')

        # Estrai gli attributi href
        urls = [link.get_attribute('href') for link in links]
        
        
    finally:
        # Pulisci chiudendo il browser
        driver.quit()
        return urls
