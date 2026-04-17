import logging

# Regel 2: Logger auf Modulebene holen.
# __name__ wird hier zu "account"
log = logging.getLogger(__name__)


class BankAccount:
  """
  Stellt ein Bankkonto dar.
  Verwendet 'logging' statt 'print'.
  """

  def __init__(self, owner: str, account_number: str, balance: float):
    self.owner = owner
    self.account_number = account_number
    self._balance = balance

    # Info-Log (verwendet %-Formatierung für Performance)
    log.info("Konto %s für %s erstellt.", self.account_number, self.owner)

  def withdraw(self, amount: float) -> bool:
    """Hebt Geld ab."""
    if amount > self._balance:
      # Ersetzt 'print' durch 'log.warning'
      log.warning(
        "Nicht genügend Deckung für Konto %s (Saldo: %f, Abhebung: %f)",
        self.account_number, self._balance, amount
      )
      return False

    self._balance -= amount
    # Debug-Logs sind detaillierter und oft standardmäßig ausgeblendet
    log.debug("Abhebung von %f EUR von %s erfolgreich.", amount, self.account_number)
    return True

  def calculate_internal_risk_score(self, divisor: int) -> float:
    """
    Eine fehleranfällige Funktion, um ZeroDivisionError zu provozieren.
    """
    log.debug("Berechne Risikoscore mit Divisor %d", divisor)
    return self._balance / divisor
