import datetime  # 1. Importiert


class Account:
  """
  Stellt ein einfaches Bankkonto dar.
  (Version von Lab 1, erweitert um Logging)
  """

  def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
    self.account_number = account_number
    self.account_holder = account_holder
    self._balance = initial_balance

    # 2. Neues Attribut für den Log-Dateipfad
    self.log_file_path = f"log_account_{self.account_number}.txt"

    # Initial-Log beim Erstellen des Kontos
    self._log_transaction(f"Konto erstellt mit Startsaldo: {initial_balance:.2f} EUR")

  # 3. Neue "protected" Logging-Methode
  def _log_transaction(self, message: str):
    """
    Schreibt eine Nachricht mit Zeitstempel in die Log-Datei des Kontos.
    Verwendet einen Context Manager (with).
    """
    # Zeitstempel im ISO-Format (z.B. '2025-11-03T14:30:05.123456')
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}\n"

    with open(self.log_file_path, mode="a", encoding="utf-8") as f:
      f.write(log_entry)

  def deposit(self, amount: float) -> bool:
    if amount > 0:
      self._balance += amount
      print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
      # 4. Logging integrieren
      self._log_transaction(f"Einzahlung: +{amount:.2f} EUR. Neuer Saldo: {self._balance:.2f} EUR")
      return True
    else:
      print("Einzahlungsbetrag muss positiv sein.")
      self._log_transaction(f"Einzahlung fehlgeschlagen (Betrag: {amount:.2f} EUR)")
      return False

  def withdraw(self, amount: float) -> bool:
    if amount <= 0:
      print("Abhebungsbetrag muss positiv sein.")
      self._log_transaction(f"Abhebung fehlgeschlagen (Betrag: {amount:.2f} EUR)")
      return False

    if self._balance >= amount:
      self._balance -= amount
      print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
      # 4. Logging integrieren
      self._log_transaction(f"Abhebung: -{amount:.2f} EUR. Neuer Saldo: {self._balance:.2f} EUR")
      return True
    else:
      print(f"Abhebung fehlgeschlagen. Nicht genügend Guthaben.")
      # 4. Logging integrieren
      self._log_transaction(f"Abhebung fehlgeschlagen (Guthaben: {self._balance:.2f} EUR, Betrag: {amount:.2f} EUR)")
      return False

  def get_balance(self) -> float:
    return self._balance

  def __str__(self) -> str:
    return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self._balance:.2f} EUR"