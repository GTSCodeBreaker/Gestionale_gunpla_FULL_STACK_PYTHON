# Gestionale Gunpla - Full Stack Python
Questo progetto permette di gestire il magazzino e il catalogo di un negozio di modellini Gunpla (Gundam Plastic Model) attraverso un database MySQL e uno script Python per la gestione dei dati

## Struttura del Database (gunplaDB)
Il file SQL crea il database gunplaDB e definisce la struttura delle tabelle necessarie per organizzare i modellini e le vendite:   
gunpla: la tabella principale (padre) che contiene le informazioni generali di ogni modellino, come il codice a barre (JAN), il nome del modello, la tipologia generale, il prezzo, l'edizione, la quantità in magazzino e la scala.   
Tabelle per tipologia (eg_gunpla, sd_gunpla, hg_gunpla, rg_gunpla, mg_gunpla, pg_gunpla): sotto-tabelle collegate alla tabella padre. Permettono di specificare dettagli aggiuntivi per ciascuna categoria di kit (Entry Grade, Super Deformed, High Grade, Real Grade, Master Grade, Perfect Grade).   
vendita: registra le transazioni effettuate, memorizzando la data e il totale dell'importo.   
Scontrino: collega i singoli modellini venduti alla rispettiva transazione di vendita, indicando la quantità venduta e il prezzo unitario al momento dell'acquisto.   
Tutte le tabelle specifiche delle tipologie e dello scontrino usano vincoli di integrità (chiavi esterne) con eliminazione e aggiornamento a cascata per garantire la coerenza dei dati.

## Logica e Script Python 

Gli script Python gestiscono la connessione al database MySQL e l'esecuzione delle operazioni sui dati in sicurezza.   
### Configurazione della Connessione
L'applicazione legge le credenziali di accesso al database da un file di ambiente tramite il pacchetto python-dotenv. 
Questo approccio garantisce la sicurezza senza dover inserire password nel codice sorgente.   
## Parametri principali di configurazione:
* **`MYSQL_HOST`**: l'indirizzo IP o l'host del server MySQL (ad es. `127.0.0.1` per il server locale)
* **`MYSQL_PORT`**: la porta usata dal servizio MySQL (di default `3306`)
* **`MYSQL_USER`**: il nome dell'utente applicativo abilitato ad accedere al database
* **`MYSQL_PASSWORD`**: la password dell'utente del database locale
* **`MYSQL_DATABASE`**: il nome dello specifico database a cui l'applicazione deve connettersi

