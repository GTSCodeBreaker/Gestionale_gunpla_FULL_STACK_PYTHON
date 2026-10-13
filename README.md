# Gunpla Store Management & Web Catalog

Un'applicazione web full-stack sviluppata in Python con Flask e MySQL per la gestione del magazzino e del catalogo di un negozio di modellini Gunpla (Gundam Plastic Model Kit).

---

## Struttura della Soluzione

Il progetto è strutturato separando la gestione del database relazionale, le query di accesso ai dati e il controller dell'interfaccia web Flask:

* **1. `gunplaDB`**: Lo schema del database relazionale MySQL.
* **2. `database.py`**: Il modulo repository / Data Access Layer per l'interazione con MySQL.
* **3. `app.py`**: L'applicazione web Flask che gestisce la logica delle route, il filtraggio dei dati, la personalizzazione dei temi e le pagine del frontend.
* **extra. `popolareDB.py`**: Uno script di utilità eseguito per il popolamento iniziale del database.

---

## 1. Database MySQL (`gunplaDB`)

Il database relazionale `gunplaDB` contiene l'inventario globale e la profilazione per tipologia/grade dei modellini:

* **Tabella principale `gunpla`**: Memorizza i dati generali dei modellini, tra cui il codice a barre univoco JAN (`jan`), il nome del modello (`nome_modello`), la tipologia (`tipologia`), il prezzo (`prezzo`), l'edizione (`edizione`), la quantità disponibile (`quantita`) e la scala (`scala`).
* **Tabelle per tipologia** (`eg_gunpla`, `pg_gunpla`, ecc.): Tabelle di dettaglio collegate alla tabella padre `gunpla` tramite chiave esterna (`FOREIGN KEY`) con vincoli di integrità referenziale (`ON DELETE CASCADE`, `ON UPDATE CASCADE`).

---

## 2. Livello di Accesso ai Dati (`database.py`)

Il modulo `database.py` raccoglie le funzioni repository che isolano le istruzioni SQL dalla logica web:

* **Configurazione e Connessione**: Recupera i parametri di connessione dal file `.env` tramite `python-dotenv` ed effettua la connessione tramite `mysql-connector-python`.
* **Query Parametrizzate**: Utilizza i placeholder `%s` nelle istruzioni SQL per prevenire attacchi di SQL Injection e proteggere la sicurezza dei dati.

### Funzioni gestite:
* **`ottieni_tutti_i_model_kit()`**: Recupera la lista completa dell'inventario.
* **`ricerca_model_kit_nome()` e `ricerca_model_kit_jan()`**: Eseguono la ricerca filtrata dei modellini per nome o per codice JAN.
* **`registrazione_gunpla()`**: Inserisce un nuovo Gunpla sia nella tabella principale che nella relativa tabella specifica di tipologia.
* **`aggiornamento_quantita_gunplas()`**: Aggiorna le scorte presenti in magazzino.
* **`registra_vendita()`, `ottieni_storico_vendite()`, `ottieni_dettaglio_vendita()`**: Gestiscono la registrazione delle vendite e lo storico delle transazioni.

---

## 3. Frontend e Controller Web (`app.py`)

Il file `app.py` costituisce il cuore dell'applicazione web sviluppata con il framework Flask:

* **Dashboard (`/` o `/dashboard`)**:
  * Supporta la ricerca dinamica dell'inventario permettendo di filtrare per nome modello o per codice JAN.
  * Calcola i principali indicatori KPI (totale pezzi in magazzino, valore economico totale del magazzino e conteggio delle scorte critiche con quantità $\le 2$).
* **Inserimento nuovo Gunpla (`/gunpla/nuovo`)**: Gestisce il form di inserimento dei nuovi modellini appoggiandosi alla funzione `registrazione_gunpla()`.
* **Gestione Templating e Temi Grafici**:
  * Interagisce con i file HTML nella cartella `templates/` mediante il motore Jinja2 per la resa dinamica dei dati a schermo.
  * Permette di personalizzare l'aspetto visivo dell'interfaccia alternando temi cromatici ispirati alle fazioni e serie dell'universo Gundam (es. Anaheim Electronics / Wing Zero).

---

## 4. Easter Egg: Sblocco del Tema Segreto "Cometa Rossa" (Char Aznable)

All'interno dell'interfaccia è nascosto uno speciale **Easter Egg** che consente di sbloccare il tema visivo esclusivo dedicato a **Char Aznable**, l'iconico pilota dell'Universal Century noto come la *Cometa Rossa*.

### Indizi per lo sblocco (Hint):

1. **Inseguendo la Cometa Rossa**: *"Un vero pilota non passa inosservato. Prova a cercare nel sistema il nome dell'asso di Zeon o la sua celebre identità..."*
2. **Tre Volte Più Veloce**: *"Si dice che i suoi Mobile Suit si muovano a velocità tripla. Presta attenzione ai codici o ai modelli iconici legati al suo nome (come MS-06S o MSN-04 Sazabi)..."*
3. **Protocollo AE-OS**: *"Fai attenzione agli elementi interattivi nella barra di navigazione o nell'area di selezione del tema: un'interazione particolare potrebbe attivare la modalità Cometa Rossa!"*

---

## Extra: Script di Popolamento Iniziale (`popolareDB.py`)

Il file `popolareDB.py` serve unicamente a popolare il database `gunplaDB` con i dati iniziali di prova. 

Contiene la funzione `popola_100_gunpla()` ed un dataset integrato di 100 modellini Gunpla reali appartenenti a diverse categorie (EG, HG, RG, MG, PG). Lo script inserisce ogni elemento nella tabella principale `gunpla` e nella relativa tabella figlia specifica per grado. Non fa parte del flusso operativo della web app in esecuzione.

---

## Guida all'Installazione e Avvio

### 1. Configurazione del file `.env`
Creare un file `.env` nella cartella radice del progetto inserendo le credenziali di accesso a MySQL:

* **`MYSQL_HOST`**: L'indirizzo IP o l'host del server MySQL (ad es. `localhost` o `127.0.0.1`)
* **`MYSQL_PORT`**: La porta usata dal servizio MySQL (di default `3306`)
* **`MYSQL_USER`**: Il nome dell'utente applicativo abilitato ad accedere al database
* **`MYSQL_PASSWORD`**: La password dell'utente del database locale
* **`MYSQL_DATABASE`**: Il nome del database (`gunplaDB`)

### 2. Creazione dell'Ambiente Virtuale
Creare e attivare l'ambiente virtuale isolato `.venv`:

* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **Linux / macOS**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Installazione Dipendenze
Con l'ambiente virtuale attivo, installare le librerie elencate in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

### 4. Popolamento Iniziale (Opzionale)
Per caricare i dati di test nel database:

```bash
python popolareDB.py
```

### 5. Avvio dell'Applicazione
Avviare il server di sviluppo Flask:

```bash
flask --app app run --debug
```
L'applicazione sarà visibile nel browser all'indirizzo `http://127.0.0.1:5000`.

---

## Licenza

Questo progetto è distribuito sotto **Licenza MIT**.