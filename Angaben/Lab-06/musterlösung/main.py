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
    lambda x: int(x['amount'] * 100),
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

# Single line
total_withdrawals_small = reduce(
    lambda acc, tx: acc + tx['amount'] if tx['type'] == 'WITHDRAW' else acc,
    transactions,
    0.0
)
print(f"\n3. Gesamtsumme Abhebungen als einzelner Befehl (reduce): {total_withdrawals_small:.2f} EUR")


total_withdrawals = sum(tx['amount'] for tx in transactions if tx['type'] == 'WITHDRAW')

