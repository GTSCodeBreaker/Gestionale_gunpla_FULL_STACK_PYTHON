import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

# Importazione delle funzioni repository dal modulo database.py
from database import (
    ottieni_tutti_i_model_kit,
    ricerca_model_kit_nome,
    ricerca_model_kit_jan,
    registrazione_gunpla,
    aggiornamento_quantita_gunplas,
    registra_vendita,
    ottieni_storico_vendite,     
    ottieni_dettaglio_vendita
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "wing_zero_secret_key_2026")

# ==============================================================================
# ROUTE DELL'APPLICAZIONE
# ==============================================================================

@app.route("/")
@app.route("/dashboard")
def dashboard():
    """Route principale con supporto a ricerca e filtraggio dinamico."""
    # Lettura dei parametri inviati dalla query string (form GET)
    query_testo = request.args.get("q", "").strip()
    criterio = request.args.get("criterio", "nome")

    # --- EASTER EGG CHAR AZNABLE ---
    if query_testo.lower() in ["char", "char aznable"]:
        flash("🔥 Red Comet detected! Performance increased by 3x!", "danger")

    # Selezione della funzione di ricerca
    if query_testo:
        if criterio == "jan":
            gunpla_list = ricerca_model_kit_jan(query_testo)
        else:
            gunpla_list = ricerca_model_kit_nome(query_testo)
    else:
        gunpla_list = ottieni_tutti_i_model_kit()


    
    # Selezione della funzione di ricerca appropriata in base al criterio
    if query_testo:
        if criterio == "jan":
            gunpla_list = ricerca_model_kit_jan(query_testo)
        else:
            gunpla_list = ricerca_model_kit_nome(query_testo)
    else:
        # Se non c'è ricerca, carica l'intero inventario
        gunpla_list = ottieni_tutti_i_model_kit()
    
    # Calcolo delle statistiche KPI
    totale_pezzi = sum(item["quantita"] for item in gunpla_list)
    valore_magazzino = sum(float(item["prezzo"]) * item["quantita"] for item in gunpla_list)
    scorte_critiche = len([item for item in gunpla_list if item["quantita"] <= 2])
    
    return render_template(
        "dashboard.html",
        gunpla_list=gunpla_list,
        totale_pezzi=totale_pezzi,
        valore_magazzino=valore_magazzino,
        scorte_critiche=scorte_critiche,
        q=query_testo,       
        criterio=criterio    
    )


