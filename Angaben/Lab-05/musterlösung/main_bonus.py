from lazy_transaction_reader import LazyTransactionReader


log_filename = "test_tx.log"

# --- Beispiel-Nutzung (Bonus) ---
print("\n--- Bonus-Herausforderung Test 1 (alle Transaktionen) ---")
try:
  # 1. Alle Transaktionen lesen
  all_tx_reader = LazyTransactionReader(log_filename)
  for line in all_tx_reader:
    print(f"  Gelesene Zeile: {line}")
  # Beachte: Die Datei sollte jetzt automatisch geschlossen sein.

except FileNotFoundError:
  pass  # Fehler wurde bereits im Konstruktor behandelt

print("\n--- Bonus-Herausforderung Test 2 (nur 'DEPOSIT') ---")
try:
  # 2. Nur Einzahlungen (DEPOSIT) filtern
  deposit_reader = LazyTransactionReader(log_filename, filter_keyword="DEPOSIT")

  print(f"Nächstes Element (manuell): {next(deposit_reader)}")
  print(f"Nächstes Element (manuell): {next(deposit_reader)}")

  # Test auf StopIteration
  try:
    next(deposit_reader)
  except StopIteration:
    print("  Erwartete StopIteration! Der Filter-Iterator ist erschöpft.")

except FileNotFoundError:
  pass

