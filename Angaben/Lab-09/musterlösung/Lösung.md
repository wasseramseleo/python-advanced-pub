# Lab 9: Regular Expressions - Lösung

## Erläuterung der Lösung

### Angabe

Die Lösung verwendet `re.search`, um die *erste* Übereinstimmung im String zu finden, und gibt ein Match-Objekt zurück.

1.  **Pattern (Muster):** `r"Transaction '([\w-]+)'.*Amount: (\d+\.\d{2}).*Status: (\w+)\."`

      * `r"..."`: Ein "Raw String", um sicherzustellen, dass Backslashes (wie `\d`) als Regex-Metazeichen und nicht als Python-Escape-Sequenzen interpretiert werden.
      * `Transaction '` & ` .*Amount:  ` & ` .*Status:  `: Dies sind die Literale, nach denen wir suchen. `.*` bedeutet "beliebiges Zeichen (`.`), null oder mehrmals (`*`)" – es überbrückt den Text.
      * **Gruppe 1: `([\w-]+)`**
          * `(...)`: Dies ist eine "Capturing Group". Was hier matched, wird in `match.group(1)` gespeichert.
          * `[\w-]`: Ein Zeichensatz. Erlaubt jedes "Wortzeichen" (`\w`, d.h. `a-z`, `A-Z`, `0-9`, `_`) ODER einen Bindestrich (`-`).
          * `+`: Quantifizierer, bedeutet "eines oder mehrere" der vorhergehenden Zeichen.
      * **Gruppe 2: `(\d+\.\d{2})`**
          * `(...)`: Gruppe 2, gespeichert in `match.group(2)`.
          * `\d+`: Eine oder mehrere Ziffern (der Teil vor dem Komma).
          * `\.`: Ein literaler Punkt. Wir müssen den Punkt "escapen", da `.` alleine "jedes Zeichen" bedeutet.
          * `\d{2}`: Genau zwei Ziffern (der Teil nach dem Komma).
      * **Gruppe 3: `(\w+)`**
          * `(...)`: Gruppe 3, gespeichert in `match.group(3)`.
          * `\w+`: Ein oder mehrere Wortzeichen (z.B. `SUCCESS` oder `FAILED`).

2.  **`match.group(n)`**: `re.search` gibt `None` zurück, wenn nichts gefunden wird. Wenn es erfolgreich ist (der `if match:`-Block), füllt es die Gruppen. `match.group(0)` (oder `match.group()`) würde den *gesamten* gematchten Text enthalten (von "Transaction..." bis "...SUCCESS."). `group(1)`, `group(2)` usw. enthalten nur den Text, der von den jeweiligen Klammern `()` erfasst wurde.

### Bonus-Herausforderung

1.  **`re.compile(pattern)`**: Wenn ein Regex-Muster (insbesondere in einer Schleife) wiederholt verwendet wird, ist es effizienter, es einmal zu kompilieren. `re.compile` erstellt ein Pattern-Objekt, das seine eigene `findall`-Methode besitzt.
2.  **Pattern:** `r"Transaction '([\w-]+)'.*Status: FAILED"`
      * Dies ist präziser. Es sucht nach dem Literal `Status: FAILED` am Ende.
      * Es hat *nur eine* Capturing Group `([\w-]+)` für die ID.
3.  **`findall()`**: Im Gegensatz zu `re.search` durchsucht `findall` den *gesamten* String und findet *alle* Übereinstimmungen.
      * **Wichtig:** Wenn das Muster Capturing Groups enthält (wie unseres), gibt `findall` eine **Liste der Gruppen-Inhalte** zurück (eine Liste von Strings).
      * Wenn das Muster *keine* Gruppen hätte, würde `findall` eine Liste der *gesamten* gematchten Texte zurückgeben.
      * Da wir nur die ID (Gruppe 1) wollten, ist dies perfekt. Das Ergebnis ist `['T-12B-404', 'T-15D-901']`.

## Python-Code: Basis-Aufgabe

```python
import re

print("--- Angabe Test ---")

# Die gegebene Log-Zeile
log_entry = "INFO: [2024-10-28 10:30:01] Transaction 'T-45A-882' completed. Amount: 1500.75 EUR. Status: SUCCESS."

# 1. Das Regex-Muster als Raw String
# Gruppe 1: Transaction ID (z.B. T-45A-882)
# Gruppe 2: Amount (z.B. 1500.75)
# Gruppe 3: Status (z.B. SUCCESS)
pattern_str = r"Transaction '([\w-]+)'.*Amount: (\d+\.\d{2}).*Status: (\w+)\."

# 2. re.search verwenden
match = re.search(pattern_str, log_entry)

# 3. Prüfen, ob ein Match gefunden wurde
if match:
    print("Log-Eintrag erfolgreich geparst:")
    
    # 4. Die extrahierten Gruppen ausgeben
    # match.group(0) ist der gesamte Treffer
    # print(f"  Gesamter Match (Group 0): {match.group(0)}") 
    
    txn_id = match.group(1)
    amount = match.group(2)
    status = match.group(3)
    
    print(f"  Transaction ID (Group 1): {txn_id}")
    print(f"  Amount (Group 2):         {amount}")
    print(f"  Status (Group 3):         {status}")
    
    # Wir können den Betrag jetzt als Zahl verwenden
    amount_float = float(amount)
    print(f"  Amount (als float):     {amount_float}")
    
else:
    print(f"Kein Match gefunden für Log-Eintrag: {log_entry}")

# Test mit einer fehlerhaften Zeile
failed_log_entry = "INFO: Invalid log format."
match_fail = re.search(pattern_str, failed_log_entry)

if not match_fail:
    print("\nTest mit ungültigem Log: Kein Match (Erwartet).")
```

## Python-Code: Bonus-Herausforderung

```python
import re

print("\n--- Bonus-Herausforderung Test ---")

# Der gegebene mehrzeilige Log-Block
log_block = """
INFO: [2024-10-28 10:30:01] Transaction 'T-45A-882' completed. Amount: 1500.75 EUR. Status: SUCCESS.
ERROR: [2024-10-28 10:31:05] Transaction 'T-12B-404' failed. Amount: 99.50 EUR. Status: FAILED.
INFO: [2024-10-28 10:32:15] Transaction 'T-99C-112' completed. Amount: 4500.00 EUR. Status: SUCCESS.
ERROR: [2024-10-28 10:33:00] Transaction 'T-15D-901' failed. Amount: 30.10 EUR. Status: FAILED.
"""

# 1. Muster, das die ID (Gruppe 1) nur dann findet, 
#    wenn der Status FAILED ist.
failed_pattern_str = r"Transaction '([\w-]+)'.*Status: FAILED"

# 2. Muster kompilieren (gut für die Wiederverwendung)
compiled_pattern = re.compile(failed_pattern_str)

# 3. findall() auf dem kompilierten Objekt verwenden
# findall() gibt eine Liste der Inhalte der Capturing Group (Gruppe 1) zurück
failed_tx_ids = compiled_pattern.findall(log_block)

# 4. Ergebnisse ausgeben
print(f"Gefundene FAILED Transaction IDs: {failed_tx_ids}")


# --- Alternative mit re.finditer ---
print("\nAlternative mit re.finditer (speichereffizient):")
# finditer gibt einen Iterator über Match-Objekte zurück
matches_iterator = compiled_pattern.finditer(log_block)

for match in matches_iterator:
    # Hier müssen wir .group(1) manuell aufrufen
    print(f"  Match gefunden: ID={match.group(1)} (bei Index {match.start()})")
```
