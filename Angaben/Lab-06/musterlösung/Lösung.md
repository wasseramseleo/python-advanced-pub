# Lab 6: Map, Filter & Reduce - Lösung

## Erläuterung der Lösung

### Basis-Aufgabe

1.  **`map`**: `map` ist ideal für 1:1-Transformationen. Für jedes Element in `transactions` wird die `lambda`-Funktion aufgerufen. `lambda x: x['amount'] * 100` nimmt ein `dict` `x` entgegen, greift auf den Schlüssel `'amount'` zu und gibt den transformierten Wert zurück. `list()` wird benötigt, da `map` einen "lazy" Iterator zurückgibt.
2.  **`filter`**: `filter` ist ideal für N:M-Selektionen. Es wendet die `lambda`-Funktion (ein Prädikat) auf jedes Element an. Nur wenn die Funktion `True` zurückgibt (hier: Typ ist `DEPOSIT` *und* Betrag \> 400), wird das Element in den Ergebnis-Iterator übernommen.
3.  **`reduce`**: `reduce` ist für N:1-Aggregationen (Reduktion auf einen Wert). Um die Aufgabe zu vereinfachen, wird die Kette "functional" aufgebaut:
      * Zuerst filtern wir die `WITHDRAW`-Transaktionen.
      * Dann `map`-en wir die gefilterte Liste auf die reinen `amount`-Werte.
      * *Erst dann* wenden wir `reduce` an. `lambda acc, curr: acc + curr` ist die Standard-Summierungsfunktion für `reduce`, wobei `acc` das Zwischenergebnis und `curr` das nächste Element (ein Betrag) ist.

### Bonus Challenge

1.  **Refactoring**: Die List Comprehensions sind oft "pythonischer" (besser lesbar), da sie die Logik (Transformation und Filterung) in einer einzigen, klaren Syntax vereinen, anstatt Funktionen wie `map` und `filter` zu verschachteln.
      * `[x['amount'] * 100 for x in transactions]` (entspricht `map`).
      * `[x for x in transactions if x['type'] == 'DEPOSIT' and x['amount'] > 400]` (entspricht `filter`).
2.  **Advanced `reduce`**: Diese Lösung zeigt die wahre Stärke von `reduce` – das Vergleichen von Elementen, um ein "bestes" zu finden.
      * Wir filtern zuerst die relevanten Transaktionen.
      * `reduce` wird aufgerufen. `lambda acc, curr: acc if acc['amount'] > curr['amount'] else curr` vergleicht den `amount` des bisherigen "besten" Elements (`acc`) mit dem `amount` des aktuellen Elements (`curr`). Es gibt immer den "Gewinner" (das `dict` mit dem höheren Betrag) an die nächste Iteration weiter.

## Python-Code: Basis-Aufgabe

