from account import Account

# 1. Objekte erstellen (Instanziierung)
print("Erstelle Konten...")
acc1 = Account(account_number="AT001", account_holder="Max Mustermann", initial_balance=500.0)
acc2 = Account(account_number="AT002", account_holder="Erika Musterfrau") # nutzt initial_balance=0.0

# 2. Objekte mit print() testen (ruft __str__ auf)
print(acc1)
print(acc2)
print("-" * 20)

# 3. Methoden testen
print(f"Kontostand (acc1): {acc1.get_balance():.2f} EUR")
acc1.deposit(150.50)
acc1.withdraw(70.0)
print(f"Neuer Kontostand (acc1): {acc1.get_balance():.2f} EUR")
print(acc1)
print("-" * 20)

# 4. Test der Fehlerbehandlung
print("Teste Abhebung (acc2)...")
acc2.deposit(100.0)
# Dies sollte fehlschlagen
acc2.withdraw(150.0)
# Dies sollte gelingen
acc2.withdraw(50.0)
print(acc2)