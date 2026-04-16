# Lab 15: Unittests mit pytest

## Lernziele

In diesem Lab erstellen Sie ein "Sicherheitsnetz" für unsere `BankAccount`-Klasse, um zukünftige
Änderungen (Refactoring) abzusichern.

* Den `pytest`-Standard (anstelle von `unittest`) anwenden.
* Native `assert`-Anweisungen für Tests verwenden.
* Setup-Logik (z.B. das Erstellen von Test-Objekten) in wiederverwendbare Fixtures (`@pytest.fixture`) auslagern.
* Edge Cases (Grenzfälle) effizient mit Parametrisierung (`@pytest.mark.parametrize`) testen.
* (Bonus) Externe Abhängigkeiten (APIs, Services) durch Mocking (`pytest-mock`) isolieren.

## Szenario

Wir haben unsere `BankAccount`-Klasse (aus früheren Labs) erweitert. Sie verfügt nun über eine rudimentäre
Betrugsprüfung (`check_fraud_risk`), die vor einer Abhebung einen (hypothetischen) externen API-Dienst aufruft.

Manuelles Testen ist nicht mehr tragbar. Wir benötigen ein automatisiertes Test-Set, das Folgendes sicherstellt:

1. Die Kernlogik (Einzahlen, Abheben) funktioniert.
2. Fehlerfälle (z.B. negative Beträge) werden korrekt behandelt.
3. Die Tests laufen *schnell* und *isoliert* (ohne echten API-Aufruf).

**Vorbereitung:**
Für dieses Lab benötigen Sie `pytest` und `pytest-mock`:
`pip install pytest pytest-mock`

**Struktur:**
Wir testen die Datei `account.py` (unser "System Under Test" oder SUT). Die Tests schreiben wir in eine separate Datei
namens `test_account.py`.

### Angabe

**Ziel:** Testen Sie die Kernfunktionalität (Erfolg, Fehler, Exceptions) der `BankAccount`-Klasse mithilfe von Fixtures
und `pytest.raises`.

**Datei: `test_account.py`**

1. **Imports:** Importieren Sie `pytest` und die `BankAccount`-Klasse.

2. **Fixture (`@pytest.fixture`)**:

    * Erstellen Sie eine Fixture namens `basic_account`.
    * Diese Funktion soll eine `BankAccount`-Instanz mit 100.0 EUR Guthaben erstellen und zurückgeben (oder `yield`
      en). (z.B. `BankAccount("Max Mustermann", "AT123", 100.0)`)
    * Dies ist Ihr "Arrange"-Schritt (Vorbereitung).

3. **Test 1: Erfolgreiche Abhebung:**

    * Erstellen Sie eine Testfunktion `test_withdraw_success(basic_account)`.
    * Fordern Sie die Fixture an, indem Sie sie als Argument benennen.
    * **Act (Aktion):** Rufen Sie `basic_account.withdraw(60.0)` auf.
    * **Assert (Prüfung):** Verwenden Sie native `asserts`:
        * `assert result is True`
        * `assert basic_account.get_balance() == 40.0`

4. **Test 2: Fehler (Nicht genügend Deckung):**

    * Erstellen Sie `test_withdraw_insufficient_funds(basic_account)`.
    * **Act:** Rufen Sie `basic_account.withdraw(110.0)` auf (mehr als vorhanden).
    * **Assert:**
        * `assert result is False`
        * `assert basic_account.get_balance() == 100.0` (Der Saldo darf sich nicht geändert haben).

5. **Test 3: Exception (Ungültiger Betrag):**

    * Erstellen Sie `test_withdraw_negative_amount(basic_account)`.
    * Die `withdraw`-Methode soll (laut Anforderung) einen `ValueError` auslösen, wenn der Betrag negativ ist.
    * **Act/Assert (kombiniert):** Verwenden Sie den `pytest.raises`-Kontextmanager, um zu prüfen, ob die Exception
      ausgelöst wird:
      ```python
      with pytest.raises(ValueError) as e:
          basic_account.withdraw(-50.0)

      # Optional: Prüfen Sie die Fehlermeldung
      assert "must be positive" in str(e.value)
      ```
    * **Assert:** `assert basic_account.get_balance() == 100.0` (Saldo unverändert).

-----

### Bonus-Herausforderung

**Ziel:** Führen Sie die Tests mithilfe von Parametrisierung (DRY) zusammen und isolieren Sie die externe
Betrugsprüfungs-API durch Mocking.

**Datei: `test_account.py`**

1. **Parametrisierung (`@pytest.mark.parametrize`)**:

    * Ändern Sie die Tests 1 und 2 (Erfolg/Fehler) aus der Angabe in *eine einzige* Testfunktion:
      `test_withdraw_parametrized(basic_account, withdraw_amount, expected_result, expected_balance)`.
    * Verwenden Sie den `@pytest.mark.parametrize`-Dekorator, um die folgenden Fälle zu testen:
        * `(60.0, True, 40.0)` (Erfolg)
        * `(100.0, True, 0.0)` (Erfolg, genau 0)
        * `(100.1, False, 100.0)` (Fehler, nicht gedeckt)

2. **Mocking (Externe Abhängigkeit isolieren)**:

    * Unsere (hypothetische) SUT `account.py` importiert einen Service: `from external_services import check_risk` und
      ruft `check_risk(...)` auf.
    * **Test 1 (Mocking - Fraud Alert):**
        * Erstellen Sie `test_withdraw_fraud_alert(basic_account, mocker)`. (Die `mocker`-Fixture kommt von
          `pytest-mock`).
        * **Arrange (Mock):** Patchen Sie den externen Service, sodass er "hohes Risiko" (z.B. `0.9`) zurückgibt.
          `mocker.patch('account.check_risk', return_value=0.9)`
        * **Act/Assert:** Prüfen Sie, ob die `withdraw`-Funktion (die intern `check_risk` aufruft) nun eine
          `PermissionError` auslöst (wie in der SUT-Logik definiert).
          `with pytest.raises(PermissionError, match="Fraud Alert"):`
          `     basic_account.withdraw(50.0) `
    * **Test 2 (Mocking - Erfolg und Call-Prüfung):**
        * Erstellen Sie `test_withdraw_fraud_check_pass(basic_account, mocker)`.
        * **Arrange (Mock):** Patchen Sie den Service, sodass er "geringes Risiko" (`0.1`) zurückgibt.
          `mock_api = mocker.patch('account.check_risk', return_value=0.1)`
        * **Act:** Führen Sie eine normale Abhebung durch: `basic_account.withdraw(50.0)`.
        * **Assert:**
            * `assert basic_account.get_balance() == 50.0` (Der Test ist bestanden).
            * **WICHTIG (Mock-Prüfung):** Stellen Sie sicher, dass die API *tatsächlich* mit den korrekten Daten
              aufgerufen wurde:
              `mock_api.assert_called_once_with("AT123", 50.0)`

## `external_services.py` (System Under Test)

```python
def check_risk(acc_id, amount):
  # response = requests.post("example.com", {'acc_id': acc_id, 'amount': amount})
  return 0.5
```