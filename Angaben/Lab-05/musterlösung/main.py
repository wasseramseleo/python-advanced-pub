from account import BankAccount

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