## Lab 2: Vererbung – Spezialisierte Konten

In Lab 1 haben wir eine solide `Account`-Basisklasse erstellt. In der Praxis benötigt unsere Banken-App jedoch spezialisierte Kontotypen, die von dieser Basis erben, aber zusätzliche oder abgewandelte Funktionen bieten.

Heute werden wir das Konzept der Vererbung nutzen, um "Spezial-Konten" wie ein Sparkonto zu erstellen.

### Lernziele

  * Eine Subklasse (abgeleitete Klasse) von einer Basisklasse definieren.
  * Verstehen, wie die `__init__`-Methoden von Basis- und Subklasse zusammenspielen.
  * Die `super()`-Funktion verwenden, um die Initialisierung der Basisklasse aufzurufen.
  * Methoden der Basisklasse in der Subklasse wiederverwenden.
  * Methoden der Basisklasse in der Subklasse überschreiben (Override).

### Szenario

Unsere Bank-App wird ein Erfolg\! Die Produktmanager möchten nun zwei neue Kontotypen einführen:

1.  **SavingsAccount (Sparkonto):** Dieses Konto erbt alle Basisfunktionen eines `Account`, soll aber zusätzlich Zinsen auf das Guthaben anrechnen können.
2.  **CheckingAccount (Girokonto):** Dieses Konto erbt ebenfalls, soll aber einen Überziehungskredit (Dispo) ermöglichen, der in der `withdraw`-Logik berücksichtigt werden muss.

Wir nutzen Vererbung, um Code-Duplizierung zu vermeiden. Ein `SavingsAccount` *ist ein* `Account`, aber mit Spezialfunktionen.

-----

### Angabe: Das Sparkonto (`SavingsAccount`)
**Voraussetzung:** Sie benötigen Ihre `account.py` (oder `account_bonus.py`) aus Lab 1. Wir werden diese Klasse importieren und von ihr erben.

Definieren Sie in einer neuen Datei (`special_accounts.py`) eine Klasse `SavingsAccount`, die von `Account` erbt.

1.  **Import:** Stellen Sie sicher, dass Ihre `Account`-Klasse importiert werden kann (z.B. `from account import Account`).
2.  **Klassendefinition:** Definieren Sie die Klasse `SavingsAccount(Account)`.
3.  **Konstruktor (`__init__`):**
      * Der Konstruktor soll die gleichen Argumente wie `Account` annehmen (`account_number`, `account_holder`, `initial_balance`) SOWIE ein zusätzliches Argument: `interest_rate` (z.B. `0.02` für 2%).
      * Rufen Sie **unbedingt** den Konstruktor der Basisklasse (`Account`) mit `super().__init__(...)` auf, um die Attribute `account_number`, `account_holder` und `_balance` zu initialisieren.
      * Speichern Sie `interest_rate` als neues, öffentliches Attribut in der `SavingsAccount`-Instanz.
4.  **Neue Methode:**
      * Fügen Sie eine Methode `apply_interest(self)` hinzu.
      * Diese Methode soll die Zinsen für den aktuellen Saldo berechnen (Formel: `zinsen = self._balance * self.interest_rate`).
      * Die berechneten Zinsen sollen dem Konto gutgeschrieben werden. **Wichtig:** Verwenden Sie dazu die geerbte `deposit()`-Methode\! (z.B. `self.deposit(zinsen)`).
5.  **Testen (in `main.py`):**
      * Erstellen Sie ein `SavingsAccount`-Objekt (z.B. mit 1000 EUR Guthaben und 5% Zinsen).
      * Rufen Sie `apply_interest()` auf.
      * Prüfen Sie mit `get_balance()`, ob die Zinsen korrekt hinzugefügt wurden (erwartet: 1050 EUR).
      * Testen Sie, ob geerbte Methoden wie `withdraw()` weiterhin funktionieren.

### Bonus-Herausforderung: Das Girokonto (`CheckingAccount`)

Fügen Sie in `special_accounts.py` eine weitere Klasse `CheckingAccount` hinzu, die ebenfalls von `Account` erbt.

1.  **Konstruktor (`__init__`):**
      * Der Konstruktor soll die Standard-Argumente (`account_number`, etc.) SOWIE ein Argument `overdraft_limit` (z.B. `500.0`) annehmen.
      * Rufen Sie `super().__init__(...)` auf.
      * Speichern Sie das `overdraft_limit` (z.B. als `_overdraft_limit`, "protected").
2.  **Methode überschreiben (Override):**
      * **Definieren Sie die `withdraw(self, amount)` Methode neu.**
      * Diese neue Methode soll die Logik der `Account`-Klasse *überschreiben*.
      * Die Abhebung (`withdraw`) soll nun erfolgreich sein (und `True` zurückgeben), solange das verfügbare Limit (Saldo + Dispo) ausreicht.
      * Die Bedingung ändert sich von `self._balance >= amount` (aus Lab 1) zu `(self._balance + self._overdraft_limit) >= amount`.
      * Wenn die Abhebung erfolgreich ist, passen Sie `self._balance` an (dieser kann nun negativ werden) und geben `True` zurück. Andernfalls geben Sie `False` zurück (und drucken eine Fehlermeldung).
3.  **Testen (in `main.py`):**
      * Erstellen Sie ein `CheckingAccount` mit 100 EUR Guthaben und 500 EUR Dispo.
      * Versuchen Sie, 300 EUR abzuheben (mit `withdraw(300)`).
      * Prüfen Sie den neuen Kontostand (sollte `-200.0` sein).
