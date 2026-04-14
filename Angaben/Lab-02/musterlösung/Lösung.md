## Lab 2: Lösung und Erklärungen

### Erläuterung des Lösungsansatzes

Wir nutzen das Vererbungsprinzip (IS-A-Beziehung), um spezialisierte Konten zu erstellen, die Code von der `Account`-Basisklasse wiederverwenden.

1.  **`SavingsAccount` (Kernaufgabe):** Diese Klasse *erweitert* die Basisklasse. Sie erbt alle Attribute (`_balance` etc.) und Methoden (`deposit`, `withdraw`). Der entscheidende Punkt ist der Aufruf von `super().__init__()`. Dieser stellt sicher, dass die Initialisierungslogik der Basisklasse (die wir in Lab 1 definiert haben) zuerst ausgeführt wird, bevor die Subklasse ihre eigenen Attribute (hier: `interest_rate`) hinzufügt. Die neue Methode `apply_interest` nutzt die geerbte `deposit`-Methode, was ein Kernelement der Wiederverwendbarkeit von Code darstellt.

2.  **`CheckingAccount` (Bonus):** Diese Klasse *modifiziert* die Basisklasse. Statt nur neue Methoden hinzuzufügen, *überschreibt* (overrides) sie die geerbte `withdraw`-Methode. Python verwendet automatisch die spezifischste Methode, die es finden kann. Wenn `withdraw` auf einem `CheckingAccount`-Objekt aufgerufen wird, findet Python die Implementierung im `CheckingAccount` zuerst und ignoriert die `withdraw`-Methode der `Account`-Basisklasse.

### Basis Aufgabe

Wir gehen davon aus, dass `account.py` aus Lab 1 im selben Verzeichnis liegt.

#### Datei: `special_accounts.py` (enthält nur Kernaufgabe)

```python
# special_accounts.py

# Wir importieren die Basisklasse aus unserer vorherigen Arbeit
from account import Account

class SavingsAccount(Account):
    """
    Ein Sparkonto, das von Account erbt.
    Fügt Zinsberechnung hinzu.
    """
    
    def __init__(self, account_number: str, account_holder: str, 
                 initial_balance: float = 0.0, interest_rate: float = 0.01):
        """
        Initialisiert das Sparkonto.
        
        Args:
            interest_rate (float): Der Zinssatz als Dezimalzahl (z.B. 0.02 für 2%).
        """
        # 3. Aufruf des Konstruktors der Basisklasse (Account)
        # Dies ist entscheidend, damit self.account_number, 
        # self.account_holder und self._balance initialisiert werden.
        super().__init__(account_number, account_holder, initial_balance)
        
        # 3. Neues, spezifisches Attribut für diese Subklasse
        self.interest_rate = interest_rate
        print(f"Sparkonto {self.account_number} mit {self.interest_rate*100}% Zinsen erstellt.")

    def apply_interest(self):
        """
        Berechnet die Zinsen auf den aktuellen Saldo
        und fügt sie dem Konto hinzu.
        """
        # Wir greifen auf _balance zu (geerbt) und self.interest_rate (eigen)
        interest_amount = self._balance * self.interest_rate
        
        if interest_amount > 0:
            print(f"Rechne Zinsen an: {interest_amount:.2f} EUR")
            # 4. Wir verwenden die geerbte 'deposit'-Methode
            self.deposit(interest_amount)
        else:
            print("Keine Zinsen angerechnet (Guthaben zu gering).")

```

#### Datei: `main.py` (Test-Skript für Kernaufgabe)

```python
# main.py
from special_accounts import SavingsAccount
from account import Account # Optional für Vergleich

# 1. Test der Basisklasse (wie in Lab 1)
print("--- Test Basis-Account ---")
acc_base = Account("AT001", "Basis Kunde", 100.0)
acc_base.withdraw(50.0)
print(acc_base)


# 5. Test der Subklasse SavingsAccount
print("\n--- Test SavingsAccount ---")
# Erstellen eines SavingsAccount-Objekts
# Beachten Sie das zusätzliche Argument 'interest_rate'
sa1 = SavingsAccount(
    account_number="AT100", 
    account_holder="Ina Sparfuchs", 
    initial_balance=1000.0,
    interest_rate=0.05  # 5% Zinsen
)

print(sa1) # Nutzt die __str__ Methode von Account (geerbt)

# 5. Test der neuen Methode 'apply_interest'
sa1.apply_interest() # Sollte 50.0 EUR Zinsen hinzufügen
print(f"Neuer Stand nach Zinsen: {sa1.get_balance():.2f} EUR") # Erwartet: 1050.0

# 5. Test der geerbten Methode 'withdraw'
sa1.withdraw(200.0)
print(f"Neuer Stand nach Abhebung: {sa1.get_balance():.2f} EUR") # Erwartet: 850.0

```

