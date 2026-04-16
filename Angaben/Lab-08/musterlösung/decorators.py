import time
from functools import wraps


# --- Definition des Dekorators ---

def log_function_call(func):
  """
  Ein Dekorator, der den Aufruf einer Funktion protokolliert,
  inklusive Argument-Handling, Rückgabewerten und Metadaten.
  """

  @wraps(func)  # 4. Metadaten erhalten (von func auf wrapper kopieren)
  def wrapper(*args, **kwargs):
    """Der Wrapper, der die eigentliche Logik ausführt."""

    # 3a. Logik VOR dem Aufruf
    print(f"LOG: Calling function '{func.__name__}'...")

    # 2. Aufruf der Originalfunktion mit allen Argumenten
    # 3b. Rückgabewert speichern
    result = func(*args, **kwargs)

    # 3c. Logik NACH dem Aufruf
    print(f"LOG: Function '{func.__name__}' finished.")

    # 3d. Rückgabewert zurückgeben
    return result

  # 5. Der Dekorator gibt den Wrapper zurück
  return wrapper


@log_function_call
def deposit(account_id: str, amount: float) -> str:
  """
  Simuliert eine Einzahlung auf ein Konto.
  Gibt einen Erfolgs-String zurück.
  """
  print(f"  -> Processing deposit: {amount} EUR for Account {account_id}")
  time.sleep(0.5)  # Simuliert Arbeitsaufwand
  return f"Success: {amount} deposited."


@log_function_call
def get_balance(account_id: str) -> float:
  """
  Simuliert die Abfrage eines Kontostands.
  Gibt einen simulierten Kontostand zurück.
  """
  print(f"  -> Fetching balance for Account {account_id}")
  return 1000.00