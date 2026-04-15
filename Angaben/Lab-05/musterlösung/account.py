from account_history_iterator import AccountHistoryIterator

class BankAccount:
  """
  Stellt ein Bankkonto dar, das (intern) eine Liste von Transaktionen hält.
  Diese Klasse ist ein "Iterable".
  """

  def __init__(self, owner: str, account_number: str):
    self.owner = owner
    self.account_number = account_number
    self.__transactions = []

  def deposit(self, amount: float):
    self.__transactions.append(f"DEPOSIT: {amount} EUR")

  def withdraw(self, amount: float):
    self.__transactions.append(f"WITHDRAW: {amount} EUR")

  def get_transactions(self) -> list:
    return self.__transactions.copy()

  def __iter__(self):
    """
    Gibt ein Iterator-Objekt zurück.
    Dies macht BankAccount zu einem "Iterable".
    """
    print("LOG: BankAccount.__iter__ aufgerufen. Erzeuge neuen Iterator.")
    return AccountHistoryIterator(self.__transactions)

