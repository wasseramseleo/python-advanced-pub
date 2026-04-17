from typing import Callable, TypedDict


# ---------------------------------------------------------------------------
# TypedDict: Typsichere Alternative zu dict[str, str | float]
# Wir wissen genau, welche Schlüssel und Typen eine Transaktion hat –
# TypedDict macht das explizit und mypy-überprüfbar.
# ---------------------------------------------------------------------------

class Transaction(TypedDict):
    id: str
    type: str      # 'DEPOSIT', 'WITHDRAW' oder 'INVALID'
    amount: float


# ---------------------------------------------------------------------------
# Handler-Funktionen (Callable[[Transaction], bool])
# ---------------------------------------------------------------------------

def deposit_handler(tx: Transaction) -> bool:
    """Verarbeitet nur DEPOSIT-Transaktionen."""
    if tx['type'] == 'DEPOSIT':
        print(f"  ✓ Einzahlung:  {tx['amount']:>8.2f} €  (ID: {tx['id']})")
        return True
    return False


def withdraw_handler(tx: Transaction) -> bool:
    """Verarbeitet nur WITHDRAW-Transaktionen."""
    if tx['type'] == 'WITHDRAW':
        print(f"  ✓ Auszahlung:  {tx['amount']:>8.2f} €  (ID: {tx['id']})")
        return True
    return False


# ---------------------------------------------------------------------------
# process_batch: nimmt eine Liste von Transaktionen und einen Handler entgegen
# ---------------------------------------------------------------------------

def process_batch(
    transactions: list[Transaction],
    handler: Callable[[Transaction], bool],
) -> None:
    """Verarbeitet einen Stapel von Transaktionen mit einem Callback-Handler."""
    print(f"\nBatch-Verarbeitung mit Handler '{handler.__name__}':")
    ok = sum(1 for tx in transactions if handler(tx))
    skipped = len(transactions) - ok
    print(f"  → {ok} verarbeitet, {skipped} übersprungen.")


# ---------------------------------------------------------------------------
# Test-Daten
# ---------------------------------------------------------------------------

batch: list[Transaction] = [
    {'id': 'T1', 'type': 'DEPOSIT',  'amount': 100.0},
    {'id': 'T2', 'type': 'WITHDRAW', 'amount':  50.0},
    {'id': 'T3', 'type': 'DEPOSIT',  'amount': 300.0},
    {'id': 'T4', 'type': 'INVALID',  'amount':  -10.0},
]

process_batch(batch, deposit_handler)
process_batch(batch, withdraw_handler)


# ---------------------------------------------------------------------------
# mypy-Demo: Was meldet mypy bei falschem Handler-Typ?
# ---------------------------------------------------------------------------

def wrong_return_handler(tx: Transaction) -> str:
    """Falscher Return-Typ (str statt bool) – mypy erkennt das!"""
    return "done"


# mypy würde bei dieser Zeile melden:
# error: Argument 2 to "process_batch" has incompatible type
#        "Callable[[Transaction], str]"; expected "Callable[[Transaction], bool]"
#
# process_batch(batch, wrong_return_handler)


# ---------------------------------------------------------------------------
# Vergleich: TypedDict vs. dict[str, str | float]
#
# dict[str, str | float]:
#   - Zugriff auf tx['amount'] liefert "str | float", nicht "float"
#   - Tippfehler im Schlüssel ('ammount') → kein mypy-Fehler
#
# TypedDict:
#   - tx['amount'] hat exakt den Typ float
#   - tx['ammount'] → mypy meldet: TypedDict "Transaction" has no key "ammount"
# ---------------------------------------------------------------------------
