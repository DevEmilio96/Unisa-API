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
