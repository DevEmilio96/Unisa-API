import csv
import json
import pymysql

# Scrivi la stringa JSON in un file
def write_professors_json(professors_data, location = "json/db.json"):
    with open(location, 'w') as json_file:
        json_file.write('[')  # Inizia con una parentesi quadra aperta
        for index, professore in enumerate(professors_data):
            # Trasforma ciascun oggetto in una stringa JSON e scrivilo nel file
            json_string = json.dumps(professore, indent=4)
            json_file.write(json_string)
            if index < len(professors_data) - 1:
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


def write_to_remote_database(professors_data):
    # Connessione al database remoto
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='unisa_api'
    )

    try:
        with connection.cursor() as cursor:
            # Inizio della transazione
            connection.begin()
            
            for id, prof in enumerate(professors_data, start=1):
                # teachers
                sql_professor = "INSERT INTO teachers (id, name, title, department, email, office, personal_webpage, url, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values_professor = (id, prof['nome'], prof['titolo'], prof['dipartimento'], prof['email'], prof['ufficio'], prof['pagina_personale'], prof['url'], prof['url_immagine_professore'])
                cursor.execute(sql_professor, values_professor)

                # phone_contacts
                if isinstance(prof['telefono'], str):
                    if prof['telefono'] == "Null" : continue
                    sql_course = "INSERT INTO phone_contacts (id_professore, tel) VALUES (%s, %s)"
                    values_course = (id, prof['telefono'])
                    cursor.execute(sql_course, values_course)

                if isinstance(prof['telefono'], list):
                    for telefono in prof['telefono']:
                        sql_course = "INSERT INTO phone_contacts (id_professore, tel) VALUES (%s, %s)"
                        values_course = (id, telefono)
                        cursor.execute(sql_course, values_course)
                
                # reception_hours
                for orario in prof['orari_di_ricevimento']:
                # Controllo sulla lunghezza della tupla
                    if orario["day"]!= "Null":
                        giorno = orario["day"]
                        timings = orario["timings"]
                        luogo = orario["location"]
                        
                        sql_course = "INSERT INTO reception_hours (id_professore, day, hours, location) VALUES (%s, %s, %s, %s)"
                        values_course = (id, giorno, timings, luogo)
                        cursor.execute(sql_course, values_course)
                
                # courses
                for corso in prof['corsi']:
                    sql_course = "INSERT INTO courses (id_professore, name, code, department, degree) VALUES (%s, %s, %s, %s, %s)"
                    values_course = (id, corso["name"], corso["code"], corso["department"], corso["degree"])
                    cursor.execute(sql_course, values_course)
            
            # Commit delle modifiche
            connection.commit()
    
    except:
        # Rollback in caso di errore
        connection.rollback()
        raise
    
    finally:
        # Chiusura della connessione al database
        connection.close()
