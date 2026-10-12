import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv as caricaenv

caricaenv()

configuratore={
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}


def _connessione_aperta():
    return mysql.connector.connect(**configuratore)

def registrazione_gunpla(jan, nome_modello, tipologia, prezzo, edizione, quantita, scala, tipologia_specifica=None):
    connessione=None
    cursore=None

    try:
        connessione = _connessione_aperta()
        cursore = connessione.cursor()
        query="""
                INSERT INTO gunpla (jan, nome_modello, tipologia, prezzo, edizione, quantita, scala)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        valori= (jan, nome_modello, tipologia, prezzo, edizione, quantita, scala)
        cursore.execute(query,valori)


        id_gunplas= cursore.lastrowid

        riconoscimento_tipologia= tipologia.strip().upper()

        if riconoscimento_tipologia== "EG":
                query2 = "INSERT INTO eg_gunpla (id_gunpla) VALUES (%s)"
                cursore.execute(query2, (id_gunplas,))

        elif riconoscimento_tipologia== "SD":
            query2 = "INSERT INTO sd_gunpla (id_gunpla, tipologia_sd) VALUES (%s, %s)"
            cursore.execute(query2, (id_gunplas, tipologia_specifica))

        elif riconoscimento_tipologia== "HG":
            query2 = "INSERT INTO hg_gunpla (id_gunpla, tipologia_hg) VALUES (%s, %s)"
            cursore.execute(query2, (id_gunplas, tipologia_specifica))

        elif riconoscimento_tipologia== "RG":
            query2 = "INSERT INTO rg_gunpla (id_gunpla) VALUES (%s)"
            cursore.execute(query2, (id_gunplas,))

        elif riconoscimento_tipologia== "MG":
            query2 = "INSERT INTO mg_gunpla (id_gunpla, tipologia_mg) VALUES (%s, %s)"
            cursore.execute(query2, (id_gunplas, tipologia_specifica))

        elif riconoscimento_tipologia== "PG":
            query2 = "INSERT INTO pg_gunpla (id_gunpla, tipologia_pg) VALUES (%s, %s)"
            cursore.execute(query2, (id_gunplas, tipologia_specifica))

        else:
            print(f"Attenzione: tipologia '{tipologia}' non riconosciuta. Inserimento limitato alla tabella principale.")

        connessione.commit()
        
        return True, id_gunplas

    except Error as errore:
        if connessione:
            connessione.rollback()
        return False, str(errore)

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()

def ottieni_tutti_i_model_kit():
    connessione = None
    cursore = None
    try:
        connessione = _connessione_aperta()
        cursore = connessione.cursor(dictionary=True)
        
        query = """
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala 
            FROM gunpla
            ORDER BY id_gunpla DESC
        """
        cursore.execute(query)
        gunpla_list = cursore.fetchall()
        return gunpla_list

    except Error as errore:
        print(f"Errore DB: {errore}")
        return []

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()

def ricerca_model_kit_nome(nome_modello):
    connessione = None
    cursore = None

    try:
        connessione = _connessione_aperta()
        cursore = connessione.cursor(dictionary=True)
        query = """
                SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala
                FROM gunpla
                WHERE nome_modello LIKE %s
                ORDER BY nome_modello ASC
            """
        
        valore_ricerca = f"%{nome_modello}%"
        cursore.execute(query, (valore_ricerca,))
        risultati = cursore.fetchall()
        return risultati
    
    except Error as errore:
        print(f"Errore durante la ricerca per nome: {errore}")
        return []

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()

def ricerca_model_kit_tipologia(tipologia_modello):
    connessione = None
    cursor = None
    try:
        connessione = _connessione_aperta()
        cursor = connessione.cursor(dictionary=True)
        
        query = """
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala
            FROM gunpla
            WHERE tipologia LIKE %s
            ORDER BY nome_modello ASC
        """
        valore_ricerca = f"%{tipologia_modello}%"
        
        cursor.execute(query, (valore_ricerca,))
        risultati = cursor.fetchall()
        return risultati

    except Error as errore:
        print(f"Errore durante la ricerca per tipologia: {errore}")
        return []

    finally:
        if cursor:
            cursor.close()
        if connessione and connessione.is_connected():
            connessione.close()

def ricerca_model_kit_jan(jan):
    connessione= None
    cursore=None

    try:
        connessione= _connessione_aperta()
        cursore= connessione.cursor(dictionary=True)
        jan2 = str(jan).strip()
        query = """
                SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala
                FROM gunpla
                WHERE jan = %s
            """
        valore_ricerca = (jan2,)

        cursore.execute(query, valore_ricerca)
        risultati = cursore.fetchall()
        return risultati

    except Error as errore:
        print(f"Errore durante la ricerca per JAN: {errore}")
        return []

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()

def ricerca_model_kit_esauriti():
    connessione= None
    cursore=None

    try:
        connessione = _connessione_aperta()
        cursor = connessione.cursor(dictionary=True)
        query = """
        SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala
        FROM gunpla
        WHERE quantita = 0
        ORDER BY nome_modello ASC
        """
        cursor.execute(query)
        risultati = cursor.fetchall()
        return risultati
    
    except Error as errore:
        print(f"Errore durante il recupero dei prodotti esauriti: {errore}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connessione and connessione.is_connected():
            connessione.close()

def aggiornamento_quantita_gunplas(jan,quantita_variabile):
    connessione = None
    cursore = None
    try:
        connessione = _connessione_aperta()
        cursore = connessione.cursor(dictionary=True)
        
        query_ricerca = "SELECT id_gunpla, nome_modello, quantita FROM gunpla WHERE jan = %s"
        cursore.execute(query_ricerca, (str(jan).strip(),))
        gunpla = cursore.fetchone()
        
        if not gunpla:
            return False, f"Nessun Gunpla trovato con il codice JAN {jan}."
        
        quantita_aggiornata = gunpla["quantita"]
        nuova_quantita = quantita_aggiornata + quantita_variabile
        

        if nuova_quantita < 0:
            return False, f"Quantità insufficiente in magazzino. Disponibili: {quantita_aggiornata}, richiesti da rimuovere: {abs(variazione_quantita)}."
        

        query_update = "UPDATE gunpla SET quantita = %s WHERE jan = %s"
        cursore.execute(query_update, (nuova_quantita, str(jan).strip()))
        
        connessione.commit()
        
        return True, f"Quantità per '{gunpla['nome_modello']}' aggiornata con successo! Nuova giacenza: {nuova_quantita}."

    except Error as errore:
        if connessione:
            connessione.rollback()
        return False, f"Errore del database: {errore}"

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()