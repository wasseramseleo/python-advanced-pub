class Account:
  """
  Erweiterte Version der Account-Klasse mit:
  - Mindestguthaben (Klassen-Attribut)
  - Name Mangling für 'private' Attribute (__balance)
  - Gleichheitsprüfung (__eq__)
  """

  # 1. Klassen-Attribut
  # Gilt für ALLE Instanzen dieser Klasse
  MINIMUM_BALANCE = 0.0

  def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
    self.account_number = account_number
    self.account_holder = account_holder

    # 2. "Private" Attribute (Name Mangling)
    # Python benennt dieses Attribut intern um (z.B. zu _Account__balance)
    if initial_balance < self.MINIMUM_BALANCE:
      raise ValueError(f"Anfangsguthaben darf nicht unter {self.MINIMUM_BALANCE} liegen")
    self.__balance = initial_balance

  def deposit(self, amount: float) -> bool:
    if amount > 0:
      self.__balance += amount
      print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
      return True
    else:
      print("Einzahlungsbetrag muss positiv sein.")
      return False

  def withdraw(self, amount: float) -> bool:
    if amount <= 0:
      print("Abhebungsbetrag muss positiv sein.")
      return False

    # 1. Prüfung gegen MINIMUM_BALANCE
    if (self.__balance - amount) >= self.MINIMUM_BALANCE:
      self.__balance -= amount
      print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
      return True
    else:
      print(
        f"Abhebung fehlgeschlagen. Guthaben nicht ausreichend oder Minimum-Saldo ({self.MINIMUM_BALANCE} EUR) würde unterschritten.")
      return False

  def get_balance(self) -> float:
    # Getter ist notwendig, da __balance 'private' ist
    return self.__balance

  def __str__(self) -> str:
    return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self.__balance:.2f} EUR"

  # 3. Operator Overloading (==)
  def __eq__(self, other) -> bool:
    """
    Prüft, ob zwei Konten 'gleich' sind (basierend auf der Kontonummer).
    """
    if isinstance(other, Account):
      # Wir definieren Gleichheit über die account_number
      return self.account_number == other.account_number
    return False