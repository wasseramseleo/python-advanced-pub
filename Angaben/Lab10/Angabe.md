# Lab 10: Type Annotations, Generics & mypy

## Lernziele

In diesem Lab fügen Sie der Banking-App vollständige Typ-Annotationen hinzu, führen statische Code-Analyse mit **mypy** durch und nutzen die modernen Typing-Features von **Python 3.12**.

* Die Syntax für Typ-Annotationen bei Variablen und Funktionen anwenden (`: type` und `-> ReturnType`).
* Typaliase mit dem **`type`-Keyword** (Python 3.12, PEP 695) definieren.
* **Generische Klassen** mit der neuen `[T]`-Syntax erstellen.
* Union Types (`int | str`), optionale Typen (`str | None`) und `Callable` korrekt einsetzen.
* **mypy** als statisches Analyse-Tool einrichten und ausführen.
* Verstehen, warum Annotationen **keine** Laufzeit-Fehler auslösen.

---

## Vorbereitung: mypy installieren

mypy ist ein statischer Type-Checker, der Ihren Code *vor* der Ausführung analysiert.

```bash
# Mit uv (empfohlen, wenn pyproject.toml vorhanden):
uv add mypy --dev

# Alternativ mit pip:
pip install mypy
```

Führen Sie mypy nach jeder Aufgabe aus und korrigieren Sie gemeldete Fehler:

```bash
# Einzelne Datei prüfen:
mypy Lab10/account.py

# Strengere Prüfung (empfohlen):
mypy Lab10/account.py --strict
```

> Die mypy-Konfiguration befindet sich in der `pyproject.toml` im Projektroot.

---

## Szenario

Unser Projekt wächst. Neue Entwickler finden es schwierig, die `BankAccount`-Klasse zu verwenden, da sie raten müssen, welche Datentypen erwartet werden. Wir führen Typ-Annotationen ein und sichern die Qualität mit **mypy**.

---

### Angabe

**Ziel:** Fügen Sie der `BankAccount`-Klasse vollständige Typ-Annotationen hinzu und definieren Sie Typaliase mit dem **`type`-Keyword** (Python 3.12).

**Kopiervorlage (bitte in `account.py` einfügen und vervollständigen):**

```python
# account.py

# 1. Definieren Sie Typaliase mit dem 'type'-Keyword (Python 3.12):
#    (Syntax: type Name = Typ)
type Amount = ...        # Sollte float sein
type AccountId = ...     # Sollte str sein


class BankAccount:
    """Stellt ein Bankkonto dar."""

    # 2. Klassenattribute annotieren
    owner: ...
    account_number: ...
    _balance: ...

    def __init__(self, owner, account_number, initial_balance=0.0):
        # 3. Parameter annotieren:
        #    owner: str, account_number: AccountId,
        #    initial_balance: Amount, Return-Type: None
        self.owner = owner
        self.account_number = account_number
        self._balance = initial_balance

    def deposit(self, amount) -> ...:
        # 4. 'amount' als Amount annotieren, Return-Type: bool
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount) -> ...:
        # 5. 'amount' als Amount annotieren, Return-Type: bool
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> ...:
        # 6. Return-Type: Amount
        return self._balance

    def get_owner_name(self) -> ...:
        # 7. Return-Type: str
        return self.owner


# 8. Typalias für eine Liste von Konten (Python 3.12):
type AccountList = ...   # list[BankAccount]


def find_account(accounts, number):
    # 9. Annotieren Sie:
    #    'accounts': AccountList
    #    'number':   AccountId
    #    Return-Type: BankAccount | None
    for acc in accounts:
        if acc.account_number == number:
            return acc
    return None
```

**Testen mit mypy:**

```bash
mypy Lab10/account.py --strict
```

Ziel: mypy meldet **0 Fehler**.

---

### Bonus 1

**Ziel:** Erstellen Sie eine **generische Klasse** mit der neuen `[T]`-Syntax.

Die Slides zeigen generische *Funktionen* (`def summe[T](...)`). Klassen können auf **dieselbe Weise** generisch gemacht werden:

```python
class Stack[T]:
    ...
```

