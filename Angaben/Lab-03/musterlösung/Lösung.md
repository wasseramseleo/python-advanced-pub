## Lab 3: Lösung und Erklärungen

### Erläuterung des Lösungsansatzes

#### Kernaufgabe (Logging)

Wir erweitern die `Account`-Klasse aus Lab 1 um eine Logging-Funktion.

1.  **Import `datetime`:** Wird für `datetime.datetime.now()` benötigt, um den genauen Zeitpunkt einer Transaktion zu erfassen. `.isoformat()` stellt sicher, dass wir einen standardisierten, gut lesbaren Zeitstempel erhalten.
2.  **`self.log_file_path`:** Durch die Speicherung im `__init__` wird jedes Konto-Objekt für seine eigene Log-Datei verantwortlich.
3.  **`_log_transaction` Methode:** Diese Methode kapselt die Logging-Logik. Der entscheidende Teil ist `with open(...) as f:`.
      * **Warum `with`?** Das `with`-Statement ruft automatisch `f.close()` auf, sobald der Code-Block (der eingerückte Teil) verlassen wird. Dies gilt auch, wenn ein Fehler (`Exception`) innerhalb des Blocks auftritt. Ohne `with` müssten wir einen `try...finally`-Block verwenden, um sicherzustellen, dass die Datei immer geschlossen wird und keine "Resource Leaks" entstehen. `with` ist also kürzer, sauberer und sicherer.
      * **Modus `"a"` (Append):** Wichtig, da wir bei jedem Log-Vorgang die Zeile *hinten anfügen* und nicht die Datei überschreiben wollen (was Modus `"w"` tun würde).

#### Bonus-Herausforderung (CodeTimer)

Um einen eigenen Context Manager zu erstellen, der mit `with` funktioniert, muss eine Klasse die Methoden `__enter__` und `__exit__` implementieren.

1.  **`__enter__(self)`:** Diese Methode wird *vor* dem Betreten des `with`-Blocks aufgerufen. Hier starten wir die Zeitmessung (`time.perf_counter()` ist genauer als `datetime` für die Messung von Ausführungszeiten).
2.  **`__exit__(self, ...)`:** Diese Methode wird *nach* dem Verlassen des `with`-Blocks aufgerufen (selbst wenn ein Fehler aufgetreten ist). Hier stoppen wir die Zeit, berechnen die Differenz und geben das Ergebnis aus.

### Teil 1: Lösung der Kernaufgabe

#### Datei: `account.py` (Modifiziert)

```python
# account.py
import datetime  # 1. Importiert

class Account:
    """
    Stellt ein einfaches Bankkonto dar.
    (Version von Lab 1, erweitert um Logging)
    """

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance
        
        # 2. Neues Attribut für den Log-Dateipfad
        self.log_file_path = f"log_account_{self.account_number}.txt"
        
        # Initial-Log beim Erstellen des Kontos
        self._log_transaction(f"Konto erstellt mit Startsaldo: {initial_balance:.2f} EUR")

    # 3. Neue "protected" Logging-Methode
    def _log_transaction(self, message: str):
        """
        Schreibt eine Nachricht mit Zeitstempel in die Log-Datei des Kontos.
        Verwendet einen Context Manager (with).
        """
        # Zeitstempel im ISO-Format (z.B. '2025-11-03T14:30:05.123456')
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            # 'with' stellt sicher, dass file.close() automatisch aufgerufen wird.
            # 'a' = append (anhängen), 'utf-8' für korrekte Zeichenkodierung
            with open(self.log_file_path, mode="a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            # Fallback, falls das Logging fehlschlägt (z.B. keine Schreibrechte)
            print(f"WARNUNG: Logging in {self.log_file_path} fehlgeschlagen: {e}")

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self._balance += amount
            print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
            # 4. Logging integrieren
            self._log_transaction(f"Einzahlung: +{amount:.2f} EUR. Neuer Saldo: {self._balance:.2f} EUR")
            return True
        else:
            print("Einzahlungsbetrag muss positiv sein.")
            self._log_transaction(f"Einzahlung fehlgeschlagen (Betrag: {amount:.2f} EUR)")
            return False

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            print("Abhebungsbetrag muss positiv sein.")
            self._log_transaction(f"Abhebung fehlgeschlagen (Betrag: {amount:.2f} EUR)")
            return False
        
        if self._balance >= amount:
            self._balance -= amount
            print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
            # 4. Logging integrieren
            self._log_transaction(f"Abhebung: -{amount:.2f} EUR. Neuer Saldo: {self._balance:.2f} EUR")
            return True
        else:
            print(f"Abhebung fehlgeschlagen. Nicht genügend Guthaben.")
            # 4. Logging integrieren
            self._log_transaction(f"Abhebung fehlgeschlagen (Guthaben: {self._balance:.2f} EUR, Betrag: {amount:.2f} EUR)")
            return False

    def get_balance(self) -> float:
        return self._balance

    def __str__(self) -> str:
        return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self._balance:.2f} EUR"

```

