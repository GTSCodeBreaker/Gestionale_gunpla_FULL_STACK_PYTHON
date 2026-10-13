import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)
# Chiave segreta per la gestione dei messaggi flash
app.secret_key = os.getenv("SECRET_KEY", "wing_zero_secret_key_2026")

# Configurazione parametri di connessione MySQL
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DATABASE"] = os.getenv("MYSQL_DATABASE", "gunplaDB")

# ==============================================================================
# GESTIONE CONNESSIONE DATABASE (Lifecycle con g e teardown)
# ==============================================================================

def get_db():
    """Apre una sola connessione al DB per richiesta e la salva in 'g'."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=app.config["MYSQL_HOST"],
            port=app.config["MYSQL_PORT"],
            user=app.config["MYSQL_USER"],
            password=app.config["MYSQL_PASSWORD"],
            database=app.config["MYSQL_DATABASE"]
        )
    return g.db

@app.teardown_appcontext
def close_db(errore=None):
    """Chiude automaticamente la connessione al termine di ogni richiesta."""
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()

# ==============================================================================
# ROUTE DELL'APPLICAZIONE
# ==============================================================================

@app.route("/")
@app.route("/dashboard")
def dashboard():
    """Route della vista principale: legge i Gunpla da gunplaDB e calcola le statistiche."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Query per recuperare tutti i Model Kit ordinati per ID decrescente
    cursor.execute("""
        SELECT id_gunpla, jan, nome_modello, tipologia, prezzo, edizione, quantita, scala 
        FROM gunpla 
        ORDER BY id_gunpla DESC
    """)
    gunpla_list = cursor.fetchall()
    cursor.close()
    
    # Calcolo dei KPI dinamici per la dashboard
    totale_pezzi = sum(item["quantita"] for item in gunpla_list)
    valore_magazzino = sum(item["prezzo"] * item["quantita"] for item in gunpla_list)
    scorte_critiche = len([item for item in gunpla_list if item["quantita"] <= 2])
    
    # Render del template Jinja2 passando i dati letti dal DB
    return render_template(
        "dashboard.html",
        gunpla_list=gunpla_list,
        totale_pezzi=totale_pezzi,
        valore_magazzino=valore_magazzino,
        scorte_critiche=scorte_critiche
    )

@app.route("/gunpla/nuovo", methods=["GET", "POST"])
def nuovo_gunpla():
    """Route per la gestione del form di inserimento (GET/POST)."""
    if request.method == "POST":
        # Lettura dei campi inviati dal form HTML
        jan = request.form.get("jan", "").strip()
        nome_modello = request.form.get("nome_modello", "").strip()
        tipologia = request.form.get("tipologia", "").strip()
        prezzo = request.form.get("prezzo", type=float)
        edizione = request.form.get("edizione", "").strip()
        quantita = request.form.get("quantita", type=int)
        scala = request.form.get("scala", "").strip()
        
        # Validazione lato server
        if not nome_modello or not jan or prezzo is None:
            flash("Compila tutti i campi obbligatori!", "danger")
            return redirect(url_for("nuovo_gunpla"))
            
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Query parametrizzata per evitare SQL Injection
            query = """
                INSERT INTO gunpla (jan, nome_modello, tipologia, prezzo, edizione, quantita, scala)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (jan, nome_modello, tipologia, prezzo, edizione, quantita, scala))
            db.commit()
            cursor.close()
            
            flash(f"Model Kit '{nome_modello}' inserito con successo!", "success")
            return redirect(url_for("dashboard"))
            
        except mysql.connector.Error as err:
            if db:
                db.rollback()
            flash(f"Errore durante l'inserimento: {err}", "danger")
            return redirect(url_for("nuovo_gunpla"))

    return render_template("nuovo_gunpla.html")

@app.route("/carrello/aggiungi/<int:id_gunpla>", methods=["POST"])
def aggiungi_al_carrello(id_gunpla):
    """Aggiunge un determinato Gunpla al carrello in sessione."""
    quantita_richiesta = request.form.get("quantita", type=int, default=1)
    
    if quantita_richiesta <= 0:
        flash("La quantità deve essere maggiore di zero!", "danger")
        return redirect(url_for("dashboard"))
    
    # Recupera i dettagli del Gunpla dal database
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_gunpla, nome_modello, prezzo, quantita FROM gunpla WHERE id_gunpla = %s", (id_gunpla,))
    gunpla = cursor.fetchone()
    cursor.close()
    
    if not gunpla:
        flash("Gunpla non trovato!", "danger")
        return redirect(url_for("dashboard"))
    
    # Inizializza il carrello in sessione se non esiste
    if "carrello" not in session:
        session["carrello"] = {}

    carrello = session["carrello"]
    id_str = str(id_gunpla)

    # Calcola quanti pezzi dello stesso articolo sono già nel carrello
    quantita_gia_nel_carrello = carrello.get(id_str, {}).get("quantita", 0)
    quantita_totale_richiesta = quantita_gia_nel_carrello + quantita_richiesta

    # Verifica scorte nel magazzino
    if quantita_totale_richiesta > gunpla["quantita"]:
        flash(f"Scorte insufficienti per {gunpla['nome_modello']}. Disponibili: {gunpla['quantita']}.", "warning")
        return redirect(url_for("dashboard"))

    # Aggiungi o aggiorna l'articolo nel carrello
    carrello[id_str] = {
        "id_gunpla": gunpla["id_gunpla"],
        "nome_modello": gunpla["nome_modello"],
        "prezzo": float(gunpla["prezzo"]),
        "quantita": quantita_totale_richiesta
    }
    
    # Notifica la modifica alla sessione di Flask
    session.modified = True
    flash(f"Aggiunto '{gunpla['nome_modello']}' (x{quantita_richiesta}) al carrello!", "success")
    
    return redirect(url_for("dashboard"))


@app.route("/carrello")
def visualizza_carrello():
    """Mostra la pagina di riepilogo del carrello prima della cassa."""
    carrello = session.get("carrello", {})
    elementi_carrello = list(carrello.values())
    
    totale_carrello = sum(item["prezzo"] * item["quantita"] for item in elementi_carrello)
    
    return render_template("carrello.html", carrello=elementi_carrello, totale=totale_carrello)


@app.route("/carrello/svuota", methods=["POST"])
def svuota_carrello():
    """Svuota completamente il carrello."""
    session.pop("carrello", None)
    flash("Carrello svuotato con successo.", "info")
    return redirect(url_for("visualizza_carrello"))






if __name__ == '__main__':
    app.run(debug=True, port=8080) 