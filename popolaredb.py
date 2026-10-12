import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# Configurazione della connessione al database MySQL
config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "gunplaDB")
}

# Lista di 100 Gunpla reali e strutturati
# Formato: (JAN, Nome Modello, Tipologia, Prezzo, Edizione, Quantità, Scala, Tipologia Specifica)
dataset_gunpla = [
    # ---------------- ENTRY GRADE (EG) - 10 Kit ----------------
    (4573102607560, "RX-78-2 Gundam", "EG", 10.00, "Standard", 15, "1/144", None),
    (4573102611230, "Strike Gundam", "EG", 12.00, "Standard", 10, "1/144", None),
    (4573102633569, "v Gundam (Nu Gundam)", "EG", 12.50, "Standard", 12, "1/144", None),
    (4573102642516, "Lah Gundam", "EG", 11.00, "Standard", 8, "1/144", None),
    (4573102654311, "Build Strike Exceed Galaxy", "EG", 13.00, "Standard", 7, "1/144", None),
    (4573102615022, "RX-78-2 Gundam (Full Weapon Set)", "EG", 15.00, "Standard", 10, "1/144", None),
    (4573102621001, "Strike Gundam (Deactive Mode)", "EG", 14.00, "Gundam Base", 4, "1/144", None),
    (4573102608888, "RX-78-2 Gundam (Clear Color)", "EG", 12.00, "Limited", 5, "1/144", None),
    (4573102631111, "v Gundam (First Lot Color)", "EG", 16.00, "Premium Bandai", 3, "1/144", None),
    (4573102649999, "Lah Gundam (First Prototype)", "EG", 13.50, "Standard", 6, "1/144", None),

    # ---------------- SUPER DEFORMED (SD) - 15 Kit ----------------
    (4573102582110, "SDEX RX-78-2 Gundam", "SD", 8.00, "Standard", 12, "Non in scala", "SDEX"),
    (4573102615010, "SDEX Wing Gundam Zero EW", "SD", 9.00, "Standard", 8, "Non in scala", "SDEX"),
    (4573102610119, "SDEX Strike Freedom Gundam", "SD", 8.50, "Standard", 10, "Non in scala", "SDEX"),
    (4573102557100, "SDCS Wing Gundam Zero EW", "SD", 11.00, "Standard", 6, "Non in scala", "SDCS"),
    (4573102576001, "SDCS RX-78-2 Gundam", "SD", 10.00, "Standard", 14, "Non in scala", "SDCS"),
    (4573102588002, "SDCS MS-06S Zaku II", "SD", 10.00, "Standard", 9, "Non in scala", "SDCS"),
    (4573102601010, "SDCS Zeta Gundam", "SD", 12.00, "Standard", 5, "Non in scala", "SDCS"),
    (4573102605552, "SDEX Ex-S Gundam", "SD", 8.50, "Standard", 7, "Non in scala", "SDEX"),
    (4573102612233, "SDEX Sazabi", "SD", 9.50, "Standard", 11, "Non in scala", "SDEX"),
    (4573102623344, "SDCS Phenix (NT Ver.)", "SD", 14.00, "Standard", 4, "Non in scala", "SDCS"),
    (4573102634455, "SD World Heroes Sun Quan Astray", "SD", 9.00, "Standard", 8, "Non in scala", "SD World"),
    (4573102645566, "SD World Heroes Cao Cao Wing Gundam", "SD", 9.00, "Standard", 8, "Non in scala", "SD World"),
    (4573102656677, "SD World Heroes Strike Liu Bei Gundam", "SD", 9.50, "Standard", 10, "Non in scala", "SD World"),
    (4573102667788, "SDCS Calibarn", "SD", 15.00, "Standard", 6, "Non in scala", "SDCS"),
    (4573102678899, "SDEX Gundam Aerial", "SD", 9.00, "Standard", 15, "Non in scala", "SDEX"),

    # ---------------- HIGH GRADE (HG) - 35 Kit ----------------
    (4573102595820, "HGUC RX-78-2 Gundam (Revive)", "HG", 13.00, "Standard", 20, "1/144", "HGUC"),
    (4573102630300, "HGWFM Gundam Aerial", "HG", 16.50, "Standard", 18, "1/144", "HGWFM"),
    (4573102633400, "HGWFM Gundam Calibarn", "HG", 22.00, "Standard", 12, "1/144", "HGWFM"),
    (4573102650011, "HGCE Freedom Gundam (Revive)", "HG", 20.00, "Standard", 15, "1/144", "HGCE"),
    (4573102650022, "HGCE Strike Freedom Gundam", "HG", 22.00, "Standard", 10, "1/144", "HGCE"),
    (4573102650033, "HGCE Destiny Gundam (Revive)", "HG", 24.00, "Standard", 8, "1/144", "HGCE"),
    (4573102650044, "HGCE Infinite Justice Gundam", "HG", 24.00, "Standard", 7, "1/144", "HGCE"),
    (4573102650055, "HGCE Mighty Strike Freedom Gundam", "HG", 28.00, "Standard", 14, "1/144", "HGCE"),
    (4573102650066, "HGCE Infinite Justice Gundam Type II", "HG", 27.00, "Standard", 9, "1/144", "HGCE"),
    (4573102573988, "HGIBO Gundam Barbatos Lupus Rex", "HG", 18.00, "Standard", 11, "1/144", "HGIBO"),
    (4573102573995, "HGIBO Gundam Bael", "HG", 16.00, "Standard", 0, "1/144", "HGIBO"),
    (4573102574008, "HGIBO Gundam Vidar", "HG", 16.00, "Standard", 6, "1/144", "HGIBO"),
    (4573102580000, "HGUC MS-06S Zaku II (Revive)", "HG", 15.00, "Standard", 16, "1/144", "HGUC"),
    (4573102580017, "HGUC MS-07B-3 Gouf Custom", "HG", 17.00, "Standard", 8, "1/144", "HGUC"),
    (4573102580024, "HGUC RX-0 Unicorn Gundam (Destroy Mode)", "HG", 21.00, "Standard", 10, "1/144", "HGUC"),
    (4573102580031, "HGUC MSN-06S Sinanju", "HG", 28.00, "Standard", 5, "1/144", "HGUC"),
    (4573102580048, "HGUC NZ-666 Kshatriya", "HG", 50.00, "Standard", 3, "1/144", "HGUC"),
    (4573102580055, "HGUC RX-105 Xi Gundam", "HG", 65.00, "Standard", 4, "1/144", "HGUC"),
    (4573102580062, "HGUC RX-104FF Penelope", "HG", 75.00, "Standard", 2, "1/144", "HGUC"),
    (4573102580079, "HGUC Messala", "HG", 32.00, "Standard", 4, "1/144", "HGUC"),
    (4573102630010, "HGWFM Gundam Pharact", "HG", 20.00, "Standard", 8, "1/144", "HGWFM"),
    (4573102630027, "HGWFM Darilbalde", "HG", 20.00, "Standard", 9, "1/144", "HGWFM"),
    (4573102630034, "HGWFM Michaelis", "HG", 18.00, "Standard", 7, "1/144", "HGWFM"),
    (4573102630041, "HGWFM Gundam Lfrith", "HG", 18.00, "Standard", 12, "1/144", "HGWFM"),
    (4573102630058, "HGWFM Beguir-Beu", "HG", 18.00, "Standard", 6, "1/144", "HGWFM"),
    (4573102630065, "HGWFM Gundam Schwarzette", "HG", 22.00, "Standard", 11, "1/144", "HGWFM"),
    (4573102640019, "HGAC Wing Gundam Zero", "HG", 18.00, "Standard", 10, "1/144", "HGAC"),
    (4573102640026, "HGAC Gundam Deathscythe", "HG", 17.00, "Standard", 8, "1/144", "HGAC"),
    (4573102640033, "HGAC Gundam Heavyarms", "HG", 17.00, "Standard", 8, "1/144", "HGAC"),
    (4573102640040, "HGAC Gundam Sandrock", "HG", 16.00, "Standard", 7, "1/144", "HGAC"),
    (4573102640057, "HGAC Shenlong Gundam", "HG", 17.00, "Standard", 9, "1/144", "HGAC"),
    (4573102651110, "HGBF Build Strike Gundam Full Package", "HG", 16.00, "Standard", 5, "1/144", "HGBF"),
    (4573102652226, "HGUC Moon Gundam", "HG", 32.00, "Standard", 6, "1/144", "HGUC"),
    (4573102653332, "HGUC Nightingale", "HG", 78.00, "Standard", 2, "1/144", "HGUC"),
    (4573102654448, "HGUC RX-93 v Gundam", "HG", 26.00, "Standard", 13, "1/144", "HGUC"),

    # ---------------- REAL GRADE (RG) - 15 Kit ----------------
    (4573102582100, "RG RX-78-2 Gundam", "RG", 28.00, "Standard", 8, "1/144", None),
    (4573102578426, "RG Nu Gundam", "RG", 42.00, "Standard", 12, "1/144", None),
    (4573102580825, "RG Sazabi", "RG", 45.00, "Standard", 10, "1/144", None),
    (4573102613318, "RG Hi-Nu Gundam", "RG", 48.00, "Standard", 9, "1/144", None),
    (4573102604255, "RG Wing Gundam Zero EW", "RG", 35.00, "Premium Bandai", 5, "1/144", None),
    (4573102610011, "RG MSN-02 Zeong", "RG", 58.00, "Standard", 6, "1/144", None),
    (4573102610028, "RG GDM-01 God Gundam", "RG", 38.00, "Standard", 11, "1/144", None),
    (4573102610035, "RG RX-0 Unicorn Gundam", "RG", 40.00, "Standard", 7, "1/144", None),
    (4573102610042, "RG RX-0[N] Unicorn Gundam 02 Banshee Norn", "RG", 42.00, "Standard", 5, "1/144", None),
    (4573102610059, "RG ZGMF-X10A Freedom Gundam", "RG", 30.00, "Standard", 8, "1/144", None),
    (4573102610066, "RG ZGMF-X20A Strike Freedom Gundam", "RG", 33.00, "Standard", 9, "1/144", None),
    (4573102610073, "RG MBF-P02 Gundam Astray Red Frame", "RG", 30.00, "Standard", 10, "1/144", None),
    (4573102610080, "RG GN-001 Gundam Exia", "RG", 28.00, "Standard", 7, "1/144", None),
    (4573102610097, "RG GN-0000+GNR-010 00 Raiser", "RG", 35.00, "Standard", 6, "1/144", None),
    (4573102660001, "RG RX-78-2 Gundam Ver.2.0", "RG", 38.00, "Standard", 15, "1/144", None),

    # ---------------- MASTER GRADE (MG) - 20 Kit ----------------
    (4573102615053, "Wing Gundam Zero EW", "MG", 55.00, "Standard", 8, "1/100", "Ver.Ka"),
    (4573102633583, "Strike Freedom Gundam", "MG", 140.00, "Standard", 3, "1/100", "MGEX"),
    (4573102640154, "Freedom Gundam", "MG", 40.00, "Standard", 10, "1/100", "MGSD"),
    (4573102604262, "Unicorn Gundam", "MG", 230.00, "Standard", 1, "1/100", "MGEX"),
    (4573102554567, "Zeta Gundam", "MG", 65.00, "Premium Bandai", 2, "1/100", "Ver.Ka"),
    (4573102580100, "RX-93 v Gundam", "MG", 75.00, "Standard", 5, "1/100", "Ver.Ka"),
    (4573102580117, "MSN-04 Sazabi", "MG", 95.00, "Standard", 4, "1/100", "Ver.Ka"),
    (4573102580124, "GN-0000DVR/S Gundam 00 Sky", "MG", 60.00, "Standard", 6, "1/100", "Standard"),
    (4573102580131, "Eclipse Gundam", "MG", 53.00, "Standard", 7, "1/100", "Standard"),
    (4573102580148, "Gundam Dynames", "MG", 48.00, "Standard", 8, "1/100", "Standard"),
    (4573102580155, "Gundam Kyrios", "MG", 52.00, "Standard", 6, "1/100", "Standard"),
    (4573102580162, "Gundam Virtue", "MG", 85.00, "Standard", 4, "1/100", "Standard"),
    (4573102580179, "Gundam Barbatos", "MG", 50.00, "Standard", 12, "1/100", "Standard"),
    (4573102580186, "MS-06S Zaku II Ver.2.0", "MG", 38.00, "Standard", 9, "1/100", "Standard"),
    (4573102580193, "RX-78-2 Gundam Ver.3.0", "MG", 48.00, "Standard", 11, "1/100", "Standard"),
    (4573102580209, "Narrative Gundam C-Packs", "MG", 75.00, "Standard", 5, "1/100", "Ver.Ka"),
    (4573102580216, "Sinanju Stein (Narrative Ver.)", "MG", 80.00, "Standard", 3, "1/100", "Ver.Ka"),
    (4573102580223, "Barbatos Clear Color", "MG", 55.00, "Gundam Base", 3, "1/100", "Limited"),
    (4573102580230, "MGSD Barbatos", "MG", 45.00, "Standard", 8, "1/100", "MGSD"),
    (4573102580247, "Full Armor Gundam", "MG", 70.00, "Standard", 4, "1/100", "Ver.Ka"),

    # ---------------- PERFECT GRADE (PG) - 5 Kit ----------------
    (4573102607607, "RX-78-2 Gundam Unleashed", "PG", 250.00, "Standard", 2, "1/60", "Unleashed"),
    (4573102582119, "Strike Gundam", "PG", 140.00, "Standard", 1, "1/60", "PG Standard"),
    (4573102614056, "Unicorn Gundam", "PG", 200.00, "Standard", 3, "1/60", "PG Standard"),
    (4573102556782, "Zaku II", "PG", 120.00, "Standard", 4, "1/60", "PG Standard"),
    (4573102621818, "Unicorn Gundam Perfectibility", "PG", 350.00, "Premium Bandai", 1, "1/60", "PG Standard")
]

