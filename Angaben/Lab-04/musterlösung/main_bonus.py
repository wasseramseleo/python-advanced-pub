from account import Account
from exceptions import InvalidAmountError, InsufficientFundsError, BankingError, FraudServiceError


def perform_transaction_robust(account: Account, action: str, amount: float):
  """
  Führt eine Transaktion aus und verwendet den vollständigen
  try...except...else...finally Block.

  Simuliert auch Exception Chaining.
  """
  print(f"\n>>> Versuche {action} von {amount:.2f} EUR...")

  try:
    # 2. Simulation für Exception Chaining
    if action == "withdraw" and amount > 400:  # Prüfung für "große" Abhebungen
      print("Prüfe Transaktion mit externem Fraud-Service...")
      try:
        # Simulierter Aufruf, der fehlschlägt
        raise TimeoutError("Externer Fraud-Service (FS-1) antwortet nicht nach 30s")

      except TimeoutError as e:
        # 2. EXCEPTION CHAINING:
        # Wir fangen den technischen Fehler (TimeoutError)
        # und 'verpacken' ihn in unseren App-spezifischen Fehler (FraudServiceError).
        # 'from e' erhält den ursprünglichen Stack Trace.
        raise FraudServiceError("Betrugsprüfung konnte nicht durchgeführt werden") from e

    # Normale Transaktionslogik
    if action == "deposit":
      account.deposit(amount)
    elif action == "withdraw":
      account.withdraw(amount)
    else:
      print("Unbekannte Aktion.")
      return

  # --- Exception Handling ---
  except InvalidAmountError as e:
    print(f"[FEHLER] Transaktion (ungültiger Betrag) fehlgeschlagen: {e}")

  except InsufficientFundsError as e:
    print(f"[FEHLER] Transaktion (Guthaben) abgelehnt: {e}")

  except FraudServiceError as e:
    # Abfangen des 'chained' Error
    print(f"[FEHLER] Transaktion (Sicherheit) blockiert: {e}")
    # Wenn man den Fehler mit Traceback loggen würde, sähe man auch die 'TimeoutError'
    if e.__cause__:
      print(f"   |-> Ursache: {e.__cause__}")

  except BankingError as e:
    print(f"[FEHLER] Allgemeiner Bankfehler: {e}")

  # 1. 'else'-Block
  else:
    # Wird NUR ausgeführt, wenn im 'try'-Block KEINE Exception aufgetreten ist.
    print(f"[ERFOLG] Transaktion verbucht. Neuer Saldo: {account.get_balance():.2f} EUR")

  # 1. 'finally'-Block
  finally:
    # Wird IMMER ausgeführt, egal ob try, except oder else lief.
    print(f"--- Transaktionsverarbeitung für Konto {account.account_number} abgeschlossen ---")


# --- Test-Szenarien ---
print("--- Starte Bonus-Tests ---")
acc1 = Account("AT001", "Max Mustermann", 500.0)

# Szenario 1: Erfolg (trifft 'else' und 'finally')
perform_transaction_robust(acc1, "withdraw", 100.0)  # Saldo: 400

# Szenario 2: Fehler (trifft 'except InsufficientFundsError' und 'finally')
perform_transaction_robust(acc1, "withdraw", 800.0)

# Szenario 3: Chaining-Fehler (trifft 'except FraudServiceError' und 'finally')
# (Betrag > 400 löst die Simulation aus)
perform_transaction_robust(acc1, "withdraw", 401.0)

# Szenario 4: Erfolg (trifft 'else' und 'finally')
perform_transaction_robust(acc1, "deposit", 150.0)  # Saldo: 550

print(f"\nEndgültiger Saldo: {acc1.get_balance():.2f} EUR")  # Erwartet: 500-100+150 = 550