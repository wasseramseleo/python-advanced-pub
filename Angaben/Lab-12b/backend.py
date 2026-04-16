from flask import Flask, jsonify, request, abort
import time
import logging

# Deaktiviert das normale Flask-Logging, um die Übung sauberer zu halten
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Ein einfacher In-Memory "Datenbank"-Speicher
# Stellt die Konten dar, die von unserer API verwaltet werden.
db = {
  "AT123": {"owner": "Max Mustermann", "balance": 1500.75, "currency": "EUR"},
  "DE456": {"owner": "Erika Mustermann", "balance": 800.00, "currency": "EUR"},
  "CH789": {"owner": "Peter Zbinden", "balance": 10000.00, "currency": "CHF"},
}


@app.route("/")
def index():
  return "Banking App API Server läuft."


@app.route("/api/account/<string:account_id>", methods=["GET"])
def get_account(account_id: str):
  """
  (GET) Ruft Kontodetails für eine ID ab.
  Simuliert eine Verzögerung, um Timeouts zu testen.
  """
  print(f"BACKEND: GET /api/account/{account_id} angefragt...")

  # Simuliert eine Netzwerk-Verzögerung von 0.5 Sekunden
  # Dies ist wichtig, um die 'timeout'-Funktionalität im Client zu testen.
  time.sleep(0.5)

  account = db.get(account_id)

  if not account:
    # 404 Not Found -> löst raise_for_status() im Client aus
    print(f"BACKEND: Account {account_id} nicht gefunden (404).")
    abort(404, description=f"Account {account_id} not found.")

  print(f"BACKEND: Sende Daten für {account_id}.")
  return jsonify(account)


@app.route("/api/account/<string:account_id>/transact", methods=["POST"])
def transact(account_id: str):
  """
  (POST) Führt eine Transaktion (DEPOSIT/WITHDRAW) durch.
  Liest JSON-Payload.
  """
  print(f"BACKEND: POST /api/account/{account_id}/transact angefragt...")

  account = db.get(account_id)
  if not account:
    # 404 Not Found
    print(f"BACKEND: Account {account_id} nicht gefunden (404).")
    abort(404, description=f"Account {account_id} not found.")

  # JSON-Payload aus der Anfrage lesen
  data = request.get_json()
  if not data or 'type' not in data or 'amount' not in data:
    # 400 Bad Request (Payload-Format ungültig)
    print(f"BACKEND: Ungültiger Payload (400).")
    abort(400, description="Invalid payload. 'type' and 'amount' required.")

  try:
    amount = float(data['amount'])
    tx_type = data['type'].upper()
  except ValueError:
    abort(400, description="Invalid amount format.")

  if amount <= 0:
    abort(400, description="Amount must be positive.")

  # Geschäftslogik
  if tx_type == "DEPOSIT":
    account['balance'] += amount
    msg = "Deposit successful"
  elif tx_type == "WITHDRAW":
    if account['balance'] < amount:
      # 400 Bad Request (Geschäftslogik-Fehler)
      print(f"BACKEND: Nicht genügend Deckung für {account_id} (400).")
      abort(400, description="Insufficient funds.")
    account['balance'] -= amount
    msg = "Withdrawal successful"
  else:
    abort(400, description="Invalid transaction type (must be DEPOSIT or WITHDRAW).")

  print(f"BACKEND: Transaktion für {account_id} erfolgreich. Neuer Saldo: {account['balance']}")
  return jsonify({
    "message": msg,
    "account_id": account_id,
    "new_balance": account['balance']
  })


if __name__ == '__main__':
  print("--- Mini-Backend-Server für Banking-App gestartet ---")
  print("Verfügbare Konten: AT123, DE456, CH789")
  print("Server läuft auf http://127.0.0.1:5000")
  print("Drücken Sie STRG+C, um den Server zu beenden.")
  app.run(debug=False, port=5000)
