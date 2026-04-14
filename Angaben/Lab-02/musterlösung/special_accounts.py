from account import Account

class SavingsAccount(Account):
  """
  Ein Sparkonto, das von Account erbt.
  Fügt Zinsberechnung hinzu.
  """
  def __init__(self, account_number: str, account_holder: str,
               initial_balance: float = 0.0, interest_rate: float = 0.01):
    """
    Initialisiert das Sparkonto.

    Args:
        interest_rate (float): Der Zinssatz als Dezimalzahl (z.B. 0.02 für 2%).
    """
    # 3. Aufruf des Konstruktors der Basisklasse (Account)
    # Dies ist entscheidend, damit self.account_number,
    # self.account_holder und self._balance initialisiert werden.
    super().__init__(account_number, account_holder, initial_balance)

    # 3. Neues, spezifisches Attribut für diese Subklasse
    self.interest_rate = interest_rate
    print(f"Sparkonto {self.account_number} mit {self.interest_rate * 100}% Zinsen erstellt.")

  def apply_interest(self):
    """
    Berechnet die Zinsen auf den aktuellen Saldo
    und fügt sie dem Konto hinzu.
    """
    # Wir greifen auf _balance zu (geerbt) und self.interest_rate (eigen)
    interest_amount = self._balance * self.interest_rate

    if interest_amount > 0:
      print(f"Rechne Zinsen an: {interest_amount:.2f} EUR")
      # 4. Wir verwenden die geerbte 'deposit'-Methode
      self.deposit(interest_amount)
    else:
      print("Keine Zinsen angerechnet (Guthaben zu gering).")

  def __format__(self, format_spec):
    if format_spec == 'euro':
      return f"{self._balance}€"
    elif format_spec == 'usd':
      return f"{self._balance}$"
    else:
      return f"{self._balance}"


class CheckingAccount(Account):
  """
  Ein Girokonto, das von Account erbt.
  Erweitert 'withdraw' um einen Überziehungskredit (Dispo).
  """

  def __init__(self, account_number: str, account_holder: str,
               initial_balance: float = 0.0, overdraft_limit: float = 500.0):
    """
    Initialisiert das Girokonto.

    Args:
        overdraft_limit (float): Der Überziehungsrahmen (Dispo).
    """
    # 1. Aufruf des Basis-Konstruktors
    super().__init__(account_number, account_holder, initial_balance)

    # 1. Speichern des neuen Attributs
    self._overdraft_limit = overdraft_limit
    print(f"Girokonto {self.account_number} mit {self._overdraft_limit:.2f} EUR Dispo erstellt.")

  # 2. Überschreiben (Override) der 'withdraw' Methode
  def withdraw(self, amount: float) -> bool:
    """
    Hebt einen Betrag vom Konto ab.
    Berücksichtigt den Überziehungskredit (Dispo).
    """
    if amount <= 0:
      print("Abhebungsbetrag muss positiv sein.")
      return False

    # 2. Geänderte Logik: Prüft Saldo + Dispo
    available_funds = self._balance + self._overdraft_limit

    if available_funds >= amount:
      # Abhebung ist ok, auch wenn Saldo negativ wird
      self._balance -= amount
      print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
      print(f"Neuer Kontostand: {self._balance:.2f} EUR")
      return True
    else:
      # Nicht mal der Dispo reicht aus
      print(f"Abhebung fehlgeschlagen. Verfügbares Limit ({available_funds:.2f} EUR) überschritten.")
      return False
