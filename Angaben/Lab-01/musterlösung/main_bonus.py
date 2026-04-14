from account_bonus import Account

print("Teste Bonus-Herausforderung...")

# Test von __eq__
acc1 = Account("AT100", "Ina Invest", 1000.0)
acc2 = Account("AT100", "Ina Invest", 1000.0) # Selbe Kontonummer
acc3 = Account("AT200", "Berta Bank", 500.0)

print(f"acc1 == acc2: {acc1 == acc2}") # Erwartet: True
print(f"acc1 == acc3: {acc1 == acc3}") # Erwartet: False

print("-" * 20)

# Test von Name Mangling (__balance)
print(f"Kontostand (Getter): {acc1.get_balance()}")

# Der folgende Versuch wird einen AttributeError auslösen:
try:
    print(acc1.__balance)
except AttributeError as e:
    print(f"Fehler beim Direktzugriff: {e}")

# Python's Name Mangling in Aktion (nicht für die Praxis empfohlen!)
# Der Name wurde zu _Account__balance umbenannt:
print(f"Zugriff via Name Mangling: {acc1._Account__balance}")