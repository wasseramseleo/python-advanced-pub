class Account:
  """
  Stellt ein einfaches Bankkonto dar, das Einzahlungen
  und Abhebungen mit Saldenprüfung verwaltet.
  """

  def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0, is_savings: bool = False, is_giro: bool = True):
    """
    Initialisiert ein neues Konto.

    Args:
        account_number (str): Die eindeutige Kontonummer.
        account_holder (str): Der Name des Kontoinhabers.
        initial_balance (float, optional): Der Startsaldo. Standard ist 0.0.
    """
    self.account_number = account_number
    self.account_holder = account_holder
    # 'Protected' Attribut: Konvention signalisiert,
    # dass dies nicht von außen direkt manipuliert werden sollte.
    self._balance = initial_balance
    self.is_savings = is_savings
    self.is_giro = is_giro

  def deposit(self, amount: float) -> bool:
    """
    Zahlt einen Betrag auf das Konto ein.
    Der Betrag muss positiv sein.
    """
    if amount > 0:
      self._balance += amount
      print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
      return True
    else:
      print("Einzahlungsbetrag muss positiv sein.")
      return False

  def withdraw(self, amount: float) -> bool:
    """
    Hebt einen Betrag vom Konto ab.
    Prüft auf positiven Betrag und ausreichende Deckung.
    """
    if amount <= 0 and not self.is_giro:
      print("Abhebungsbetrag muss positiv sein.")
      return False

    if self._balance >= amount:
      self._balance -= amount
      print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
      return True
    else:
      print(f"Abhebung fehlgeschlagen. Nicht genügend Guthaben. (Stand: {self._balance:.2f} EUR)")
      return False

  def get_balance(self) -> float:
    """
    Gibt den aktuellen Kontostand zurück.
    """
    return self._balance

  def __str__(self) -> str:
    """
    Gibt eine String-Repräsentation des Kontos zurück.
    Wird von print() aufgerufen.
    """
    # Formatiert den Saldo als Währung mit 2 Nachkommastellen
    return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self._balance:.2f} EUR"