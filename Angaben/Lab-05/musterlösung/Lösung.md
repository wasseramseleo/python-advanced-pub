# Lab 5: Iteratoren - Lösung

## Erläuterung der Lösung

### Basisaufgabe

Die Lösung trennt klar zwischen dem "Iterable" (dem Container) und dem "Iterator" (dem zustandsbehafteten "Zeiger").

1.  **`BankAccount` (Das Iterable):** Diese Klasse ist der "Container". Sie selbst weiß nicht, *wo* sie in einer Iteration steht. Sie implementiert nur `__iter__`. Ihre einzige Aufgabe ist es, auf Anfrage (`iter(account)` oder `for tx in account:`) ein *neues* Iterator-Objekt zu erstellen und zurückzugeben.
2.  **`AccountHistoryIterator` (Der Iterator):** Diese Klasse ist der "Zeiger". Sie implementiert das eigentliche Iterator-Protokoll:
      * `__init__`: Speichert den Zustand (die Datenquelle und den Index, bei `0` beginnend).
      * `__iter__`: Gibt sich selbst zurück, damit ein Iterator auch dort verwendet werden kann, wo ein Iterable erwartet wird (z.B. `list(my_iterator)`).
      * `__next__`: Beinhaltet die Logik: "Wo bin ich (`_index`)?", "Habe ich noch Daten?" (Wenn nein: `StopIteration`), "Was ist das nächste Element?". Es ändert seinen internen Zustand (`_index` inkrementieren) bei jedem Aufruf.

### Bonus-Herausforderung

Die Bonus-Lösung ist *echtes* "Lazy Loading". Sie ist viel speichereffizienter, da sie zu keinem Zeitpunkt alle Daten im Speicher hält.

1.  **`LazyTransactionReader`:** Dieser Iterator hält nur einen Dateizeiger (`_file_handle`).
2.  **`__next__`:** Diese Methode liest *nur eine einzige Zeile* aus der Datei, wenn sie aufgerufen wird.
3.  **Filterung:** Die `while True`-Schleife in `__next__` ist entscheidend. Wenn ein Filter gesetzt ist (`filter_keyword`), liest sie intern Zeilen, bis sie entweder ein Match findet (und zurückgibt) oder das Ende der Datei erreicht (`StopIteration`). Der Aufrufer (z.B. die `for`-Schleife) bemerkt von den übersprungenen Zeilen nichts; er erhält nur die gefilterten Ergebnisse, eines nach dem anderen.
4.  **Ressourcen-Management:** Das Öffnen im `__init__` und das explizite `close()` (das in `__next__` bei `StopIteration` aufgerufen wird) stellt sicher, dass die Datei nicht unnötig offen bleibt, nachdem der Iterator erschöpft ist.

## Python-Code: Basisaufgabe

```python
class BankAccount:
    """
    Stellt ein Bankkonto dar, das (intern) eine Liste von Transaktionen hält.
    Diese Klasse ist ein "Iterable".
    """
    def __init__(self, owner: str, account_number: str):
        self.owner = owner
        self.account_number = account_number
        self.__transactions = [] 

    def deposit(self, amount: float):
        self.__transactions.append(f"DEPOSIT: {amount} EUR")

    def withdraw(self, amount: float):
        self.__transactions.append(f"WITHDRAW: {amount} EUR")

    def get_transactions(self) -> list:
        return self.__transactions.copy()
            
    def __iter__(self):
        """
        Gibt ein Iterator-Objekt zurück. 
        Dies macht BankAccount zu einem "Iterable".
        """
        print("LOG: BankAccount.__iter__ aufgerufen. Erzeuge neuen Iterator.")
        return AccountHistoryIterator(self.__transactions)

class AccountHistoryIterator:
    """
    Dies ist der "Iterator". Er hält den Zustand der Iteration.
    """
    def __init__(self, transactions: list):
        self._transactions = transactions
        self._index = 0 # Zustand (Wo bin ich?)

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

# --- Beispiel-Nutzung (Basis-Aufgabe) ---
print("--- Basis-Aufgabe Test ---")
my_account = BankAccount("Erika Mustermann", "AT98765")
my_account.deposit(500)
my_account.withdraw(100)
my_account.deposit(50)

print(f"Beginne Iteration über Konto: {my_account.owner}")

# 1. Nutzung in einer for-Schleife (fängt StopIteration automatisch)
for tx in my_account:
    print(f"  -> Transaktion: {tx}")

print("\nZweite Iteration (erzeugt neuen Iterator):")
# 2. Eine for-Schleife kann mehrmals verwendet werden, da __iter__
# jedes Mal einen NEUEN Iterator erstellt.
for tx in my_account:
    print(f"  -> Zweiter Durchgang: {tx}")

print("\nManuelle Iteration (zeigt Erschöpfung):")
# 3. Manuelle Nutzung (zeigt, dass Iterator zustandsbehaftet ist)
manual_iter = iter(my_account) # Ruft my_account.__iter__() auf
print(next(manual_iter)) # DEPOSIT: 500
print(next(manual_iter)) # WITHDRAW: 100
# Der Iterator ist nun "verbraucht" für die ersten beiden Elemente
# Eine neue for-Schleife würde trotzdem von vorne anfangen:
for tx in my_account:
    print(f"  -> Dritter Durchgang: {tx}")
    break # Nur um den ersten zu zeigen
```

