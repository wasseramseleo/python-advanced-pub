# Lab 9: Regular Expressions

## Lernziele

In diesem Lab verwenden Sie reguläre Ausdrücke (Regex), um unstrukturierte Textdaten aus Transaktionsprotokollen zu parsen und in strukturierte Informationen umzuwandeln.

  * Das `re`-Modul (insbesondere `re.search` und `re.findall`) korrekt anwenden.
  * Die Notwendigkeit von "Raw Strings" (z.B. `r"\d"`) verstehen.
  * Metazeichen (`\d`, `\w`, `\s`, `[A-Z]`), Quantifizierer (`+`, `*`, `{n}`) und Anker (`^`, `$`) verwenden.
  * **Capturing Groups** (`()`) nutzen, um spezifische Teile eines Musters zu extrahieren.
  * Den Unterschied zwischen `re.search` (ein Match-Objekt) und `re.findall` (eine Liste) verstehen.

## Szenario

Unsere Banking-App-Server produzieren Log-Dateien. Eine wichtige Art von Log ist der "Transaction Finalizer"-Bericht. Dieser Bericht wird als einfacher Text (String) generiert und enthält alle Details einer Transaktion in einer einzigen Zeile.

Wir müssen diese unstrukturierten Zeilen parsen, um die Daten in unsere Analyse-Datenbank zu laden.

### Angabe

**Ziel:** Extrahieren Sie die Transaktions-ID, den Betrag und den Status aus einer einzelnen Log-Zeile mit `re.search` und Capturing Groups.

**Gegebene Log-Zeile (als String):**
`log_entry = "INFO: [2024-10-28 10:30:01] Transaction 'T-45A-882' completed. Amount: 1500.75 EUR. Status: SUCCESS."`

**Ihre Aufgabe:**

1.  Importieren Sie das `re`-Modul.
2.  Erstellen Sie ein Regex-Muster (als **Raw String**: `r"..."`), das die folgenden drei Teile aus der `log_entry` "einfängt" (captured):
      * **Transaction ID:** (z.B. `T-45A-882`) Sie besteht aus "Wortzeichen" (`\w`) und Bindestrichen.
      * **Amount:** (z.B. `1500.75`) Dies ist eine Zahl (Ziffern `\d`, ein Punkt `\.`, Ziffern).
      * **Status:** (z.B. `SUCCESS`) Dies ist ein Wort am Ende (z.B. `\w+`).
3.  **Pattern-Tipps:**
      * Verwenden Sie `(...)` um die Teile, die Sie extrahieren möchten (die drei oben genannten).
      * Verwenden Sie `.*` (ein "gieriger" Platzhalter), um den Text *zwischen* den Teilen, die Sie interessieren, zu überbrücken.
      * Beispiel-Struktur: `r"Transaction '(.*)'.*Amount: (.*) EUR.*Status: (.*)\."` (Dies ist ein guter Start, aber Sie können es präziser machen).
4.  **Durchführung:**
      * Verwenden Sie `re.search(pattern, log_entry)`, um das Match-Objekt zu erhalten.
      * Prüfen Sie, ob ein Match gefunden wurde (z.B. `if match:`).
      * Wenn ja, geben Sie die extrahierten Gruppen aus:
          * `match.group(1)` (sollte die ID sein)
          * `match.group(2)` (sollte der Betrag sein)
          * `match.group(3)` (sollte der Status sein)

-----

### Bonus-Herausforderung

**Ziel:** Verarbeiten Sie einen *mehrzeiligen* Log-Block und finden Sie *alle* fehlgeschlagenen Transaktionen (`FAILED`) mithilfe von `re.compile` und `re.findall` (oder `re.finditer`).

**Gegebener Log-Block (Multiline-String):**

```python
log_block = """
INFO: [2024-10-28 10:30:01] Transaction 'T-45A-882' completed. Amount: 1500.75 EUR. Status: SUCCESS.
ERROR: [2024-10-28 10:31:05] Transaction 'T-12B-404' failed. Amount: 99.50 EUR. Status: FAILED.
INFO: [2024-10-28 10:32:15] Transaction 'T-99C-112' completed. Amount: 4500.00 EUR. Status: SUCCESS.
ERROR: [2024-10-28 10:33:00] Transaction 'T-15D-901' failed. Amount: 30.10 EUR. Status: FAILED.
"""
```

**Ihre Aufgabe:**

1.  **Kompilieren (Performance):** Erstellen Sie ein Regex-Muster, das *nur* die Transaktions-ID (`T-xxx-xxx`) aus Zeilen extrahiert, die `Status: FAILED` enthalten.
      * Tipp: `r"Transaction '([\w-]+)'.*Status: FAILED"`
2.  Verwenden Sie `re.compile(pattern)`, um ein kompiliertes Regex-Objekt zu erhalten. Dies ist effizienter, wenn ein Muster oft wiederverwendet wird.
3.  **Alle finden:** Verwenden Sie die `.findall()`-Methode des kompilierten Objekts auf dem `log_block`.
      * `failed_tx_ids = compiled_pattern.findall(log_block)`
4.  Geben Sie die Liste `failed_tx_ids` aus. Sie sollte `['T-12B-404', 'T-15D-901']` enthalten.

**(Alternative für Fortgeschrittene):** Verwenden Sie `re.finditer()` anstelle von `re.findall()`. `finditer` gibt einen Iterator von Match-Objekten zurück (speichereffizienter) statt einer Liste von Strings.
