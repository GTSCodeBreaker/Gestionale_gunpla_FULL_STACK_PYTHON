import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv as caricaenv
from datetime import datetime

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
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala, attivo 
            FROM gunpla
            WHERE attivo = 1
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
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala, attivo
            FROM gunpla
            WHERE nome_modello LIKE %s AND attivo = 1
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
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala, attivo
            FROM gunpla
            WHERE tipologia LIKE %s AND attivo = 1
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
    connessione = None
    cursore = None

    try:
        connessione = _connessione_aperta()
        cursore = connessione.cursor(dictionary=True)
        jan2 = str(jan).strip()
        
        query = """
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala, attivo
            FROM gunpla
            WHERE jan = %s AND attivo = 1
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

    connessione = None
    cursor = None

    try:
        connessione = _connessione_aperta()
        cursor = connessione.cursor(dictionary=True)
        
        query = """
            SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala, attivo
            FROM gunpla
            WHERE quantita = 0 AND attivo = 1
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

def disattiva_model_kit(jan):
    connessione = None
    cursore = None

    try:
        connessione = _connessione_aperta()
        cursore = connessione.cursor()
        
        query = "UPDATE gunpla SET attivo = 0 WHERE jan = %s"
        cursore.execute(query, (str(jan).strip(),))
        connessione.commit()
        
        modificati = cursore.rowcount
        return modificati > 0

    except Error as errore:
        if connessione:
            connessione.rollback()
        print(f"Errore durante la disattivazione del Model Kit: {errore}")
        return False

    finally:
        if cursore:
            cursore.close()
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
            return False, f"Quantità insufficiente in magazzino. Disponibili: {quantita_aggiornata}, richiesti da rimuovere: {abs(quantita_variabile)}."
        

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

def registra_vendita(carrello, percentuale_sconto=0.0):

    if not carrello:
        print("Il carrello è vuoto. Impossibile procedere con la vendita.")
        return None

    connessione = None
    cursore = None

    totale_lordo = sum(item['prezzo'] * item['quantita'] for item in carrello)
    totale_netto = totale_lordo * (1 - (percentuale_sconto / 100))
    data_ora_attuale = datetime.now()

    try:

        connessione = _connessione_aperta()
        cursore = connessione.cursor()

        query_vendita = """
            INSERT INTO vendita (data_vendita, totale_vendita)
            VALUES (%s, %s)
        """
        cursore.execute(query_vendita, (data_ora_attuale, totale_netto))
        
        id_vendita_generato = cursore.lastrowid

        query_scontrino = """
            INSERT INTO Scontrino (id_gunpla, prezzo_al_pezzo, id_vendita, quantita_venduta)
            VALUES (%s, %s, %s, %s)
        """
        
        query_aggiorna_scorte = """
            UPDATE gunpla
            SET quantita = quantita - %s
            WHERE id_gunpla = %s AND quantita >= %s
        """

        for item in carrello:
            id_gunpla = item['id_gunpla']
            prezzo_unitario = item['prezzo']
            quantita = item['quantita']

            cursore.execute(query_scontrino, (id_gunpla, prezzo_unitario, id_vendita_generato, quantita))

            cursore.execute(query_aggiorna_scorte, (quantita, id_gunpla, quantita))
            

            if cursore.rowcount == 0:
                raise Error(f"Giacenza insufficiente in magazzino per il Gunpla ID: {id_gunpla}")

        connessione.commit()
        print(f"Vendita #{id_vendita_generato} completata con successo! Totale: {totale_netto:.2f}€")
        return id_vendita_generato

    except Error as errore:
        if connessione:
            connessione.rollback()
        print(f"Errore durante la registrazione della vendita: {errore}")
        return None

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()
