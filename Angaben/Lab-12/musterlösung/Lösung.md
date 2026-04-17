# Lab 12: Die `requests`-Bibliothek - Lösung

## Erläuterung der Lösung

### Basis-Aufgabe

Die Funktion `get_account_details` demonstriert robusten Code für `GET`-Anfragen.

1.  **`requests.get`**: Sendet die HTTP-GET-Anfrage an die konstruierte URL.
2.  **`timeout=1.0`**: Dies ist entscheidend. Es bedeutet, dass der Client maximal 1.0 Sekunde auf eine *Antwort* vom Server wartet. Der Test-Backend-Server hat eine künstliche Verzögerung von 0.5s; wenn der Timeout auf 0.3s gesetzt würde, würde die Anfrage fehlschlagen.
3.  **`try...except RequestException`**: Dies ist ein "Catch-all" für alle Fehler, die `requests` auslösen kann (Netzwerkfehler, Verbindungsfehler, DNS-Fehler, Timeout-Fehler).
4.  **`response.raise_for_status()`**: Dies ist der wichtigste Schritt zur Fehlerprüfung. Wenn die Anfrage erfolgreich war (HTTP 200 OK), tut diese Methode nichts. Wenn der Server jedoch einen Fehler meldet (z.B. 404 Not Found, 500 Internal Server Error, 403 Forbidden), löst diese Methode eine `HTTPError`-Exception aus, die vom `try...except`-Block abgefangen wird.
5.  **`response.json()`**: Parst den JSON-Text der Antwort in ein Python-Dictionary.

### Bonus-Herausforderung

Die Bonus-Herausforderung implementiert `POST`-Anfragen innerhalb einer `requests.Session`.

1.  **`with requests.Session() as s:`**: Erstellt ein Session-Objekt. Innerhalb dieses Blocks werden Verbindungen zur Domain (`127.0.0.1:5000`) offengehalten (Connection Pooling). Dies ist bei mehreren aufeinanderfolgenden Anfragen (wie Einzahlung, Abhebung) deutlich performanter als einzelne `requests.post()`-Aufrufe.
2.  **`session.post(...)`**: Die `perform_transaction`-Funktion erhält das Session-Objekt `s` und verwendet dessen `.post()`-Methode.
3.  **`json={'type': ...}`**: Das `json`-Argument ist der Standardweg, um Daten in einer `POST`-Anfrage zu senden. `requests` serialisiert das Python-Dictionary automatisch in einen JSON-String und setzt den `Content-Type: application/json` Header.
4.  **Fehlerbehandlung**: Der Backend-Server ist so konfiguriert, dass er einen HTTP 400 (Bad Request) sendet, wenn die Geschäftslogik fehlschlägt (z.B. "Insufficient funds"). Unser `raise_for_status()` fängt diesen 400er-Fehler korrekt ab, und die Funktion gibt `None` zurück.

## Python-Code: Angabe

```python
import requests
import requests.exceptions # Import für spezifische Fehlerbehandlung

# Basis-URL des laufenden Backend-Servers
BASE_URL = "http://127.0.0.1:5000"

def get_account_details(account_id: str) -> dict | None:
    """
    Ruft Kontodetails robust von der API ab.
    
    Args:
        account_id (str): Die ID des Kontos (z.B. "AT123").

    Returns:
        dict | None: Ein Dictionary mit Kontodaten bei Erfolg, sonst None.
    """
    url = f"{BASE_URL}/api/account/{account_id}"
    print(f"ANFRAGE: GET {url}")
    
    try:
        # 1. Anfrage mit Timeout
        response = requests.get(url, timeout=1.0)
        
        # 2. HTTP-Fehler prüfen (4xx oder 5xx)
        response.raise_for_status() 
        
        # 3. Erfolg: JSON parsen und zurückgeben
        return response.json()
        
    except requests.exceptions.Timeout:
        print(f"  FEHLER: Timeout bei Anfrage für {account_id}.")
        return None
    except requests.exceptions.HTTPError as http_err:
        # Spezifische Behandlung für 4xx/5xx Fehler
        print(f"  FEHLER: HTTP-Fehler für {account_id}: {http_err}")
        return None
    except requests.exceptions.RequestException as e:
        # Allgemeiner Fehler (Netzwerk, DNS, etc.)
        print(f"  FEHLER: Allgemeiner Fehler für {account_id}: {e}")
        return None

# --- Test der Angabe ---
print("--- Angabe Test ---")

# 1. Erfolgreicher Abruf
details_ok = get_account_details("AT123")
if details_ok:
    print(f"  ERFOLG (AT123): {details_ok}")

print("-" * 20)

# 2. Fehlerhafter Abruf (404 Not Found)
details_fail = get_account_details("AT999")
if not details_fail:
    print(f"  ERFOLG (AT999): Fehler wie erwartet abgefangen.")

```