#### Datei: `main.py` (Test-Skript)

```python
# main.py
from account import Account
import os # Nützlich, um alte Logs zu löschen

# 5. Testen
acc1_id = "DE001"
acc2_id = "DE002"

# Alte Log-Dateien löschen für einen sauberen Test
if os.path.exists(f"log_account_{acc1_id}.txt"):
    os.remove(f"log_account_{acc1_id}.txt")
if os.path.exists(f"log_account_{acc2_id}.txt"):
    os.remove(f"log_account_{acc2_id}.txt")

print("Erstelle Konten und führe Transaktionen durch...")

acc1 = Account(account_number=acc1_id, account_holder="Max Mustermann", initial_balance=500.0)
acc2 = Account(account_number=acc2_id, account_holder="Erika Musterfrau")

# Transaktionen für acc1
acc1.deposit(150.50)
acc1.withdraw(70.0)
acc1.withdraw(1000.0) # Fehlgeschlagen

# Transaktionen für acc2
acc2.deposit(100.0)
acc2.withdraw(50.0)

print(acc1)
print(acc2)
print("\nSkript beendet. Bitte überprüfen Sie die .txt-Log-Dateien.")
print(f"(z.B. 'log_account_{acc1_id}.txt')")

```

#### Beispielinhalt: `log_account_DE001.txt`

```
[2025-11-03T15:01:20.123456] Konto erstellt mit Startsaldo: 500.00 EUR
[2025-11-03T15:01:20.123500] Einzahlung: +150.50 EUR. Neuer Saldo: 650.50 EUR
[2025-11-03T15:01:20.123550] Abhebung: -70.00 EUR. Neuer Saldo: 580.50 EUR
[2025-11-03T15:01:20.123600] Abhebung fehlgeschlagen (Guthaben: 580.50 EUR, Betrag: 1000.00 EUR)
```

-----

### Teil 2: Lösung der Bonus-Herausforderung

#### Datei: `utils.py` (Neu)

```python
# utils.py
import time

class CodeTimer:
    """
    Ein Context Manager zum Messen der Ausführungszeit
    eines Code-Blocks.
    
    Verwendung:
    with CodeTimer(name="Mein Test"):
        # ... langsamer Code ...
    """
    
    def __init__(self, name: str = "Timer"):
        """
        Initialisiert den Timer.
        
        Args:
            name (str): Ein Name zur Identifizierung der Messung in der Ausgabe.
        """
        self.name = name
        self.start_time = 0.0

    def __enter__(self):
        """
        Startet den Timer, wenn der 'with'-Block betreten wird.
        """
        # time.perf_counter() ist ideal für Performance-Messungen
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Stoppt den Timer und gibt die Dauer aus,
        wenn der 'with'-Block verlassen wird.
        
        Die exc_ (exception) Argumente sind für uns nicht relevant,
        aber erforderlich für die Signatur.
        """
        end_time = time.perf_counter()
        duration = end_time - self.start_time
        
        # Ausgabe der gemessenen Zeit
        print(f"\n--- [{self.name}] Code-Block beendet in {duration:.6f} Sekunden ---")
        # Wir geben nichts zurück (oder None), 
        # was signalisiert, dass alle Exceptions normal weitergeleitet werden sollen.

```

#### Datei: `main.py` (Test-Skript für Bonus)

```python
# main.py
from account import Account
from utils import CodeTimer  # 1. Bonus-Import
import os

# --- Setup (Alte Logs löschen) ---
acc1_id = "AT001"
if os.path.exists(f"log_account_{acc1_id}.txt"):
    os.remove(f"log_account_{acc1_id}.txt")

# --- Kern-Tests (wie oben) ---
print("Führe einzelne Transaktionen durch...")
acc1 = Account(account_number=acc1_id, account_holder="Max Mustermann", initial_balance=500.0)
acc1.deposit(100.0)
acc1.withdraw(50.0)


# 2. Anwendung des Bonus Context Managers
print("\nStarte Batch-Einzahlungstest...")

# Wir messen, wie lange 1000 Einzahlungen dauern
# (Logging in eine Datei kann die Ausführung verlangsamen!)
with CodeTimer(name="1000x Einzahlungen"):
    for i in range(1000):
        acc1.deposit(1.0)

print(f"Test beendet. Aktueller Saldo: {acc1.get_balance():.2f} EUR")

```

#### Beispiel-Ausgabe (Konsole)

``` text
Führe einzelne Transaktionen durch...
Einzahlung von 100.00 EUR erfolgreich.
Abhebung von 50.00 EUR erfolgreich.

Starte Batch-Einzahlungstest...
Einzahlung von 1.00 EUR erfolgreich.
Einzahlung von 1.00 EUR erfolgreich.
... (996 weitere Einzahlungen) ...
Einzahlung von 1.00 EUR erfolgreich.
Einzahlung von 1.00 EUR erfolgreich.

--- [1000x Einzahlungen] Code-Block beendet in 0.012345 Sekunden ---

Test beendet. Aktueller Saldo: 1550.00 EUR
```