## Python-Code: Bonus-Herausforderung

```python
import os

class LazyTransactionReader:
    """
    Ein speichereffizienter Iterator, der eine große Transaktionsdatei
    Zeile für Zeile liest und optional filtert.
    """
    def __init__(self, filename: str, filter_keyword: str = None):
        print(f"LOG: LazyTransactionReader: Öffne Datei '{filename}'")
        self.filename = filename
        self.filter_keyword = filter_keyword
        try:
            self._file_handle = open(filename, 'r')
        except FileNotFoundError:
            print(f"FEHLER: Datei {filename} nicht gefunden.")
            self._file_handle = None
            raise

    def __iter__(self):
        return self

    def __next__(self):
        if self._file_handle is None:
            raise StopIteration # Bereits geschlossen oder Fehler

        while True: # Intern loopen, bis wir ein Match finden oder die Datei endet
            line = self._file_handle.readline()

            if not line:
                # Ende der Datei (EOF)
                print("LOG: LazyTransactionReader: Dateiende erreicht.")
                self.close() # Ressource freigeben
                raise StopIteration

            line = line.strip() # \n entfernen

            # Filter-Logik
            if self.filter_keyword is None:
                return line # Kein Filter, jede Zeile zurückgeben
            
            if self.filter_keyword.upper() in line.upper():
                return line # Match gefunden!

            # Kein Match & Filter ist an -> weiter zur nächsten Zeile (while True)
            # print(f"DEBUG: Überspringe Zeile: {line}")

    def close(self):
        """Schließt das Dateihandle, falls offen."""
        if self._file_handle:
            print(f"LOG: LazyTransactionReader: Schließe Datei '{self.filename}'")
            self._file_handle.close()
            self._file_handle = None

# --- Setup: Erstellen einer Dummy-Logdatei ---
log_filename = "test_tx.log"
dummy_data = """
DEPOSIT: 1000.50
WITHDRAW: 50.00
WITHDRAW: 120.25
DEPOSIT: 300.00
SYSTEM:FEE: 5.00
WITHDRAW: 80.00
"""

try:
    with open(log_filename, "w") as f:
        f.write(dummy_data.strip())
except IOError as e:
    print(f"Setup fehlgeschlagen: {e}")
    # Beenden, wenn wir die Datei nicht schreiben können

# --- Beispiel-Nutzung (Bonus) ---
print("\n--- Bonus-Herausforderung Test 1 (alle Transaktionen) ---")
try:
    # 1. Alle Transaktionen lesen
    all_tx_reader = LazyTransactionReader(log_filename)
    for line in all_tx_reader:
        print(f"  Gelesene Zeile: {line}")
    # Beachte: Die Datei sollte jetzt automatisch geschlossen sein.
    
except FileNotFoundError:
    pass # Fehler wurde bereits im Konstruktor behandelt

print("\n--- Bonus-Herausforderung Test 2 (nur 'DEPOSIT') ---")
try:
    # 2. Nur Einzahlungen (DEPOSIT) filtern
    deposit_reader = LazyTransactionReader(log_filename, filter_keyword="DEPOSIT")
    
    print(f"Nächstes Element (manuell): {next(deposit_reader)}")
    print(f"Nächstes Element (manuell): {next(deposit_reader)}")
    
    # Test auf StopIteration
    try:
        next(deposit_reader)
    except StopIteration:
        print("  Erwartete StopIteration! Der Filter-Iterator ist erschöpft.")

except FileNotFoundError:
    pass

# Aufräumen
if os.path.exists(log_filename):
    os.remove(log_filename)
```
