from functools import reduce

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