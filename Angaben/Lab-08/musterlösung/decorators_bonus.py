from functools import wraps


# --- Definition des parametrisierten Dekorators ---

def require_role(required_role: str):
  """
  Dekorator-Fabrik (Ebene 1): Nimmt das Argument
  für den Dekorator entgegen (z.B. 'admin').
  """

  def decorator(func):
    """
    Der eigentliche Dekorator (Ebene 2):
    Nimmt die Funktion entgegen.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
      """
      Der Wrapper (Ebene 3): Führt die Prüfung
      und die Funktion aus.
      """

      # 3. Wrapper-Logik (simulierte Prüfung)
      # Wir erwarten 'user_role' als Keyword-Argument
      print(args)
      user_role = kwargs.get('user_role', 'guest')

      if user_role == required_role:
        # Prüfung bestanden: Funktion aufrufen
        print(f"SECURITY: Role '{user_role}' OK. Proceeding.")
        return func(*args, **kwargs)
      else:
        # Prüfung fehlgeschlagen: Fehler auslösen
        print(f"SECURITY: Role '{user_role}' REJECTED.")
        raise PermissionError(
          f"Access denied. Requires role: '{required_role}'"
        )

    return wrapper

  return decorator


# --- Test-Funktionen ---

@require_role('admin')  # Parameter 'admin' wird an require_role übergeben
def delete_account(account_id: str, user_role: str = 'guest'):
  """Löscht ein Konto (nur für Admins)."""
  print(f"SUCCESS: Account {account_id} wurde gelöscht.")
  return True


@require_role('user')  # Parameter 'user'
def view_own_balance(account_id: str, user_role: str = 'guest'):
  """Zeigt Kontostand (für 'user' oder 'admin')."""
  print(f"SUCCESS: Zeige Kontostand für {account_id}.")
  return 123.45
