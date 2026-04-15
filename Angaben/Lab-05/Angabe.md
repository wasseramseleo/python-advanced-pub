# Lab 5: Iteratoren

## Lernziele

In diesem Lab implementieren Sie das Iterator-Protokoll, um speichereffizient durch große Datenmengen (z.B. Transaktionsverläufe) zu navigieren.

  * Den Unterschied zwischen "Iterable" (z.B. `list`) und "Iterator" (zustandsbehaftet) verstehen.
  * Eine Klasse durch Implementierung von `__iter__` "iterable" machen.
  * Eine separate Iterator-Klasse erstellen, die `__iter__` (gibt `self` zurück) und `__next__` (gibt Daten zurück) implementiert.
  * `StopIteration` korrekt auslösen und verwenden.

## Szenario

Unsere `BankAccount`-Klasse (aus Lab 1) wird erweitert. Jedes Konto speichert nun eine Liste von Transaktionen. Bei Konten mit *Millionen* von Transaktionen (z.B. bei Firmenkunden) würde das Laden des gesamten Verlaufs in eine Liste den Speicher sprengen.

Wir müssen eine Möglichkeit schaffen, die `BankAccount`-Klasse in einer `for`-Schleife zu verwenden (`for transaction in account:`), die die Transaktionen *eine nach der anderen* (lazy) bereitstellt, ohne jemals die gesamte Liste im Speicher zu halten.

### Angabe

**Ziel:** Machen Sie die `BankAccount`-Klasse "iterable", indem Sie das Iterator-Protokoll mit einer separaten Iterator-Klasse implementieren.

1.  **Vorbereitung:** Wir gehen von einer vereinfachten `BankAccount`-Klasse aus (siehe Kopiervorlage unten). Diese Klasse hält ihre Transaktionen vorerst in einem *privaten* Attribut `self.__transactions` (eine `list` von Strings).

    ```python
    class BankAccount:
        """
        Stellt ein Bankkonto dar, das (intern) eine Liste von Transaktionen hält.
        Wir verwenden hier eine vereinfachte Version von Lab 1.
        """
        def __init__(self, owner: str, account_number: str):
            self.owner = owner
            self.account_number = account_number
            # Hält den Verlauf. In der Realität wäre dies eine DB-Verbindung.
            # Wir simulieren es mit einer Liste.
            self.__transactions = [] 

        def deposit(self, amount: float):
            """Fügt eine Einzahlung als Transaktion hinzu."""
            # (Validierung etc. übersprungen)
            self.__transactions.append(f"DEPOSIT: {amount} EUR")

        def withdraw(self, amount: float):
            """Fügt eine Abhebung als Transaktion hinzu."""
            self.__transactions.append(f"WITHDRAW: {amount} EUR")

        def get_transactions(self) -> list:
            """
            NICHT ideal für große Datenmengen, da es die ganze Liste kopiert.
            """
            return self.__transactions.copy()
    ```

2.  **`AccountHistoryIterator` erstellen:**

      * Definieren Sie eine *neue, separate* Klasse `AccountHistoryIterator`.
      * Der `__init__(self, transactions)` soll die (gesamte) Transaktionsliste und einen Zähler (`self._index = 0`) initialisieren.
      * Implementieren Sie `__iter__(self)`: Diese Methode muss `self` zurückgeben.
      * Implementieren Sie `__next__(self)`:
          * Prüfen Sie, ob `self._index` das Ende der Transaktionsliste erreicht hat.
          * Falls ja: `raise StopIteration`.
          * Falls nein: Holen Sie die Transaktion am `self._index`, erhöhen Sie `self._index` um 1 und geben Sie die Transaktion zurück.

3.  **`BankAccount` anpassen:**

      * Fügen Sie der `BankAccount`-Klasse die Methode `__iter__(self)` hinzu.
      * Diese Methode soll eine *neue Instanz* des `AccountHistoryIterator` zurückgeben und ihm die `self.__transactions`-Liste übergeben.

4.  **Testen:**

      * Erstellen Sie ein `BankAccount`, rufen Sie `deposit()` und `withdraw()` mehrmals auf.
      * Nutzen Sie eine `for`-Schleife direkt auf dem Konto-Objekt, um die Transaktionen auszugeben:
        `for tx in my_account:`
        `     print(tx) `

-----

### Bonus-Herausforderung

**Ziel:** Den Iterator speichereffizient machen, sodass er *nicht* die gesamte Liste im Voraus benötigt, sondern Daten "lazy" aus einer Datei liest.

Die Basis-Aufgabe ist noch nicht speichereffizient, da der Iterator die *gesamte* `self.__transactions`-Liste als Kopie hält.

1.  **Szenario:** Stellen Sie sich vor, die Transaktionen liegen in einer riesigen Log-Datei (`transactions.log`).
2.  **`LazyTransactionReader` erstellen:**
      * Erstellen Sie eine *neue* Iterator-Klasse `LazyTransactionReader`.
      * Der `__init__(self, filename: str, filter_keyword: str = None)` soll den Dateinamen und ein optionales Filter-Wort speichern. Er soll die Datei hier *öffnen* und das Dateihandle (z.B. `self._file_handle`) speichern.
      * Implementieren Sie `__iter__(self)` (gibt `self` zurück).
      * Implementieren Sie `__next__(self)`:
          * Lesen Sie die *nächste* Zeile aus `self._file_handle`.
          * Wenn die Zeile leer ist (Ende der Datei, `""`): Rufen Sie `self.close()` auf (siehe nächster Schritt) und `raise StopIteration`.
          * Entfernen Sie Whitespace (z.B. `\n`) von der Zeile.
          * **Filter-Logik:** Wenn `filter_keyword` gesetzt ist *und* nicht in der Zeile vorkommt, *überspringen* Sie die Zeile (rufen Sie `__next__` rekursiv auf oder nutzen Sie eine `while`-Schleife intern) und suchen Sie weiter.
          * Geben Sie die gültige (oder ungefilterte) Zeile zurück.
      * Implementieren Sie eine `close(self)`-Methode, die das `self._file_handle` schließt, falls es offen ist.
3.  **Test:** Erstellen Sie manuell eine Textdatei `test_tx.log` und testen Sie Ihren Iterator mit `next()` und in einer `for`-Schleife, einmal mit und einmal ohne Filter (z.B. `filter_keyword="DEPOSIT"`).