@app.route("/gunpla/nuovo", methods=["GET", "POST"])
def nuovo_gunpla():
    """Gestione dell'inserimento tramite la funzione registrazione_gunpla()."""
    if request.method == "POST":
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
            
        # Chiamata alla funzione del database
        esito, risultato = registrazione_gunpla(
            jan=jan,
            nome_modello=nome_modello,
            tipologia=tipologia,
            prezzo=prezzo,
            edizione=edizione,
            quantita=quantita,
            scala=scala
        )
        
        if esito:
            flash(f"Model Kit '{nome_modello}' inserito con successo!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash(f"Errore durante l'inserimento: {risultato}", "danger")
            return redirect(url_for("nuovo_gunpla"))

    return render_template("nuovo_gunpla.html")


@app.route("/carrello/aggiungi/<int:id_gunpla>", methods=["POST"])
def aggiungi_al_carrello(id_gunpla):
    """Aggiunge un Gunpla al carrello cercandolo nella lista ricevuta da database.py."""
    quantita_richiesta = request.form.get("quantita", type=int, default=1)
    
    if quantita_richiesta <= 0:
        flash("La quantità deve essere maggiore di zero!", "danger")
        return redirect(url_for("dashboard"))
    
    # Recupero dati usando le funzioni repository
    tutti_i_gunpla = ottieni_tutti_i_model_kit()
    gunpla = next((g for g in tutti_i_gunpla if g["id_gunpla"] == id_gunpla), None)
    
    if not gunpla:
        flash("Gunpla non trovato!", "danger")
        return redirect(url_for("dashboard"))
    
    # Inizializza il carrello in sessione
    if "carrello" not in session:
        session["carrello"] = {}

    carrello = session["carrello"]
    id_str = str(id_gunpla)

    quantita_gia_nel_carrello = carrello.get(id_str, {}).get("quantita", 0)
    quantita_totale_richiesta = quantita_gia_nel_carrello + quantita_richiesta

    # Verifica disponibilita
    if quantita_totale_richiesta > gunpla["quantita"]:
        flash(f"Scorte insufficienti per {gunpla['nome_modello']}. Disponibili: {gunpla['quantita']}.", "warning")
        return redirect(url_for("dashboard"))

    carrello[id_str] = {
        "id_gunpla": gunpla["id_gunpla"],
        "nome_modello": gunpla["nome_modello"],
        "prezzo": float(gunpla["prezzo"]),
        "quantita": quantita_totale_richiesta
    }
    
    session.modified = True
    flash(f"Aggiunto '{gunpla['nome_modello']}' (x{quantita_richiesta}) al carrello!", "success")
    return redirect(url_for("dashboard"))


@app.route("/carrello")
def visualizza_carrello():
    """Mostra la pagina di riepilogo del carrello."""
    carrello = session.get("carrello", {})
    elementi_carrello = list(carrello.values())
    totale_carrello = sum(item["prezzo"] * item["quantita"] for item in elementi_carrello)
    
    return render_template("carrello.html", carrello=elementi_carrello, totale=totale_carrello)


@app.route("/carrello/svuota", methods=["POST"])
def svuota_carrello():
    """Svuota la sessione del carrello."""
    session.pop("carrello", None)
    flash("Carrello svuotato con successo.", "info")
    return redirect(url_for("visualizza_carrello"))


@app.route("/gunpla/modifica/<int:id_gunpla>", methods=["GET", "POST"])
def modifica_gunpla(id_gunpla):
    """Gestisce la modifica delle scorte consentendo di aumentare o diminuire la quantità."""
    tutti_i_gunpla = ottieni_tutti_i_model_kit()
    gunpla = next((g for g in tutti_i_gunpla if g["id_gunpla"] == id_gunpla), None)
    
    if not gunpla:
        flash("Gunpla non trovato!", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        operazione = request.form.get("operazione", "aumenta")
        quantita_input = request.form.get("quantita", type=int, default=0)

        if quantita_input <= 0:
            flash("Inserisci una quantità valida maggiore di zero!", "warning")
            return render_template("modifica_gunpla.html", gunpla=gunpla)

        # Se l'operazione è "diminuisci", trasformiamo il valore in negativo
        differenza = quantita_input if operazione == "aumenta" else -quantita_input

        # Aggiorna le scorte usando la funzione repository
        esito, messaggio = aggiornamento_quantita_gunplas(gunpla["jan"], differenza)
        if esito:
            flash(messaggio, "success")
        else:
            flash(messaggio, "danger")
            
        return redirect(url_for("dashboard"))

    return render_template("modifica_gunpla.html", gunpla=gunpla)

# ==============================================================================
# ROUTE CASSA E CHECKOUT
# ==============================================================================

@app.route("/carrello/cassa", methods=["GET", "POST"])
def cassa():
    """Gestisce il processo di checkout, l'applicazione dello sconto e la registrazione della vendita."""
    carrello = session.get("carrello", {})
    elementi_carrello = list(carrello.values())

    if not elementi_carrello:
        flash("Il carrello è vuoto. Aggiungi dei prodotti prima di andare alla cassa!", "warning")
        return redirect(url_for("dashboard"))

    totale_lordo = sum(item["prezzo"] * item["quantita"] for item in elementi_carrello)

    if request.method == "POST":
        # Lettura dello sconto inserito dall'operatore
        percentuale_sconto = request.form.get("sconto", type=float, default=0.0)
        
        if percentuale_sconto < 0 or percentuale_sconto > 100:
            flash("La percentuale di sconto deve essere compresa tra 0 e 100.", "danger")
            return redirect(url_for("cassa"))

        # Registrazione transazione nel database MySQL tramite database.py
        id_vendita = registra_vendita(elementi_carrello, percentuale_sconto)

        if id_vendita:
            valore_sconto = totale_lordo * (percentuale_sconto / 100)
            totale_netto = totale_lordo - valore_sconto

            # Salva i dettagli per il riepilogo scontrino
            dettagli_scontrino = {
                "id_vendita": id_vendita,
                "articoli": elementi_carrello,
                "totale_lordo": totale_lordo,
                "percentuale_sconto": percentuale_sconto,
                "valore_sconto": valore_sconto,
                "totale_netto": totale_netto
            }

            # Svuota il carrello dopo la vendita riuscita
            session.pop("carrello", None)
            flash(f"Vendita #{id_vendita} registrata con successo!", "success")

            return render_template("conferma_ordine.html", ricevuta=dettagli_scontrino)
        else:
            flash("Errore durante la registrazione della vendita nel database.", "danger")
            return redirect(url_for("visualizza_carrello"))

    return render_template("cassa.html", carrello=elementi_carrello, totale_lordo=totale_lordo)


# ==============================================================================
# ROUTE STORICO SCONTRINI
# ==============================================================================

@app.route("/storico_scontrini")
def storico_scontrini():
    """Mostra la lista completa di tutti gli scontrini e delle vendite effettuate."""
    vendite = ottieni_storico_vendite()
    
    totale_incassato = sum(float(v["totale_vendita"]) for v in vendite)
    totale_scontrini = len(vendite)
    media_scontrino = (totale_incassato / totale_scontrini) if totale_scontrini > 0 else 0.0

    return render_template(
        "storico_scontrini.html",
        vendite=vendite,
        totale_incassato=totale_incassato,
        totale_scontrini=totale_scontrini,
        media_scontrino=media_scontrino
    )


@app.route("/storico_scontrini/<int:id_vendita>")
def dettaglio_scontrino(id_vendita):
    """Visualizza o ristampa una specifica ricevuta digitale."""
    ricevuta = ottieni_dettaglio_vendita(id_vendita)
    if not ricevuta:
        flash(f"Scontrino #{id_vendita} non trovato nel database.", "danger")
        return redirect(url_for("storico_scontrini"))
        
    return render_template("conferma_ordine.html", ricevuta=ricevuta)

if __name__ == "__main__":
    app.run(debug=True, port=8080)