```python
from functools import reduce

# Daten-Grundlage
transactions = [
    {'id': 'T1001', 'type': 'DEPOSIT', 'amount': 5000.00, 'currency': 'EUR'},
    {'id': 'T1002', 'type': 'WITHDRAW', 'amount': 1200.00, 'currency': 'EUR'},
    {'id': 'T1003', 'type': 'DEPOSIT', 'amount': 350.75, 'currency': 'EUR'},
    {'id': 'T1004', 'type': 'PAYMENT', 'amount': 89.90, 'currency': 'EUR'},
    {'id': 'T1005', 'type': 'WITHDRAW', 'amount': 2000.00, 'currency': 'EUR'},
    {'id': 'T1006', 'type': 'DEPOSIT', 'amount': 1500.00, 'currency': 'USD'},
]

print("--- Basis-Aufgabe Test ---")

# --- Task 1: map (Beträge in Cent) ---
# map wendet die lambda-Funktion auf jedes Element an.
amounts_in_cents = list(map(
    lambda x: x['amount'] * 100, 
    transactions
))
print(f"1. Beträge in Cent (map): {amounts_in_cents}")


# --- Task 2: filter (High-Value Deposits) ---
# filter behält nur Elemente, für die lambda True zurückgibt.
high_value_deposits = list(filter(
    lambda tx: tx['type'] == 'DEPOSIT' and tx['amount'] > 400,
    transactions
))
print(f"\n2. High-Value Deposits (filter):")
for tx in high_value_deposits:
    print(f"   {tx}")


# --- Task 3: reduce (Summe aller Abhebungen) ---
# Wir verketten filter, map und reduce

# 3a. Nur Abhebungen (WITHDRAW) filtern
withdrawals = filter(
    lambda tx: tx['type'] == 'WITHDRAW', 
    transactions
)

# 3b. Nur die Beträge (amount) aus den Abhebungen extrahieren
withdrawal_amounts = map(
    lambda tx: tx['amount'], 
    withdrawals
)

# 3c. Die Liste der Beträge mit reduce zur Summe aggregieren
# reduce(funktion, iterable, [initializer])
# lambda acc, curr: acc + curr  (acc = Akkumulator, curr = aktuelles Element)
total_withdrawals = reduce(
    lambda acc, curr: acc + curr, 
    withdrawal_amounts,
    0.0 # Initialwert 0.0, falls die Liste leer ist
)

print(f"\n3. Gesamtsumme Abhebungen (reduce): {total_withdrawals:.2f} EUR")
# Erwartetes Ergebnis: 1200.00 + 2000.00 = 3200.00
```

## Bonus Challenge

```python
from functools import reduce

# (Verwende dieselben 'transactions' Daten wie oben)
transactions = [
    {'id': 'T1001', 'type': 'DEPOSIT', 'amount': 5000.00, 'currency': 'EUR'},
    {'id': 'T1002', 'type': 'WITHDRAW', 'amount': 1200.00, 'currency': 'EUR'},
    {'id': 'T1003', 'type': 'DEPOSIT', 'amount': 350.75, 'currency': 'EUR'},
    {'id': 'T1004', 'type': 'PAYMENT', 'amount': 89.90, 'currency': 'EUR'},
    {'id': 'T1005', 'type': 'WITHDRAW', 'amount': 2000.00, 'currency': 'EUR'},
    {'id': 'T1006', 'type': 'DEPOSIT', 'amount': 1500.00, 'currency': 'USD'},
]

print("\n--- Bonus Challenge Test ---")

# --- 1. Refactoring mit List Comprehensions ---

# Task 1 (map) als List Comprehension:
amounts_in_cents_lc = [x['amount'] * 100 for x in transactions]
print(f"1a. Beträge in Cent (LC): {amounts_in_cents_lc}")

# Task 2 (filter) als List Comprehension:
high_value_deposits_lc = [
    tx for tx in transactions 
    if tx['type'] == 'DEPOSIT' and tx['amount'] > 400
]
print(f"\n1b. High-Value Deposits (LC):")
for tx in high_value_deposits_lc:
    print(f"   {tx}")


# --- 2. Advanced reduce (Finde höchste EUR-Einzahlung) ---

# 2a. Filtere zuerst die relevanten Transaktionen (DEPOSIT und EUR)
eur_deposits = [
    tx for tx in transactions
    if tx['type'] == 'DEPOSIT' and tx['currency'] == 'EUR'
]

# 2b. Wende reduce an, um das "maximale" Element zu finden
# Wir brauchen einen sicheren Initialwert, falls eur_deposits leer ist.
# Ein leeres dict oder ein dict mit amount 0 ist eine gute Wahl.
initial_tx = {'id': 'NONE', 'amount': 0.0} 

# Die lambda-Funktion vergleicht den Akkumulator (acc) mit dem aktuellen (curr)
# und gibt immer das 'dict' mit dem höheren 'amount' zurück.
highest_eur_deposit = reduce(
    lambda acc, curr: acc if acc['amount'] > curr['amount'] else curr,
    eur_deposits,
    initial_tx
)

print(f"\n2. Höchste EUR-Einzahlung (advanced reduce):")
print(f"   {highest_eur_deposit}")
# Erwartetes Ergebnis: {'id': 'T1001', 'type': 'DEPOSIT', 'amount': 5000.00, 'currency': 'EUR'}
```
