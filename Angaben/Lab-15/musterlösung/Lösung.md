# Lab 15: Unittests mit pytest - Lösung

## Erläuterung der Lösung

Dieses Lab besteht aus zwei Dateien: dem "System Under Test" (SUT), das wir testen, und der Test-Datei selbst.

### 1. `account.py` (Das System Under Test - SUT)

Diese Datei enthält unsere `BankAccount`-Klasse, die wir testen wollen. Sie wurde (wie in der Anleitung beschrieben) um
eine Abhängigkeit zu einem *hypothetischen* externen Service (`external_services.fraud_api`) erweitert. Wir müssen
diesen Service in unseren Tests "mocken" (simulieren).

### 2. `test_account.py` (Der Test-Code)

#### Angabe

* **`@pytest.fixture` (Arrange):** Die `basic_account`-Fixture ist die "Arrange"-Phase (Vorbereitung). Sie stellt eine
  saubere `BankAccount`-Instanz mit 100.0 Guthaben für *jeden* Test bereit, der sie anfordert. Dies stellt sicher, dass
  Tests isoliert voneinander laufen.
* **Native `assert` (Assert):** `pytest` verwendet native Python `asserts`. `assert basic_account.get_balance() == 40.0`
  ist kürzer und lesbarer als `self.assertEqual(basic_account.get_balance(), 40.0)` (aus `unittest`).
* **`pytest.raises` (Exception-Test):** Der `with pytest.raises(ValueError)`-Block ist der Standardweg, um zu
  *erwarten*, dass eine Codezeile eine Exception auslöst. Der Test schlägt fehl, wenn *keine* `ValueError`-Exception
  ausgelöst wird.

#### Bonus-Herausforderung

* **`@pytest.mark.parametrize` (DRY):** Dieser Dekorator ist die "Don't Repeat Yourself"-Lösung für Tests. Anstatt drei
  separate Testfunktionen für "Erfolg", "Genau Null" und "Fehler" zu schreiben, definieren wir *eine* Testfunktion (
  `test_withdraw_parametrized`) und lassen `pytest` sie dreimal mit den verschiedenen Datensätzen ausführen.
* **Mocking (Isolation):**
    * **`mocker`**: Dies ist eine Fixture von `pytest-mock`, die wir anfordern, um das Patchen (Ersetzen) von
      Objekten/Methoden zur Laufzeit zu ermöglichen.
    * **`mocker.patch(...)`**: Dies ist der Kern des Mockings. Wir weisen `pytest` an, den Pfad `'account.check_risk'`
      abzufangen.
    * **`return_value=0.9`**: Wir simulieren eine API-Antwort. Im Test `test_withdraw_fraud_alert` gibt die API `0.9` (
      hohes Risiko) zurück. Unsere SUT-Logik fängt dies ab und löst einen `PermissionError` aus, den wir mit
      `pytest.raises` erwarten.
    * **`return_value=0.1`**: Im Test `test_withdraw_fraud_check_pass` simulieren wir eine "erfolgreiche" API-Antwort (
      geringes Risiko).
    * **`mock_api.assert_called_once_with(...)`**: Dies ist ein kritischer Test. Wir prüfen nicht nur, ob unser Code
      *funktioniert* (Saldo ist 50.0), sondern auch, ob er sich *korrekt verhalten* hat – hat er die externe API (den
      Mock) *genau einmal* und *mit den korrekten Argumenten* (Konto "AT123", Betrag 50.0) aufgerufen?

## Python-Code 1: `external_services.py` (System Under Test)

```python
def check_risk(acc_id, amount):
  # response = requests.post("example.com", {'acc_id': acc_id, 'amount': amount})
  return 0.5
```

## Python-Code 2: `account.py` (System Under Test)

```python
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
```

## Python-Code 3: `test_account.py` (Test-Datei)

```python
import pytest
from account import BankAccount  # Import des SUT


# --- Angabe ---

@pytest.fixture
def basic_account() -> BankAccount:
  """
  Fixture: Stellt ein sauberes Konto-Objekt mit 100.0
  Guthaben für jeden Test bereit.
  """
  print("n  (SETUP FIXTURE: Erstelle basic_account mit 100.0)")
  return BankAccount("Max Mustermann", "AT123", 100.0)


def test_withdraw_success(basic_account):
  """
  Testet eine normale, erfolgreiche Abhebung.
  """
  # Act
  result = basic_account.withdraw(60.0)

  # Assert
  assert result is True
  assert basic_account.get_balance() == 40.0


def test_withdraw_insufficient_funds(basic_account):
  """
  Testet eine Abhebung, die wegen mangelnder Deckung fehlschlägt.
  """
  # Act
  result = basic_account.withdraw(110.0)

  # Assert
  assert result is False
  assert basic_account.get_balance() == 100.0  # Saldo muss unverändert sein


def test_withdraw_negative_amount(basic_account):
  """
  Testet, ob eine negative Abhebung einen ValueError auslöst.
  """
  # Act & Assert (kombiniert)
  with pytest.raises(ValueError) as e:
    basic_account.withdraw(-50.0)

  # Optionale Prüfung der Fehlermeldung
  assert "muss positiv sein" in str(e.value)
  # Saldo muss unverändert sein
  assert basic_account.get_balance() == 100.0


@pytest.mark.parametrize(
  "withdraw_amount, expected_result, expected_balance",
  [
    (60.0, True, 40.0),  # Fall 1: Erfolg
    (100.0, True, 0.0),  # Fall 2: Erfolg (genau 0)
    (100.1, False, 100.0)  # Fall 3: Fehler (nicht gedeckt)
  ]
)
def test_withdraw_parametrized(basic_account, withdraw_amount, expected_result, expected_balance):
  """
  Testet mehrere Abhebe-Szenarien mit Parametrisierung.
  """
  result = basic_account.withdraw(withdraw_amount)
  assert result is expected_result
  assert basic_account.get_balance() == expected_balance


def test_withdraw_fraud_alert(basic_account, mocker):
  """
  Testet (mittels Mocking), dass eine 'PermissionError' ausgelöst wird,
  wenn der Fraud-Service 'hohes Risiko' (0.9) meldet.
  """
  # Arrange (Mock): Ersetze den API-Aufruf, return_value=0.9
  mocker = mocker.patch(
    'account.check_risk',
    return_value=0.9
  )

  # Act & Assert
  with pytest.raises(PermissionError, match="Fraud Alert"):
    basic_account.withdraw(50000.0)

  # Saldo muss unverändert sein, da die Transaktion blockiert wurde
  assert basic_account.get_balance() == 100.0


def test_withdraw_fraud_check_pass(basic_account, mocker):
  """
  Testet (mittels Mocking), dass eine Abhebung normal funktioniert,
  wenn der Fraud-Service 'geringes Risiko' (0.1) meldet.
  Prüft auch, ob der Mock korrekt aufgerufen wurde.
  """
  # Arrange (Mock): Ersetze den API-Aufruf, return_value=0.1
  mocker = mocker.patch(
    'account.check_risk',
    return_value=0.1
  )

  # Act
  result = basic_account.withdraw(50.0)

  # Assert (Logik)
  assert result is True
  assert basic_account.get_balance() == 50.0

  # Assert (Mock-Verhalten)
  # Wurde der (gemockte) API-Call genau 1x aufgerufen?
  # ... mit den korrekten Argumenten?
  mocker.assert_called_once_with("AT123", 50.0)
```