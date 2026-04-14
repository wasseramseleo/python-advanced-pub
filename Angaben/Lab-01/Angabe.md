## Lab 1: Klassen & Objekte – Das Bankkonto

Willkommen zum ersten Lab! In dieser Übung legen wir das Fundament für unsere Banking-App. Wir definieren die Kern-Datenstruktur, mit der wir in den kommenden Tagen arbeiten werden: das `Account` (Konto).

### Lernziele

  * Eine Klasse (`class`) mit Attributen und Methoden definieren.
  * Den Unterschied zwischen Instanz-Attributen und Klassen-Attributen verstehen.
  * Den `__init__` Konstruktor zur Initialisierung von Objekten verwenden.
  * Methoden implementieren, um das Verhalten eines Objekts zu steuern.
  * Python-Konventionen für `public`, `_protected` und `__private` Member verstehen.
  * Spezielle Methoden (Dunder-Methoden) wie `__str__` für das "Operator Overloading" nutzen.

### Szenario

Jeder Kunde in unserer Bank-App benötigt mindestens ein Konto. Dieses Konto muss grundlegende Informationen speichern (Kontonummer, Inhaber) und grundlegende Aktionen zulassen (Einzahlen, Abheben, Kontostand prüfen).

Wir beginnen mit der Definition einer `Account` Klasse, die als Blaupause für alle zukünftigen Konten dient.

-----

### Angabe

Definieren Sie eine Klasse `Account` in einer Datei `account.py`.

1.  **Konstruktor (`__init__`):**

      * Die Klasse soll beim Erstellen (Instanziieren) drei Argumente entgegennehmen: `account_number` (string), `account_holder` (string) und `initial_balance` (float, Standardwert `0.0`).
      * Speichern Sie `account_number` und `account_holder` als öffentliche Instanz-Attribute.
      * Speichern Sie den Kontostand in einem "protected" Attribut namens `_balance`.

2.  **Kernmethoden (Instanz-Methoden):**

      * `deposit(self, amount)`: Erhöht den `_balance` um den gegebenen Betrag. Der Betrag muss positiv sein.
      * `withdraw(self, amount)`: Verringert den `_balance` um den Betrag. Dies darf nur geschehen, wenn der Betrag positiv ist UND der Kontostand (`_balance`) ausreichend Deckung aufweist. Geben Sie `True` zurück, wenn die Abhebung erfolgreich war, andernfalls `False`.
      * `get_balance(self)`: Eine "Getter"-Methode, die den Wert von `_balance` zurückgibt.

3.  **Operator Overloading (`__str__`):**

      * Implementieren Sie die `__str__(self)` Methode. Wenn `print()` auf ein `Account`-Objekt angewendet wird, soll ein formatierter String zurückgegeben werden, z.B.: `Konto 12345 (Inhaber: Max Mustermann), Stand: 500.00 EUR`.

4.  **Testen (in einer separaten `main.py`):**

      * Importieren Sie Ihre Klasse.
      * Erstellen Sie zwei verschiedene `Account`-Objekte.
      * Führen Sie einige `deposit` und `withdraw` Operationen durch.
      * Drucken Sie die Objekte (mit `print()`), um Ihre `__str__` Methode zu testen, und rufen Sie `get_balance()` auf.

### Bonus-Herausforderung

Erweitern Sie die `Account`-Klasse für fortgeschrittene Anforderungen:

1.  **Klassen-Attribut (Class Attribute):**

      * Fügen Sie ein Klassen-Attribut `MINIMUM_BALANCE` hinzu, das auf `0` gesetzt ist.
      * Passen Sie die `withdraw` Methode so an, dass sie prüft, ob der neue Kontostand unter `MINIMUM_BALANCE` fallen würde.

2.  **"Private" Attribute (Name Mangling):**

      * Ändern Sie das `_balance` Attribut zu `__balance` (mit zwei Unterstrichen).
      * Passen Sie alle Methoden (`deposit`, `withdraw`, `get_balance`, `__init__`, `__str__`) an, um stattdessen `self.__balance` zu verwenden.
      * Versuchen Sie (nachdem Sie die Methoden angepasst haben), in Ihrer `main.py` direkt auf `account.__balance` zuzugreifen. Was beobachten Sie? (Dies demonstriert Pythons *Name Mangling*).

3.  **Operator Overloading (`__eq__`):**

      * Implementieren Sie die `__eq__(self, other)` Methode (für den `==` Operator). Zwei Konten sollen als "gleich" gelten, wenn ihre `account_number` identisch ist.
