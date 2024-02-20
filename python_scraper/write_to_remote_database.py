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
                # Esecuzione della query per scrivere i dati del professore nel database
                sql_professor = "INSERT INTO teachers (id, name, title, department, email, office, personal_webpage, url, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values_professor = (id, prof['nome'], prof['titolo'], prof['dipartimento'], prof['email'], prof['ufficio'], prof['pagina_personale'], prof['url'], prof['url_immagine_professore'])
                cursor.execute(sql_professor, values_professor)
                
                # Esecuzione della query per scrivere i dati dei corsi del professore nel database
                
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
