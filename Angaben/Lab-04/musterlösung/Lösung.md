## Lab 4: Lösung und Erklärungen

### Erläuterung des Lösungsansatzes

Der Kern dieses Labs ist der Übergang von "defensiver Programmierung" (Rückgabe von `True`/`False`) zu "offensiver Programmierung" (Auslösen von `Exceptions`). Wenn eine Methode ihre Aufgabe (z.B. Geld abheben) nicht erfüllen *kann*, sollte sie einen Fehler auslösen, anstatt stillschweigend zu scheitern.

1.  **Eigene Exception-Hierarchie (`exceptions.py`):** Wir definieren `BankingError` als Basis. Dadurch können Aufrufer wählen: Entweder sie fangen alle Bankfehler (`except BankingError:`) oder nur spezifische (`except InsufficientFundsError:`).
2.  **Refactoring `account.py`:** Die Methoden `deposit` und `withdraw` werden "brüchiger" (im positiven Sinne). Sie verlassen sich darauf, dass der Aufrufer (z.B. `main.py`) bereit ist, mit Fehlersituationen umzugehen. Sie werfen (`raise`) Exceptions, anstatt sie selbst zu unterdrücken.
3.  **Handler `main.py`:** Die `main.py` wird zur "Kommandozentrale". Sie implementiert die `try...except`-Logik.
      * **Kernaufgabe:** Zeigt das Abfangen spezifischer Fehler.
      * **Bonus (`else`, `finally`):** Zeigt den vollständigen `try`-Block. `else` ist ideal für Erfolgslogik (Code, der nur laufen soll, wenn `try` erfolgreich war). `finally` ist entscheidend für Aufräumarbeiten (z.B. "Verbindung schließen", "Log schreiben"), unabhängig vom Erfolg.
      * **Bonus (Chaining):** Das `raise ... from e` ist entscheidend. Es bewahrt den ursprünglichen Stack-Trace der `TimeoutError` (der "Root Cause"), während es dem Aufrufer den verständlicheren `FraudServiceError` präsentiert.

### Teil 1: Lösung der Kernaufgabe

#### Datei: `exceptions.py` (Neu)

```python
# exceptions.py

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

```

#### Datei: `account.py` (Version von Lab 1 oder 3)

```python
# account.py
import datetime
# 2. Import der neuen Exceptions
from exceptions import InvalidAmountError, InsufficientFundsError

class Account:
    """
    Rafactored Account-Klasse.
    Löst Exceptions aus statt 'False' zurückzugeben.
    (Basiert auf der Version von Lab 3 mit Logging)
    """

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance
        self.log_file_path = f"log_account_{self.account_number}.txt"
        self._log_transaction(f"Konto erstellt mit Startsaldo: {initial_balance:.2f} EUR")

    def _log_transaction(self, message: str):
        """Schreibt eine Nachricht mit Zeitstempel in die Log-Datei."""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file_path, mode="a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            print(f"WARNUNG: Logging fehlgeschlagen: {e}")


    def deposit(self, amount: float):
        """
        Zahlt einen Betrag ein.
        Löst InvalidAmountError bei ungültigem Betrag aus.
        """
        # 2. Validierung und 'raise'
        if amount <= 0:
            msg = f"Einzahlung fehlgeschlagen: Betrag ({amount:.2f} EUR) muss positiv sein."
            self._log_transaction(msg)
            raise InvalidAmountError(msg)
        
        # Normale Logik
        self._balance += amount
        print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
        self._log_transaction(f"Einzahlung: +{amount:.2f} EUR. Neuer Saldo: {self._balance:.2f} EUR")
        # Kein 'return True' mehr nötig

    def withdraw(self, amount: float):
        """
        Hebt einen Betrag ab.
        Löst InvalidAmountError oder InsufficientFundsError aus.
        """
        # 2. Validierung 1
        if amount <= 0:
            msg = f"Abhebung fehlgeschlagen: Betrag ({amount:.2f} EUR) muss positiv sein."
            self._log_transaction(msg)
            raise InvalidAmountError(msg)
        
        # 2. Validierung 2
        if self._balance < amount:
            msg = f"Abhebung fehlgeschlagen. Guthaben nicht ausreichend. Benötigt: {amount:.2f} EUR, Verfügbar: {self._balance:.2f} EUR"
            self._log_transaction(msg)
            raise InsufficientFundsError(msg)
        
        # Normale Logik
        self._balance -= amount
        print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
        self._log_transaction(f"Abhebung: -{amount:.2f} EUR. Neuer Saldo: {self._balance:.2f} EUR")
        # Kein 'return True' mehr nötig

    def get_balance(self) -> float:
        return self._balance

    def __str__(self) -> str:
        return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self._balance:.2f} EUR"

```

#### Datei: `main.py` (Kernaufgabe)

