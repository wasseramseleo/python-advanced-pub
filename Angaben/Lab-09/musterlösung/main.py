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
  print(f"  Amount (als float):       {amount_float}")

else:
  print(f"Kein Match gefunden für Log-Eintrag: {log_entry}")

# Test mit einer fehlerhaften Zeile
failed_log_entry = "INFO: Invalid log format."
match_fail = re.search(pattern_str, failed_log_entry)

if not match_fail:
  print("\nTest mit ungültigem Log: Kein Match (Erwartet).")