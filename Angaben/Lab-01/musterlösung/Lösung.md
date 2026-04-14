## Lab 1: Lösung und Erklärungen

### Erläuterung des Lösungsansatzes

Die Lösung erstellt eine `Account`-Klasse, die als zentrale Blaupause für Bankkonten dient.

1.  **`__init__` (Konstruktor):** Wir verwenden den Konstruktor, um den *Zustand* jedes Objekts bei seiner Erstellung festzulegen. `account_number` und `account_holder` sind öffentlich (`self.attribut`), während `_balance` als "protected" (`self._attribut`) deklariert wird. Dies signalisiert anderen Entwicklern, dass sie nicht direkt darauf zugreifen sollten, obwohl Python dies technisch nicht verhindert.
2.  **Instanz-Methoden:** `deposit` und `withdraw` sind die Kernverhalten. Sie enthalten *Business-Logik* (Validierung), wie z.B. die Prüfung auf positive Beträge und ausreichende Deckung. `get_balance` ist ein typischer Getter für das protected-Attribut.
3.  **`__str__`:** Diese "Dunder-Methode" (Double Underscore) ist ein Kernaspekt des Operator Overloading. Sie definiert, wie das Objekt als String repräsentiert wird, was für `print()` und Logging unerlässlich ist.

### Basis Aufgabe

#### Datei: `account.py`

```python
# account.py

class Account:
    """
    Stellt ein einfaches Bankkonto dar, das Einzahlungen
    und Abhebungen mit Saldenprüfung verwaltet.
    """

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        """
        Initialisiert ein neues Konto.

        Args:
            account_number (str): Die eindeutige Kontonummer.
            account_holder (str): Der Name des Kontoinhabers.
            initial_balance (float, optional): Der Startsaldo. Standard ist 0.0.
        """
        self.account_number = account_number
        self.account_holder = account_holder
        # 'Protected' Attribut: Konvention signalisiert, 
        # dass dies nicht von außen direkt manipuliert werden sollte.
        self._balance = initial_balance

    def deposit(self, amount: float) -> bool:
        """
        Zahlt einen Betrag auf das Konto ein.
        Der Betrag muss positiv sein.
        """
        if amount > 0:
            self._balance += amount
            print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
            return True
        else:
            print("Einzahlungsbetrag muss positiv sein.")
            return False

    def withdraw(self, amount: float) -> bool:
        """
        Hebt einen Betrag vom Konto ab.
        Prüft auf positiven Betrag und ausreichende Deckung.
        """
        if amount <= 0:
            print("Abhebungsbetrag muss positiv sein.")
            return False
        
        if self._balance >= amount:
            self._balance -= amount
            print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
            return True
        else:
            print(f"Abhebung fehlgeschlagen. Nicht genügend Guthaben. (Stand: {self._balance:.2f} EUR)")
            return False

    def get_balance(self) -> float:
        """
        Gibt den aktuellen Kontostand zurück.
        """
        return self._balance

    def __str__(self) -> str:
        """
        Gibt eine String-Repräsentation des Kontos zurück.
        Wird von print() aufgerufen.
        """
        # Formatiert den Saldo als Währung mit 2 Nachkommastellen
        return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self._balance:.2f} EUR"

```

#### Datei: `main.py` (Test-Skript)

```python
# main.py
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

```

-----


### Teil 2: Lösung der Bonus-Herausforderung

Wir modifizieren die `account.py` Datei.

#### Datei: `account_bonus.py`

```python
# account_bonus.py

class Account:
    """
    Erweiterte Version der Account-Klasse mit:
    - Mindestguthaben (Klassen-Attribut)
    - Name Mangling für 'private' Attribute (__balance)
    - Gleichheitsprüfung (__eq__)
    """
    
    # 1. Klassen-Attribut
    # Gilt für ALLE Instanzen dieser Klasse
    MINIMUM_BALANCE = 0.0

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        
        # 2. "Private" Attribute (Name Mangling)
        # Python benennt dieses Attribut intern um (z.B. zu _Account__balance)
        if initial_balance < self.MINIMUM_BALANCE:
            raise ValueError(f"Anfangsguthaben darf nicht unter {self.MINIMUM_BALANCE} liegen")
        self.__balance = initial_balance

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self.__balance += amount
            print(f"Einzahlung von {amount:.2f} EUR erfolgreich.")
            return True
        else:
            print("Einzahlungsbetrag muss positiv sein.")
            return False

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            print("Abhebungsbetrag muss positiv sein.")
            return False
        
        # 1. Prüfung gegen MINIMUM_BALANCE
        if (self.__balance - amount) >= self.MINIMUM_BALANCE:
            self.__balance -= amount
            print(f"Abhebung von {amount:.2f} EUR erfolgreich.")
            return True
        else:
            print(f"Abhebung fehlgeschlagen. Guthaben nicht ausreichend oder Minimum-Saldo ({self.MINIMUM_BALANCE} EUR) würde unterschritten.")
            return False

    def get_balance(self) -> float:
        # Getter ist notwendig, da __balance 'private' ist
        return self.__balance

    def __str__(self) -> str:
        return f"Konto {self.account_number} (Inhaber: {self.account_holder}), Stand: {self.__balance:.2f} EUR"

    # 3. Operator Overloading (==)
    def __eq__(self, other) -> bool:
        """
        Prüft, ob zwei Konten 'gleich' sind (basierend auf der Kontonummer).
        """
        if isinstance(other, Account):
            # Wir definieren Gleichheit über die account_number
            return self.account_number == other.account_number
        return False

```

#### Datei: `main_bonus.py` (Test-Skript)

```python
# main_bonus.py
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

```