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

@pytest.fixture
def another_basic_account() -> BankAccount:
  """
  Fixture: Stellt ein sauberes Konto-Objekt mit 100.0
  Guthaben für jeden Test bereit.
  """
  print("n  (SETUP FIXTURE: Erstelle basic_account mit 100.0)")
  return BankAccount("Max Mustermann", "DE388", 0.0)


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
def test_withdraw_parametrized(another_basic_account, withdraw_amount, expected_result, expected_balance):
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