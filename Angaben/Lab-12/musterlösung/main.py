import requests
import requests.exceptions  # Import für spezifische Fehlerbehandlung

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