**Aufgabe:** Implementieren Sie die generische `Stack[T]`-Klasse in `main.py`:

```python
# main.py
from account import BankAccount, find_account, AccountList, AccountId

# --- Generische Stack-Klasse (Python 3.12 Syntax) ---

class Stack[T]:
    """Ein generischer LIFO-Stack für beliebige Typen."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: ...) -> None:     # 1. Typ von 'item' angeben
        self._items.append(item)

    def pop(self) -> ...:                  # 2. Return-Typ: T | None
        if self._items:
            return self._items.pop()
        return None

    def peek(self) -> ...:                 # 3. Return-Typ: T | None
        if self._items:
            return self._items[-1]
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


# --- Test: Stack mit verschiedenen Typen ---
int_stack: Stack[int] = Stack()
int_stack.push(10)
int_stack.push(20)
print(f"Top (int): {int_stack.peek()}")     # 20
print(f"Pop:       {int_stack.pop()}")      # 20
print(f"Länge:     {len(int_stack)}")       # 1

str_stack: Stack[str] = Stack()
str_stack.push("Hallo")
str_stack.push("Welt")
print(f"Top (str): {str_stack.peek()}")     # Welt

# mypy-Frage: Was meldet mypy bei dieser Zeile? Warum?
# int_stack.push("falscher Typ")

# --- Aufgabe 1 testen ---
accounts: AccountList = [
    BankAccount("Anna Müller", "AT001", 500.0),
    BankAccount("Bob Kaiser", "AT002", 250.0),
]

found = find_account(accounts, "AT002")
if found:
    print(f"Gefunden: {found.get_owner_name()}, Saldo: {found.get_balance()}")

not_found = find_account(accounts, "XYZ")
print(f"Nicht gefunden: {not_found}")
```

```bash
mypy Lab10/main.py --strict
```

---

## Bonus 2

**Ziel:** Verwenden Sie `TypedDict` für typsichere Dictionaries und `Callable` für Callbacks.

**Hintergrund:** `dict[str, str | float]` ist ungenau – wir wissen genau, welche Schlüssel und Typen ein Transaktions-Dict hat. `TypedDict` macht das präzise und mypy-freundlich.

**Kopiervorlage für `main_bonus.py`:**

```python
# main_bonus.py
from typing import Callable, TypedDict


# 1. Definieren Sie ein TypedDict für eine Transaktion:
class Transaction(TypedDict):
    id: str
    type: str      # 'DEPOSIT', 'WITHDRAW' oder 'INVALID'
    amount: float


# 2. Handler mit korrekter TypedDict-Annotation:
def deposit_handler(tx: Transaction) -> bool:
    """Verarbeitet nur DEPOSIT-Transaktionen."""
    if tx['type'] == 'DEPOSIT':
        print(f"  Einzahlung: {tx['amount']:.2f} €")
        return True
    return False


# 3. Implementieren Sie process_batch mit korrekten Annotationen:
#    - transactions: list[Transaction]
#    - handler:      Callable[[Transaction], bool]
#    - return:       None
def process_batch(transactions, handler) -> None:
    print(f"\nVerarbeite Batch ({len(transactions)} Transaktionen):")
    ok = sum(1 for tx in transactions if handler(tx))
    print(f"  → {ok} verarbeitet, {len(transactions) - ok} übersprungen.")


# 4. Testdaten und Aufruf:
batch: list[Transaction] = [
    {'id': 'T1', 'type': 'DEPOSIT',  'amount': 100.0},
    {'id': 'T2', 'type': 'WITHDRAW', 'amount':  50.0},
    {'id': 'T3', 'type': 'DEPOSIT',  'amount': 300.0},
    {'id': 'T4', 'type': 'INVALID',  'amount':  -10.0},
]

process_batch(batch, deposit_handler)


# 5. Bonus-Bonus: Schreiben Sie einen 'withdraw_handler' und testen Sie ihn.
#    Definieren Sie außerdem eine Funktion mit falschem Return-Typ (-> str)
#    und übergeben Sie sie an process_batch. Was meldet mypy?
```

```bash
mypy Lab10/main_bonus.py --strict
```
