# Lab 10: Type Annotations, Generics & mypy – Lösung

## Aufgabe 1: BankAccount annotieren & Typaliase

### Erklärung

**`type`-Keyword (Python 3.12, PEP 695):** Statt `MyType = SomeType` (impliziter Alias) schreibt man jetzt `type MyType = SomeType`. Das macht den Alias explizit, ermöglicht generische Aliase (`type Pair[T] = tuple[T, T]`) und wird von mypy vollständig unterstützt.

**Typaliase** verbessern die Lesbarkeit: `amount: Amount` ist sprechender als `amount: float`, weil klar ist, dass es sich um einen Geldbetrag handelt – und nicht z.B. eine Temperatur oder ein Gewicht. Bei Refactorings reicht eine Änderung an einer Stelle.

**`BankAccount | None`**: Die moderne Schreibweise für optionale Rückgaben (seit Python 3.10). mypy erzwingt, dass der Aufrufer den `None`-Fall prüft, bevor er auf das Objekt zugreift.

### account.py

```python
# Typaliase mit dem 'type'-Keyword (Python 3.12, PEP 695)
type Amount = float
type AccountId = str


class BankAccount:
    """Stellt ein Bankkonto dar."""

    owner: str
    account_number: AccountId
    _balance: Amount

    def __init__(
        self,
        owner: str,
        account_number: AccountId,
        initial_balance: Amount = 0.0,
    ) -> None:
        self.owner = owner
        self.account_number = account_number
        self._balance = initial_balance

    def deposit(self, amount: Amount) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount: Amount) -> bool:
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> Amount:
        return self._balance

    def get_owner_name(self) -> str:
        return self.owner


type AccountList = list[BankAccount]


def find_account(accounts: AccountList, number: AccountId) -> BankAccount | None:
    for acc in accounts:
        if acc.account_number == number:
            return acc
    return None
```

**mypy-Output (bei korrekter Lösung):**
```
Success: no issues found in 1 source file
```

---

## Bonus 1: Generische Stack-Klasse

### Erklärung

**Vor Python 3.12** (alter Weg mit TypeVar):
```python
from typing import TypeVar, Generic
T = TypeVar("T")

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
```

**Ab Python 3.12** (PEP 695, neuer Weg):
```python
class Stack[T]:
    def push(self, item: T) -> None: ...
```

Der neue Weg ist kürzer, lesbarer und konsistent mit der Syntax für generische Funktionen (`def summe[T](...)`), die in den Slides gezeigt wird.

mypy erkennt bei `Stack[int]`, dass `push("text")` ein Fehler ist – **ohne Laufzeitfehler**. Das ist der Kernnutzen: Fehler werden *vor* der Ausführung gefunden.

### main.py

```python
from account import BankAccount, find_account, AccountList, AccountId


class Stack[T]:
    """Ein generischer LIFO-Stack für beliebige Typen."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T | None:
        if self._items:
            return self._items.pop()
        return None

    def peek(self) -> T | None:
        if self._items:
            return self._items[-1]
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


int_stack: Stack[int] = Stack()
int_stack.push(10)
int_stack.push(20)
print(f"Top (int): {int_stack.peek()}")   # 20
print(f"Pop:       {int_stack.pop()}")    # 20
print(f"Länge:     {len(int_stack)}")     # 1

str_stack: Stack[str] = Stack()
str_stack.push("Hallo")
str_stack.push("Welt")
print(f"Top (str): {str_stack.peek()}")   # Welt

# int_stack.push("falscher Typ")
# → mypy: Argument 1 to "push" has incompatible type "str"; expected "int"

accounts: AccountList = [
    BankAccount("Anna Müller", "AT001", 500.0),
    BankAccount("Bob Kaiser",  "AT002", 250.0),
]
number: AccountId = "AT002"
found = find_account(accounts, number)
if found:
    found.deposit(100.0)
    print(f"Gefunden: {found.get_owner_name()}, Saldo: {found.get_balance():.2f} €")
not_found = find_account(accounts, "XYZ")
print(f"Nicht gefunden: {not_found}")
```

---

## Bonus 2: TypedDict & Callable

### Erklärung

**TypedDict** löst das Problem von `dict[str, str | float]`:

| | `dict[str, str \| float]` | `TypedDict` |
|---|---|---|
| `tx['amount']` Typ | `str \| float` | `float` ✓ |
| Tippfehler `tx['ammount']` | kein Fehler | mypy-Fehler ✓ |
| Fehlende Schlüssel | kein Fehler | mypy-Fehler ✓ |

**`Callable[[Transaction], bool]`** stellt sicher, dass nur Funktionen mit der richtigen Signatur als Handler übergeben werden können. mypy prüft das an der Aufrufstelle.

### main_bonus.py

```python
from typing import Callable, TypedDict


class Transaction(TypedDict):
    id: str
    type: str
    amount: float


def deposit_handler(tx: Transaction) -> bool:
    if tx['type'] == 'DEPOSIT':
        print(f"  Einzahlung: {tx['amount']:.2f} €  (ID: {tx['id']})")
        return True
    return False


def withdraw_handler(tx: Transaction) -> bool:
    if tx['type'] == 'WITHDRAW':
        print(f"  Auszahlung: {tx['amount']:.2f} €  (ID: {tx['id']})")
        return True
    return False


def process_batch(
    transactions: list[Transaction],
    handler: Callable[[Transaction], bool],
) -> None:
    print(f"\nBatch-Verarbeitung mit Handler '{handler.__name__}':")
    ok = sum(1 for tx in transactions if handler(tx))
    print(f"  → {ok} verarbeitet, {len(transactions) - ok} übersprungen.")


batch: list[Transaction] = [
    {'id': 'T1', 'type': 'DEPOSIT',  'amount': 100.0},
    {'id': 'T2', 'type': 'WITHDRAW', 'amount':  50.0},
    {'id': 'T3', 'type': 'DEPOSIT',  'amount': 300.0},
    {'id': 'T4', 'type': 'INVALID',  'amount':  -10.0},
]

process_batch(batch, deposit_handler)
process_batch(batch, withdraw_handler)
```

**mypy-Output bei falschem Handler:**
```
error: Argument 2 to "process_batch" has incompatible type
       "Callable[[Transaction], str]"; expected "Callable[[Transaction], bool]"
```

---

## mypy-Konfiguration

Die `pyproject.toml` enthält eine mypy-Konfiguration für das gesamte Projekt:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

Ausführen für das gesamte Lab:
```bash
mypy Lab10/
```
