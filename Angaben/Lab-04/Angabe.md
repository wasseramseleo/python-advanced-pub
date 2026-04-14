## Lab 4: Exceptions – Robuste Transaktionsverarbeitung

In unseren bisherigen Labs haben die Methoden `deposit` und `withdraw` bei Fehlern (z.B. mangelnde Deckung) `False` zurückgegeben oder einfach eine Nachricht gedruckt. In großen Anwendungen ist dies unzureichend.

Wenn eine Transaktion fehlschlägt, muss der aufrufende Code (z.B. das App-Frontend) *genau* wissen, *warum* sie fehlschlug. War der Betrag ungültig? War das Konto nicht gedeckt? War ein externer Dienst nicht verfügbar?

Wir werden nun unsere `Account`-Klasse (basierend auf Lab 1 oder 3) so umgestalten, dass sie bei Fehlern spezifische **Exceptions** auslöst (`raise`). Der aufrufende Code lernt, diese Fehler mit `try...except...else...finally` elegant zu behandeln.

### Lernziele

  * Die Syntax von `try...except...else...finally` verstehen und anwenden.
  * Spezifische Exceptions (z.B. `ValueError`) statt allgemeiner (`Exception`) abfangen.
  * Eigene, domänenspezifische Exception-Hierarchien definieren.
  * Exceptions auslösen (`raise`) statt Fehler-Codes (wie `False`) zurückzugeben.

### Szenario

Wir müssen die Transaktionslogik unserer Bank-App "produktionsreif" machen.

1.  **Eigene Exceptions:** Wir definieren eine eigene Fehlerhierarchie (z.B. `BankingError`), um alle bankspezifischen Probleme zu kategorisieren.
2.  **Refactoring:** Wir passen `Account.deposit()` und `Account.withdraw()` an. Statt `False` zurückzugeben, lösen sie `InvalidAmountError` oder `InsufficientFundsError` aus.
3.  **Handler:** Der aufrufende Code (unsere `main.py`) muss diese Fehler nun abfangen und dem "Benutzer" (via `print`) eine klare Rückmeldung geben.

-----

### Angabe: Von Fehler-Codes zu Exceptions

1.  **Datei `exceptions.py` erstellen:**

      * Erstellen Sie eine neue Datei `exceptions.py`.
      * Definieren Sie darin eine Basis-Exception:
        ```python
        class BankingError(Exception):
            """Basis-Exception für alle Fehler in unserer Bank-App."""
            pass
        ```
      * Definieren Sie zwei spezifische Exceptions, die von `BankingError` erben:
        ```python
        class InvalidAmountError(BankingError):
            """Wird ausgelöst, wenn ein Transaktionsbetrag ungültig ist (z.B. <= 0)."""
            pass

        class InsufficientFundsError(BankingError):
            """Wird ausgelöst, wenn das Guthaben für eine Abhebung nicht ausreicht."""
            pass
        ```

2.  **`account.py` refactoring:**

      * Öffnen Sie Ihre `account.py` (idealerweise die Version mit Logging aus Lab 3, die Version aus Lab 1 funktioniert aber auch).
      * Importieren Sie Ihre neuen Exceptions: `from exceptions import InvalidAmountError, InsufficientFundsError`.
      * **`deposit(self, amount)` anpassen:**
          * Entfernen Sie `return True` / `return False`.
          * Wenn `amount <= 0`, lösen Sie einen Fehler aus: `raise InvalidAmountError("Einzahlungsbetrag muss positiv sein.")`
          * (Der Log-Aufruf, falls vorhanden, sollte *vor* dem `raise` erfolgen).
      * **`withdraw(self, amount)` anpassen:**
          * Entfernen Sie `return True` / `return False`.
          * Wenn `amount <= 0`, lösen Sie einen Fehler aus: `raise InvalidAmountError("Abhebungsbetrag muss positiv sein.")`
          * Wenn `self._balance < amount`, lösen Sie einen Fehler aus: `raise InsufficientFundsError(f"Guthaben nicht ausreichend. Benötigt: {amount:.2f} EUR, Verfügbar: {self._balance:.2f} EUR")`

3.  **`main.py` (Handler) implementieren:**

      * Erstellen Sie eine Funktion `perform_transaction(account, action, amount)`.
      * Innerhalb dieser Funktion, verwenden Sie einen `try...except`-Block:
          * **`try`:** Rufen Sie `account.deposit(amount)` oder `account.withdraw(amount)` auf (je nach `action`-Parameter).
          * **`except InvalidAmountError as e:`:** Fangen Sie den Fehler ab und drucken Sie eine benutzerfreundliche Nachricht (z.B. `print(f"Transaktion fehlgeschlagen: {e}")`).
          * **`except InsufficientFundsError as e:`:** Fangen Sie den Fehler ab und drucken Sie (z.B. `print(f"Transaktion abgelehnt: {e}")`).
      * Testen Sie dies mit mehreren Aufrufen, von denen einige fehlschlagen müssen (z.B. Abhebung von 1000 EUR bei 500 EUR Guthaben; Einzahlung von -50 EUR).

### Bonus-Herausforderung: `else`, `finally` und Exception Chaining

1.  **`else` und `finally`:**

      * Erweitern Sie den `try...except`-Block in Ihrer `perform_transaction`-Funktion:
      * **`else`:** Fügen Sie einen `else`-Block hinzu. Dieser wird *nur* ausgeführt, wenn *keine* Exception aufgetreten ist. Geben Sie hier eine Erfolgsmeldung aus (z.B. `print(f"Transaktion erfolgreich verbucht. Neuer Saldo: {account.get_balance():.2f} EUR")`).
      * **`finally`:** Fügen Sie einen `finally`-Block hinzu. Dieser wird *immer* ausgeführt. Geben Sie hier eine "Aufräum-"Nachricht aus (z.B. `print("--- Transaktionsverarbeitung beendet ---")`).

2.  **Exception Chaining:**

      * Stellen Sie sich vor, *vor* jeder Abhebung muss ein externer Betrugsprüfungs-Dienst (Fraud-Service) kontaktiert werden. Dieser Dienst kann `ConnectionError` oder `TimeoutError` werfen.
      * **`exceptions.py`:** Fügen Sie eine neue Exception hinzu: `class FraudServiceError(BankingError): pass`
      * **`main.py`:** Passen Sie `perform_transaction` für Abhebungen (`withdraw`) an:
          * Simulieren Sie im `try`-Block (vor dem `account.withdraw`-Aufruf) einen Fehler:
        <!-- end list -->
        ```python
        if action == "withdraw" and amount > 500: # Große Abhebungen prüfen
            try:
                # Simulierter Aufruf an externen Dienst, der fehlschlägt
                raise TimeoutError("Externer Fraud-Service antwortet nicht")
            except TimeoutError as e:
                # Exception Chaining: Wir fangen den technischen Fehler
                # und verpacken ihn in unseren eigenen, verständlichen Fehler.
                raise FraudServiceError("Betrugsprüfung konnte nicht durchgeführt werden") from e
        ```
      * **`except`-Blöcke:** Fügen Sie einen `except FraudServiceError as e:`-Block hinzu, um diesen neuen Fehler ebenfalls zu behandeln.