def popola_100_gunpla():
    connessione = None
    cursore = None
    try:
        connessione = mysql.connector.connect(**config)
        cursore = connessione.cursor()

        query_padre = """
            INSERT INTO gunpla (jan, nome_modello, tipologia, prezzo, edizione, quantita, scala)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        conteggio_inseriti = 0

        for item in dataset_gunpla:
            jan, nome, tipo, prezzo, edizione, qta, scala, spec = item
            
            # Inserimento nella tabella padre 'gunpla'
            cursore.execute(query_padre, (jan, nome, tipo, prezzo, edizione, qta, scala))
            id_generato = cursore.lastrowid
            
            # Inserimento nella sotto-tabella corrispondente in base alla tipologia
            tipo_clean = tipo.strip().upper()
            if tipo_clean == "EG":
                cursore.execute("INSERT INTO eg_gunpla (id_gunpla) VALUES (%s)", (id_generato,))
            elif tipo_clean == "SD":
                cursore.execute("INSERT INTO sd_gunpla (id_gunpla, tipologia_sd) VALUES (%s, %s)", (id_generato, spec))
            elif tipo_clean == "HG":
                cursore.execute("INSERT INTO hg_gunpla (id_gunpla, tipologia_hg) VALUES (%s, %s)", (id_generato, spec))
            elif tipo_clean == "RG":
                cursore.execute("INSERT INTO rg_gunpla (id_gunpla) VALUES (%s)", (id_generato,))
            elif tipo_clean == "MG":
                cursore.execute("INSERT INTO mg_gunpla (id_gunpla, tipologia_mg) VALUES (%s, %s)", (id_generato, spec))
            elif tipo_clean == "PG":
                cursore.execute("INSERT INTO pg_gunpla (id_gunpla, tipologia_pg) VALUES (%s, %s)", (id_generato, spec))

            conteggio_inseriti += 1

        connessione.commit()
        print(f"Popolamento completato con successo! Inseriti {conteggio_inseriti} model kit.")

    except Error as errore:
        if connessione:
            connessione.rollback()
        print(f"Errore durante il popolamento del DB: {errore}")

    finally:
        if cursore:
            cursore.close()
        if connessione and connessione.is_connected():
            connessione.close()

if __name__ == "__main__":
    popola_100_gunpla()