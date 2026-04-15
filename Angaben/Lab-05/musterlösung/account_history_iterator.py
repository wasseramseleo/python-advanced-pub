class AccountHistoryIterator:
  """
  Dies ist der "Iterator". Er hält den Zustand der Iteration.
  """

  def __init__(self, transactions: list):
    self._transactions = transactions
    self._index = 0

  def __iter__(self):
    """Iteratoren geben sich selbst zurück."""
    return self

  def __next__(self):
    """Gibt das nächste Element zurück oder löst StopIteration aus."""
    if self._index >= len(self._transactions):
      # Ende der Liste erreicht
      print("LOG: AccountHistoryIterator.StopIteration ausgelöst.")
      raise StopIteration
    else:
      # Daten zurückgeben und Index für nächsten Aufruf erhöhen
      current_transaction = self._transactions[self._index]
      self._index += 1
      return current_transaction