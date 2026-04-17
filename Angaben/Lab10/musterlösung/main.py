from account import BankAccount, find_account, AccountList, AccountId


# ---------------------------------------------------------------------------
# Generische Stack-Klasse (Python 3.12, PEP 695)
# Statt: from typing import TypeVar, Generic
#        T = TypeVar("T")
#        class Stack(Generic[T]):  ...
# Jetzt einfach:
#        class Stack[T]:  ...
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Test: Stack mit verschiedenen Typen
# mypy stellt sicher, dass z.B. int_stack.push("text") ein Fehler ist.
# ---------------------------------------------------------------------------

int_stack: Stack[int] = Stack()
int_stack.push(10)
int_stack.push(20)
print(f"Top (int): {int_stack.peek()}")     # 20
print(f"Pop:       {int_stack.pop()}")       # 20
print(f"Länge:     {len(int_stack)}")        # 1

str_stack: Stack[str] = Stack()
str_stack.push("Hallo")
str_stack.push("Welt")
print(f"Top (str): {str_stack.peek()}")      # Welt

# Folgende Zeile würde mypy mit einem Fehler markieren:
# int_stack.push("falscher Typ")
# → error: Argument 1 to "push" of "Stack" has incompatible type "str"; expected "int"


# ---------------------------------------------------------------------------
# Test: account.py mit Typaliase (type Amount, AccountId, AccountList)
# ---------------------------------------------------------------------------

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



