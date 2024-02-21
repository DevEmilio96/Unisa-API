import pymysql

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