-----

### Teil 2: Lösung der Bonus-Herausforderung

Wir fügen die `CheckingAccount`-Klasse zur `special_accounts.py` hinzu.

#### Datei: `special_accounts.py` (Vollständige Version)

```python
# special_accounts.py

from account import Account

class SavingsAccount(Account):
    """
    Ein Sparkonto, das von Account erbt.
    Fügt Zinsberechnung hinzu. (Wie oben)
    """
    
    def __init__(self, account_number: str, account_holder: str, 
                 initial_balance: float = 0.0, interest_rate: float = 0.01):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = interest_rate
        print(f"Sparkonto {self.account_number} mit {self.interest_rate*100}% Zinsen erstellt.")

    def apply_interest(self):
        interest_amount = self._balance * self.interest_rate
        if interest_amount > 0:
            print(f"Rechne Zinsen an: {interest_amount:.2f} EUR")
            self.deposit(interest_amount)
        else:
            print("Keine Zinsen angerechnet (Guthaben zu gering).")

# --- Bonus-Lösung beginnt hier ---

class CheckingAccount(Account):
    """
    Ein Girokonto, das von Account erbt.
    Erweitert 'withdraw' um einen Überziehungskredit (Dispo).
    """
    
    def __init__(self, account_number: str, account_holder: str, 
                 initial_balance: float = 0.0, overdraft_limit: float = 500.0):
        """
        Initialisiert das Girokonto.
        
        Args:
            overdraft_limit (float): Der Überziehungsrahmen (Dispo).
        """
        # 1. Aufruf des Basis-Konstruktors
        super().__init__(account_number, account_holder, initial_balance)
        
        # 1. Speichern des neuen Attributs
        self._overdraft_limit = overdraft_limit
        print(f"Girokonto {self.account_number} mit {self._overdraft_limit:.2f} EUR Dispo erstellt.")

    # 2. Überschreiben (Override) der 'withdraw' Methode
    def withdraw(self, amount: float) -> bool:
        """
        Hebt einen Betrag vom Konto ab.
        Berücksichtigt den Überziehungskredit (Dispo).
        """
        if amount <= 0:
            print("Abhebungsbetrag muss positiv sein.")
            return False
        
        # 2. Geänderte Logik: Prüft Saldo + Dispo
        available_funds = self._balance + self._overdraft_limit
        
        if available_funds >= amount:
            # Abhebung ist ok, auch wenn Saldo negativ wird
            self._balance -= amount
            print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
            print(f"Neuer Kontostand: {self._balance:.2f} EUR")
            return True
        else:
            # Nicht mal der Dispo reicht aus
            print(f"Abhebung fehlgeschlagen. Verfügbares Limit ({available_funds:.2f} EUR) überschritten.")
            return False

```

#### Datei: `main.py` (Test-Skript für Bonus)

```python
# main.py
from special_accounts import SavingsAccount, CheckingAccount

# ... (Test für SavingsAccount von oben) ...


# 3. Test der Bonus-Herausforderung (CheckingAccount)
print("\n--- Test CheckingAccount (Bonus) ---")

ca1 = CheckingAccount(
    account_number="AT200",
    account_holder="Gabi Giro",
    initial_balance=100.0,
    overdraft_limit=500.0
)
print(f"Verfügbares Limit: (100 Saldo + 500 Dispo) = 600 EUR")

# 3. Test der überschriebenen 'withdraw' Methode
print("\nVersuche Abhebung von 300 EUR (sollte gelingen):")
ca1.withdraw(300.0)
# Erwarteter Saldo: 100 - 300 = -200.0
print(f"Aktueller Saldo: {ca1.get_balance():.2f} EUR") # get_balance() ist geerbt

print("\nVersuche Abhebung von 400 EUR (sollte scheitern):")
# Verfügbar sind nur noch: -200 (Saldo) + 500 (Dispo) = 300 EUR
ca1.withdraw(400.0)
print(f"Aktueller Saldo: {ca1.get_balance():.2f} EUR") # Saldo sollte unverändert -200.0 sein

print("\nTeste geerbte 'deposit' Methode:")
ca1.deposit(1000.0) # Saldo sollte von -200 auf 800 steigen
print(f"Aktueller Saldo: {ca1.get_balance():.2f} EUR")

```