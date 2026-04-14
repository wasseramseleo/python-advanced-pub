from account import Account
import os # Nützlich, um alte Logs zu löschen


acc1_id = "AT001"
acc2_id = "AT002"

# Alte Log-Dateien löschen für einen sauberen Test
if os.path.exists(f"log_account_{acc1_id}.txt"):
    os.remove(f"log_account_{acc1_id}.txt")
if os.path.exists(f"log_account_{acc2_id}.txt"):
    os.remove(f"log_account_{acc2_id}.txt")

print("Erstelle Konten und führe Transaktionen durch...")

acc1 = Account(account_number=acc1_id, account_holder="Max Mustermann", initial_balance=500.0)
acc2 = Account(account_number=acc2_id, account_holder="Erika Musterfrau")

# Transaktionen für acc1
acc1.deposit(150.50)
acc1.withdraw(70.0)
acc1.withdraw(1000.0) # Fehlgeschlagen

# Transaktionen für acc2
acc2.deposit(100.0)
acc2.withdraw(50.0)

print(acc1)
print(acc2)
print("\nSkript beendet. Bitte überprüfen Sie die .txt-Log-Dateien.")
print(f"(z.B. 'log_account_{acc1_id}.txt')")