import re

print("\n--- Bonus-Herausforderung Test ---")


log_block = """
INFO: [2024-10-28 10:30:01] Transaction 'T-45A-882' completed. Amount: 1500.75 EUR. Status: SUCCESS.
ERROR: [2024-10-28 10:31:05] Transaction 'T-12B-404' failed. Amount: 99.50 EUR. Status: FAILED.
INFO: [2024-10-28 10:32:15] Transaction 'T-99C-112' completed. Amount: 4500.00 EUR. Status: SUCCESS.
ERROR: [2024-10-28 10:33:00] Transaction 'T-15D-901' failed. Amount: 30.10 EUR. Status: FAILED.
"""

# 1. Muster, das die ID (Gruppe 1) nur dann findet, wenn der Status FAILED ist.
failed_pattern_str = r"Transaction '([\w-]+)'.*Status: FAILED"

# 2. Muster kompilieren (gut für die Wiederverwendung)
compiled_pattern = re.compile(failed_pattern_str)

# 3. findall() auf dem kompilierten Objekt verwenden
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