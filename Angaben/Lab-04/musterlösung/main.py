from account import Account
from exceptions import InvalidAmountError, InsufficientFundsError, BankingError


def perform_transaction(account: Account, action: str, amount: float):
  """
  Führt eine Transaktion aus und fängt bekannte Bank-Fehler ab.
  """
  print(f"\nVersuche {action} von {amount:.2f} EUR...")

  try:
    # 3. Der 'try'-Block
    if action == "deposit":
      account.deposit(amount)
    elif action == "withdraw":
      account.withdraw(amount)
    else:
      print("Unbekannte Aktion.")
      return

  # 3. Spezifische 'except'-Blöcke
  except InvalidAmountError as e:
    print(f"[FEHLER] Transaktion (ungültiger Betrag) fehlgeschlagen: {e}")

  except InsufficientFundsError as e:
    print(f"[FEHLER] Transaktion (Guthaben) abgelehnt: {e}")

  except BankingError as e:
    # Fängt alle anderen Fehler auf, die von BankingError erben
    print(f"[FEHLER] Allgemeiner Bankfehler: {e}")


# --- Test-Szenarien ---
acc1 = Account("AT001", "Max Mustermann", 500.0)
print(acc1)

# Szenario 1: Erfolgreiche Abhebung
perform_transaction(acc1, "withdraw", 100.0)  # Sollte klappen

# Szenario 2: Fehlgeschlagen (Guthaben)
perform_transaction(acc1, "withdraw", 1000.0)  # Sollte InsufficientFundsError auslösen

# Szenario 3: Fehlgeschlagen (Betrag)
perform_transaction(acc1, "deposit", -50.0)  # Sollte InvalidAmountError auslösen

# Szenario 4: Erfolgreiche Einzahlung
perform_transaction(acc1, "deposit", 200.0)

print(f"\nEndgültiger Saldo: {acc1.get_balance():.2f} EUR")  # Erwartet: 500-100+200 = 600