## Python-Code: Bonus-Herausforderung

```python
import requests
import requests.exceptions

# (Wir nehmen an, BASE_URL und get_account_details von oben 
# sind hier ebenfalls verfügbar)

def perform_transaction(session: requests.Session, account_id: str, tx_type: str, amount: float) -> dict | None:
    """
    Führt eine Transaktion (POST) innerhalb einer Session durch.
    
    Args:
        session (requests.Session): Das aktive Session-Objekt.
        account_id (str): Die Konto-ID.
        tx_type (str): "DEPOSIT" or "WITHDRAW".
        amount (float): Der Betrag.

    Returns:
        dict | None: Die JSON-Antwort des Servers bei Erfolg, sonst None.
    """
    url = f"{BASE_URL}/api/account/{account_id}/transact"
    payload = {'type': tx_type, 'amount': amount}
    print(f"ANFRAGE: POST {url} (Payload: {payload})")
    
    try:
        # Verwendet die .post()-Methode der Session
        response = session.post(url, json=payload, timeout=1.0)
        
        # HTTP-Fehler prüfen (z.B. 400 bei "Insufficient funds")
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        # Zeigt den 400er-Fehler (Insufficient funds) vom Server an
        print(f"  FEHLER: Transaktion fehlgeschlagen: {http_err}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  FEHLER: Netzwerkfehler bei Transaktion: {e}")
        return None


# --- Test der Bonus-Herausforderung ---
print("\n--- Bonus-Herausforderung Test ---")

# 'with' stellt sicher, dass die Session (und ihre Verbindungen) 
# am Ende geschlossen werden.
with requests.Session() as s:
    
    # Optional: Den 'get_account_details' anpassen, 
    # damit er auch die Session 's' nutzt
    start_data = get_account_details("DE456") # (Oder: s.get(...))
    if start_data:
        print(f"Startsaldo (DE456): {start_data['balance']} EUR")

    # 1. Einzahlung
    print("\nFühre Einzahlung 500 EUR durch...")
    data1 = perform_transaction(s, "DE456", "DEPOSIT", 500)
    if data1:
        print(f"  ERFOLG: Neuer Saldo: {data1['new_balance']}")

    # 2. Abhebung
    print("\nFühre Abhebung 200 EUR durch...")
    data2 = perform_transaction(s, "DE456", "WITHDRAW", 200)
    if data2:
        print(f"  ERFOLG: Neuer Saldo: {data2['new_balance']}")

    # 3. Fehler-Test (Nicht genügend Deckung)
    print("\nFühre Abhebung 9999 EUR durch (sollte fehlschlagen)...")
    data3 = perform_transaction(s, "DE456", "WITHDRAW", 9999)
    if not data3:
        print("  ERFOLG: Transaktion wie erwartet fehlgeschlagen (400 Bad Request).")

    # 4. Fehler-Test (Negativer Betrag)
    print("\nFühre Einzahlung -100 EUR durch (sollte fehlschlagen)...")
    data4 = perform_transaction(s, "DE456", "DEPOSIT", -100)
    if not data4:
        print("  ERFOLG: Transaktion wie erwartet fehlgeschlagen (400 Bad Request).")
```
