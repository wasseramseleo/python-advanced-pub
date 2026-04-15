# Lab 6: Map, Filter & Reduce

## Lernziele

In diesem Lab analysieren Sie Transaktionsdaten mithilfe von funktionalen Programmierkonzepten.

  * `lambda`-Funktionen für "Inline"-Logik erstellen und anwenden.
  * `map()` für 1:1-Transformationen von Daten verwenden.
  * `filter()` zur Selektion von Daten basierend auf einem Prädikat verwenden.
  * `reduce()` (aus `functools`) zur Aggregation von Daten auf einen Einzelwert verwenden.
  * Den Unterschied (und die Lesbarkeit) zu List Comprehensions bewerten.

## Szenario

Die Finanzabteilung unserer Banking-App muss eine Reihe von Ad-hoc-Analysen für einen Stapel von Transaktionen durchführen, die kürzlich verarbeitet wurden. Die Rohdaten liegen als eine `list` von `dict`-Objekten vor.

Ihre Aufgabe ist es, diese Analysen schnell und "funktional" durchzuführen, ohne komplexe Klassen oder mehrzeilige `for`-Schleifen zu schreiben.

### Daten-Grundlage

Verwenden Sie die folgende Liste als Startpunkt für alle Aufgaben:

```python
# Eine Liste von Transaktions-Dictionaries
transactions = [
    {'id': 'T1001', 'type': 'DEPOSIT', 'amount': 5000.00, 'currency': 'EUR'},
    {'id': 'T1002', 'type': 'WITHDRAW', 'amount': 1200.00, 'currency': 'EUR'},
    {'id': 'T1003', 'type': 'DEPOSIT', 'amount': 350.75, 'currency': 'EUR'},
    {'id': 'T1004', 'type': 'PAYMENT', 'amount': 89.90, 'currency': 'EUR'},
    {'id': 'T1005', 'type': 'WITHDRAW', 'amount': 2000.00, 'currency': 'EUR'},
    {'id': 'T1006', 'type': 'DEPOSIT', 'amount': 1500.00, 'currency': 'USD'}, # Beachte USD!
]
```

### Angabe

Führen Sie die folgenden drei Analysen durch. Jede Aufgabe soll **primär mit der angegebenen Funktion** und einer `lambda`-Funktion gelöst werden.

1.  **Task 1: `map` (1:1-Transformation)**

      * **Ziel:** Das Management benötigt eine Liste aller Transaktionsbeträge (`amount`), umgerechnet in Cent (z.B. `5000.00` -\> `500000`).
      * **Aktion:** Erstellen Sie eine `list` namens `amounts_in_cents`, indem Sie `map()` auf die `transactions`-Liste anwenden. Die `lambda`-Funktion soll das `amount`-Feld extrahieren und mit 100 multiplizieren.

2.  **Task 2: `filter` (N:M-Selektion)**

      * **Ziel:** Die Compliance-Abteilung benötigt eine Liste aller "High-Value" Einzahlungen (`DEPOSIT`) über 400 EUR.
      * **Aktion:** Erstellen Sie eine `list` namens `high_value_deposits`, indem Sie `filter()` auf die `transactions`-Liste anwenden. Die `lambda`-Funktion muss `True` zurückgeben, wenn `type == 'DEPOSIT'` *und* `amount > 400` ist.

3.  **Task 3: `reduce` (N:1-Aggregation)**

      * **Ziel:** Die Buchhaltung benötigt die Gesamtsumme aller Abhebungen (`WITHDRAW`).
      * **Aktion:** Importieren Sie `reduce` aus `functools`.
      * **Tipp:** Sie müssen eventuell `filter` und `map` *vor* `reduce` anwenden (oder die Logik in die `reduce`-Funktion einbauen). Am einfachsten: Filtern Sie zuerst alle `WITHDRAW`s, `map`-en Sie diese auf ihre `amount`-Werte und *dann* `reduce`-en Sie die Ergebnisliste zur Summe.

-----

### Bonus-Herausforderung

**Ziel:** Vergleichen Sie die Lesbarkeit von `map`/`filter` mit List Comprehensions und lösen Sie eine komplexere Aggregationsaufgabe.

1.  **Refactoring für verbesserte Lesbarkeit:**

      * Implementieren Sie **Task 1 (`map`)** und **Task 2 (`filter`)** aus der Kernaufgabe erneut, aber diesmal unter Verwendung von **List Comprehensions** anstelle von `map` und `filter`.
      * Speichern Sie die Ergebnisse in `amounts_in_cents_lc` und `high_value_deposits_lc`.
      * *Keine Lösung erforderlich, nur Implementierung.*

2.  **Advanced `reduce` (Komplexe Aggregation):**

      * **Ziel:** Finden Sie die *gesamte* Transaktion (`dict`) mit dem **höchsten Einzahlungsbetrag (`DEPOSIT`)** in EUR.
      * **Aktion:**
          * Filtern Sie zuerst alle `DEPOSIT`-Transaktionen in EUR.
          * Verwenden Sie `reduce` auf der gefilterten Liste.
          * Die `lambda`-Funktion für `reduce` ist anspruchsvoll: Sie nimmt zwei Argumente (`acc` = Akkumulator, `curr` = aktuelles Element). Beide sind Transaktions-Dictionaries.
          * Die Funktion muss `acc` zurückgeben, wenn dessen `amount` größer ist als der `amount` von `curr`, andernfalls muss sie `curr` zurückgeben.
      * **Tipp:** `reduce` benötigt einen `initializer` (Anfangswert), wenn die Liste leer sein könnte. Um es einfacher zu halten, können Sie davon ausgehen, dass die gefilterte Liste nicht leer ist.
