from decorators_bonus import delete_account, view_own_balance

# --- Aufrufe ---
print("\n--- Bonus-Herausforderung Test ---")

# Test 1: Admin-Funktion als Admin (sollte klappen)
try:
  delete_account("AT12345", user_role='admin')
except PermissionError as e:
  print(f"Fehler: {e}")

# Test 2: Admin-Funktion als User (sollte fehlschlagen)
print("\n---")
try:
  delete_account("AT98765", user_role='user')
except PermissionError as e:
  print(f"Fehler (erwartet): {e}")

# Test 3: User-Funktion als User (sollte klappen)
print("\n---")
try:
  view_own_balance("AT456", user_role='user')
except PermissionError as e:
  print(f"Fehler: {e}")
