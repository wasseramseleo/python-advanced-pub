import logging
from external_services import check_risk

log = logging.getLogger(__name__)


class BankAccount:
  """
  Repräsentiert ein Bankkonto mit Betrugsprüfung.
  """

  def __init__(self, owner: str, account_number: str, balance: float):
    self.owner = owner
    self.account_number = account_number
    self._balance = balance
    log.info(f"Konto {self.account_number} erstellt.")

  def get_balance(self) -> float:
    """Gibt den aktuellen Saldo zurück."""
    return self._balance

  def deposit(self, amount: float) -> bool:
    """Zahlt Geld ein."""
    if amount <= 0:
      raise ValueError("Einzahlungsbetrag muss positiv sein")
    self._balance += amount
    return True

  def check_fraud_risk(self, amount: float):
    """
    Ruft einen externen Service auf, um das Betrugsrisiko zu prüfen.
    (Diese Methode werden wir mocken)
    """
    log.debug(f"Prüfe Betrugsrisiko für {self.account_number}...")

    # --- Externer Aufruf ---
    risk_level = check_risk(self.account_number, amount)
    # ----------------------

    if risk_level > 0.8:
      log.warning(f"FRAUD ALERT für {self.account_number}")
      raise PermissionError("Fraud Alert: Transaktion blockiert")
    log.debug("Betrugsprüfung bestanden.")

  def withdraw(self, amount: float) -> bool:
    """
    Hebt Geld ab, nach Prüfung von Regeln und Betrugs-API.
    """
    if amount <= 0:
      raise ValueError("Abhebungsbetrag muss positiv sein")

    # Aufruf der (externen) Betrugsprüfung
    self.check_fraud_risk(amount)

    if amount > self._balance:
      log.warning(f"Nicht genügend Deckung für {self.account_number}")
      return False

    self._balance -= amount
    return True