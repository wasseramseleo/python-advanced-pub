# Lab 12: Die `requests`-Bibliothek

## Lernziele

In diesem Lab lernen Sie, wie Sie mit Python Daten von einer externen API (unserem Banking-Backend) abrufen und dorthin senden.

  * Einfache `GET`-Anfragen (Daten abrufen) und `POST`-Anfragen (Daten senden) durchführen.
  * Die `json`-Antwort einer API parsen.
  * Robusten Code schreiben, der `timeout` verwendet, um Hängenbleiben zu verhindern.
  * `response.raise_for_status()` in einem `try...except`-Block verwenden, um HTTP-Fehler (4xx/5xx) korrekt abzufangen.
  * `requests.Session` für Performance-Vorteile und Cookie-Management bei mehreren Anfragen verwenden.

## Szenario

Unsere Banking-App ist keine monolithische Anwendung. Die Kontoverwaltung läuft als separater "Microservice" (eine API). Ihre Aufgabe ist es, einen Python-Client zu schreiben, der mit dieser API über HTTP kommuniziert, um Kontodaten abzurufen und Transaktionen durchzuführen.

**WICHTIG:** Für dieses Lab muss der `Lab_12_Backend.py`-Server in einem separaten Terminal laufen\!

Starten Sie den Server (z.B. in `cmd` oder `powershell`):
`python Lab_12_Backend.py`

Der Server läuft dann unter `http://127.0.0.1:5000`.

### Angabe

**Ziel:** Rufen Sie Kontoinformationen mit `requests.get()` robust ab.

Erstellen Sie eine Funktion `get_account_details(account_id: str) -> dict | None`.

1.  **Imports:** Importieren Sie `requests` und `requests.exceptions`.
2.  **Basis-URL:** Definieren Sie die URL (z.B. `BASE_URL = "http://127.0.0.1:5000"`). Die Ziel-URL ist `f"{BASE_URL}/api/account/{account_id}"`.
3.  **Fehlerbehandlung:** Implementieren Sie einen `try...except requests.exceptions.RequestException as e:`-Block.
4.  **Anfrage (`try`-Block):**
      * Führen Sie `requests.get(...)` aus.
      * **Timeout:** Setzen Sie ein `timeout` von 1.0 Sekunden.
      * **Fehler-Prüfung:** Rufen Sie `response.raise_for_status()` auf. Dies löst eine Exception aus, wenn der Server einen 4xx- (z.B. 404 Not Found) oder 5xx-Fehler zurückgibt.
      * **Erfolg:** Wenn kein Fehler auftritt, parsen Sie die JSON-Antwort mit `response.json()` und geben Sie das resultierende Dictionary zurück.
5.  **Fehlerfall (`except`-Block):**
      * Geben Sie eine Fehlermeldung aus (z.B. `print(f"Fehler beim Abruf von {account_id}: {e}")`).
      * Geben Sie `None` zurück.

**Testen:**
Rufen Sie Ihre Funktion mit den folgenden IDs auf und geben Sie die Ergebnisse aus:

  * `get_account_details("AT123")` (Sollte die Kontodaten von Max Mustermann liefern)
  * `get_account_details("AT999")` (Sollte einen 404-Fehler auslösen und `None` zurückgeben)

-----

### Bonus-Herausforderung

**Ziel:** Führen Sie mehrere Transaktionen effizient mit einem `requests.Session`-Objekt durch.

Eine `Session` ist schneller, wenn mehrere Anfragen an dieselbe Domain gesendet werden (Connection Pooling).

1.  **Funktion `perform_transaction`:**
      * Erstellen Sie eine Funktion `perform_transaction(session: requests.Session, account_id: str, tx_type: str, amount: float) -> dict | None`.
      * Die Funktion soll (ähnlich der Angabe) `session.post(...)` verwenden, um den Endpoint `f"{BASE_URL}/api/account/{account_id}/transact` anzusprechen.
      * **Payload:** Die `POST`-Anfrage muss die Daten als JSON senden. Verwenden Sie das `json`-Argument: `json={'type': tx_type, 'amount': amount}`.
      * **Robustheit:** Verwenden Sie ebenfalls `timeout`, `raise_for_status` und `try...except`.

**Testen:**
Erstellen Sie einen `requests.Session`-Kontext und führen Sie mehrere Operationen *innerhalb* dieses Kontexts mit derselben Session durch.

```python
BASE_URL = "http://127.0.0.1:5000"

# (Definition von get_account_details und perform_transaction hier)

with requests.Session() as s:
    print("--- Bonus-Herausforderung Test ---")
    
    # Startsaldo prüfen (kann die Funktion aus der Angabe wiederverwenden)
    start_data = get_account_details("DE456") # (Oder passen Sie sie an, um die Session 's' zu nutzen)
    if start_data:
        print(f"Startsaldo (DE456): {start_data['balance']} EUR")

    # 1. Einzahlung
    print("Führe Einzahlung 500 EUR durch...")
    data1 = perform_transaction(s, "DE456", "DEPOSIT", 500)
    if data1:
        print(f"Neuer Saldo: {data1['new_balance']}")

    # 2. Abhebung
    print("Führe Abhebung 200 EUR durch...")
    data2 = perform_transaction(s, "DE456", "WITHDRAW", 200)
    if data2:
        print(f"Neuer Saldo: {data2['new_balance']}")

    # 3. Fehler-Test (Nicht genügend Deckung)
    print("Führe Abhebung 9999 EUR durch (sollte fehlschlagen)...")
    data3 = perform_transaction(s, "DE456", "WITHDRAW", 9999)
    if not data3:
        print("Transaktion wie erwartet fehlgeschlagen.")
```