```python
# main.py
from account import Account
from exceptions import InvalidAmountError, InsufficientFundsError, BankingError

def perform_transaction(account: Account, action: str, amount: float):
    """
    Führt eine Transaktion aus und fängt bekannte Bank-Fehler ab.
    """
    print(f"\nVersuche {action} von {amount:.2f} EUR...")
    
    try:
        # 3. Der 'try'-Block
        if action == "deposit":
            account.deposit(amount)
        elif action == "withdraw":
            account.withdraw(amount)
        else:
            print("Unbekannte Aktion.")
            return

    # 3. Spezifische 'except'-Blöcke
    except InvalidAmountError as e:
        print(f"[FEHLER] Transaktion (ungültiger Betrag) fehlgeschlagen: {e}")
        
    except InsufficientFundsError as e:
        print(f"[FEHLER] Transaktion (Guthaben) abgelehnt: {e}")
    
    except BankingError as e:
        # Fängt alle anderen Fehler auf, die von BankingError erben
        print(f"[FEHLER] Allgemeiner Bankfehler: {e}")

# --- Test-Szenarien ---
acc1 = Account("AT001", "Max Mustermann", 500.0)
print(acc1)

# Szenario 1: Erfolgreiche Abhebung
perform_transaction(acc1, "withdraw", 100.0) # Sollte klappen

# Szenario 2: Fehlgeschlagen (Guthaben)
perform_transaction(acc1, "withdraw", 1000.0) # Sollte InsufficientFundsError auslösen

# Szenario 3: Fehlgeschlagen (Betrag)
perform_transaction(acc1, "deposit", -50.0) # Sollte InvalidAmountError auslösen

# Szenario 4: Erfolgreiche Einzahlung
perform_transaction(acc1, "deposit", 200.0)

print(f"\nEndgültiger Saldo: {acc1.get_balance():.2f} EUR") # Erwartet: 500-100+200 = 600

```

-----

### Teil 2: Lösung der Bonus-Herausforderung

#### Datei: `exceptions.py` (Erweitert)

```python
# exceptions.py
# (Klassen BankingError, InvalidAmountError, InsufficientFundsError von oben)
# ...

class BankingError(Exception):
    pass
class InvalidAmountError(BankingError):
    pass
class InsufficientFundsError(BankingError):
    pass

# 2. Neue Exception für den Bonus
class FraudServiceError(BankingError):
    """
    Wird ausgelöst, wenn der externe Betrugsprüfungs-Dienst ausfällt.
    """
    pass
```

#### Datei: `main_bonus.py`

```python
# main_bonus.py
from account import Account
from exceptions import InvalidAmountError, InsufficientFundsError, BankingError, FraudServiceError

def perform_transaction_robust(account: Account, action: str, amount: float):
    """
    Führt eine Transaktion aus und verwendet den vollständigen
    try...except...else...finally Block.
    
    Simuliert auch Exception Chaining.
    """
    print(f"\n>>> Versuche {action} von {amount:.2f} EUR...")
    
    try:
        # 2. Simulation für Exception Chaining
        if action == "withdraw" and amount > 400: # Prüfung für "große" Abhebungen
            print("Prüfe Transaktion mit externem Fraud-Service...")
            try:
                # Simulierter Aufruf, der fehlschlägt
                raise TimeoutError("Externer Fraud-Service (FS-1) antwortet nicht nach 30s")
            
            except TimeoutError as e:
                # 2. EXCEPTION CHAINING:
                # Wir fangen den technischen Fehler (TimeoutError)
                # und 'verpacken' ihn in unseren App-spezifischen Fehler (FraudServiceError).
                # 'from e' erhält den ursprünglichen Stack Trace.
                raise FraudServiceError("Betrugsprüfung konnte nicht durchgeführt werden") from e
        
        # Normale Transaktionslogik
        if action == "deposit":
            account.deposit(amount)
        elif action == "withdraw":
            account.withdraw(amount)
        else:
            print("Unbekannte Aktion.")
            return

    # --- Exception Handling ---
    except InvalidAmountError as e:
        print(f"[FEHLER] Transaktion (ungültiger Betrag) fehlgeschlagen: {e}")
        
    except InsufficientFundsError as e:
        print(f"[FEHLER] Transaktion (Guthaben) abgelehnt: {e}")
        
    except FraudServiceError as e:
        # Abfangen des 'chained' Error
        print(f"[FEHLER] Transaktion (Sicherheit) blockiert: {e}")
        # Wenn man den Fehler mit Traceback loggen würde, sähe man auch die 'TimeoutError'
        if e.__cause__:
             print(f"   |-> Ursache: {e.__cause__}")
             
    except BankingError as e:
        print(f"[FEHLER] Allgemeiner Bankfehler: {e}")

    # 1. 'else'-Block
    else:
        # Wird NUR ausgeführt, wenn im 'try'-Block KEINE Exception aufgetreten ist.
        print(f"[ERFOLG] Transaktion verbucht. Neuer Saldo: {account.get_balance():.2f} EUR")

    # 1. 'finally'-Block
    finally:
        # Wird IMMER ausgeführt, egal ob try, except oder else lief.
        print(f"--- Transaktionsverarbeitung für Konto {account.account_number} abgeschlossen ---")


# --- Test-Szenarien ---
print("--- Starte Bonus-Tests ---")
acc1 = Account("AT001", "Max Mustermann", 500.0)

# Szenario 1: Erfolg (trifft 'else' und 'finally')
perform_transaction_robust(acc1, "withdraw", 100.0) # Saldo: 400

# Szenario 2: Fehler (trifft 'except InsufficientFundsError' und 'finally')
perform_transaction_robust(acc1, "withdraw", 800.0) 

# Szenario 3: Chaining-Fehler (trifft 'except FraudServiceError' und 'finally')
# (Betrag > 400 löst die Simulation aus)
perform_transaction_robust(acc1, "withdraw", 401.0) 

# Szenario 4: Erfolg (trifft 'else' und 'finally')
perform_transaction_robust(acc1, "deposit", 150.0) # Saldo: 550

print(f"\nEndgültiger Saldo: {acc1.get_balance():.2f} EUR") # Erwartet: 500-100+150 = 550

```
