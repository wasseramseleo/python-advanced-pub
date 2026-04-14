class BankingError(Exception):
  """
  Basis-Exception für alle Fehler in unserer Bank-App.
  Alle spezifischen Bank-Fehler sollten hiervon erben.
  """
  pass


class InvalidAmountError(BankingError):
  """
  Wird ausgelöst, wenn ein Transaktionsbetrag ungültig ist (z.B. <= 0).
  Erbt von BankingError.
  """
  pass


class InsufficientFundsError(BankingError):
  """
  Wird ausgelöst, wenn das Guthaben für eine Abhebung nicht ausreicht.
  Erbt von BankingError.
  """
  pass

class FraudServiceError(BankingError):
  """
  Wird ausgelöst, wenn der externe Betrugsprüfungs-Dienst ausfällt.
  """
  pass