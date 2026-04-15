# Lab 10: Type Annotations & typing

## Lernziele

In diesem Lab fügen Sie dem Code unserer Banking-App Typ-Annotationen hinzu, um die Lesbarkeit zu verbessern und die statische Analyse (z.B. mit `mypy`) zu ermöglichen.

  * Die Syntax für Typ-Annotationen bei Variablen und Funktionen anwenden (`: type` und `-> ReturnType`).
  * Verstehen, warum Annotationen die Code-Qualität und Dokumentation verbessern, aber *keine* Laufzeit-Fehler (Runtime Errors) auslösen.
  * Moderne Annotationen für Container (z.B. `list[int]`) verwenden.
  * "Union Types" (z.B. `int | str`) und optionale Typen (z.B. `str | None`) korrekt einsetzen.

## Szenario

Unser Projekt wächst. Neue Entwickler finden es schwierig, die `BankAccount`-Klasse zu verwenden, da sie raten müssen, welche Datentypen die Methoden erwarten (z.B. `deposit(amount)` - ist `amount` ein `int`, `float` oder `str`?) und was sie zurückgeben.

Um die Wartbarkeit zu erhöhen und Tools wie `mypy` nutzen zu können, führen wir im gesamten Projekt Typ-Annotationen ein. Ihre Aufgabe ist es, die `BankAccount`-Klasse und zugehörige Funktionen zu annotieren.


### Angabe

**Ziel:** Fügen Sie einer vereinfachten `BankAccount`-Klasse (basierend auf Lab 1) und einer Hilfsfunktion vollständige Typ-Annotationen hinzu.

1.  **Vorbereitung:** Starten Sie mit der folgenden *un-annotierten* Kopiervorlage.
2.  **Aufgabe:** Fügen Sie überall dort Typ-Annotationen hinzu, wo sie fehlen (markiert mit `...`).

**Kopiervorlage (bitte vervollständigen):**

```python
# === Kopiervorlage (bitte annotieren) ===

class BankAccount:
    """
    Stellt ein Bankkonto dar. (Version für Type Hinting)
    """
    
    # 1. Klassen-Attribute annotieren
    owner: ...       # Sollte str sein
    account_number: ... # Sollte str sein
    _balance: ...      # Sollte float sein

    def __init__(self, owner, account_number, initial_balance=0.0):
        # 2. __init__ Parameter annotieren (Return-Type ist implizit None)
        self.owner = owner
        self.account_number = account_number
        self._balance = initial_balance

    def deposit(self, amount) -> ...:
        # 3. 'amount' (float) und Return-Type (bool) annotieren
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount) -> ...:
        # 4. 'amount' (float) und Return-Type (bool) annotieren
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> ...:
        # 5. Return-Type (float) annotieren
        return self._balance

    def get_owner_name(self) -> ...:
        # 6. Return-Type (str) annotieren
        return self.owner

# --- Externe Funktion zum Annotieren ---

def find_account_by_number(accounts, number):
    # 7. Annotieren Sie:
    #    'accounts' (eine Liste von BankAccount-Objekten) -> list[BankAccount]
    #    'number' (str)
    #    Return-Type (Das Konto ODER None, falls nicht gefunden) -> BankAccount | None
    
    for acc in accounts:
        if acc.account_number == number:
            return acc
    return None

# --- Test-Code (muss nach der Annotation fehlerfrei laufen) ---
print("--- Angabe Test ---")
acc1 = BankAccount("Max Mustermann", "AT123", 100.0)
acc1.deposit(50.5)
print(f"Saldo: {acc1.get_balance()}")

accounts_list = [acc1]
found_acc = find_account_by_number(accounts_list, "AT123")

if found_acc:
    print(f"Gefunden: {found_acc.get_owner_name()}")

not_found_acc = find_account_by_number(accounts_list, "XYZ")
print(f"Nicht gefunden: {not_found_acc}")
```

-----

### Bonus-Herausforderung

**Ziel:** Verwenden Sie komplexe Typen aus dem `typing`-Modul (oder moderne Äquivalente) wie `Callable` und `dict`.

**Szenario:** Wir benötigen eine flexible Funktion zur Verarbeitung von Transaktions-Batches. Diese Funktion soll eine "Callback"-Funktion (einen "Handler") akzeptieren, die entscheidet, was mit jeder Transaktion geschieht.

1.  **Import:** Importieren Sie `Callable` aus dem `typing`-Modul.
2.  **Daten:** Verwenden Sie diese Beispieldaten:
    ```python
    transactions_batch = [
        {'id': 'T1', 'type': 'DEPOSIT', 'amount': 100.0},
        {'id': 'T2', 'type': 'WITHDRAW', 'amount': 50.0},
        {'id': 'T3', 'type': 'INVALID', 'amount': -10.0}
    ]
    ```
3.  **Callback-Handler (Beispiel):** Erstellen Sie einen Handler (eine normale Funktion):
    ```python
    def simple_deposit_handler(tx_data):
        # (Parameter 'tx_data' muss annotiert werden)
        if tx_data['type'] == 'DEPOSIT':
            print(f"Verarbeite Einzahlung: {tx_data['amount']}")
            return True
        return False
    ```
4.  **Hauptfunktion `process_batch` (Hier liegt die Aufgabe):**
      * Erstellen Sie eine Funktion `process_batch`.
      * Annotieren Sie die Argumente:
          * `transactions`: Eine Liste von Dictionaries. Jedes `dict` hat `str`-Schlüssel und Werte, die `str` ODER `float` sein können. (Tipp: `list[dict[str, str | float]]`)
          * `handler`: Ein "Callable". Der Handler nimmt ein `dict` (wie oben) entgegen und gibt ein `bool` zurück. (Tipp: `Callable[[dict[str, str | float]], bool]`)
      * Annotieren Sie den Rückgabewert: Die Funktion gibt `None` zurück.
      * **Implementierung:** Die Funktion soll über `transactions` iterieren und den `handler` für jede Transaktion aufrufen.
