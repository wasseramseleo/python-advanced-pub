# Lab 8: Dekoratoren - Lösung

## Erläuterung der Lösung

### Angabe

Die Lösung implementiert einen Standard-Dekorator, der alle drei "Stolpersteine" korrekt behandelt:

1.  **`@functools.wraps(func)`**: Dies wird auf die `wrapper`-Funktion angewendet. Es kopiert die Metadaten (`__name__`, `__doc__` etc.) von der Originalfunktion `func` auf den `wrapper`. Ohne dies würden `deposit.__name__` und `get_balance.__name__` beide `"wrapper"` ausgeben, was Debugging und `help()` unmöglich macht.
2.  **`*args, **kwargs`**: Der `wrapper` wird anstelle der Originalfunktion aufgerufen. Er muss alle Argumente (Positions-Argumente `*args` und Keyword-Argumente `**kwargs`) annehmen, die für `func` bestimmt waren.
3.  **`result = func(...)` und `return result`**: Der `wrapper` muss den Rückgabewert der Originalfunktion `func` abfangen und selbst zurückgeben. Andernfalls würde der Dekorator den Rückgabewert "verschlucken" und der Aufrufer würde `None` erhalten.

Der `log_function_call`-Dekorator ist nun eine "transparente" Hülle, die Logging hinzufügt, ohne die Signatur oder das Verhalten der dekorierten Funktion zu ändern.

### Bonus-Herausforderung

Diese Lösung zeigt eine "Dekorator-Fabrik" (Decorator Factory).

1.  **Drei Ebenen**: Wir benötigen drei verschachtelte Funktionen, um ein Argument an den Dekorator selbst zu übergeben:
      * `require_role(required_role)`: Die äußerste Funktion. Sie wird sofort beim Laden des Skripts aufgerufen (wenn `@require_role('admin')` gelesen wird). Sie speichert das Argument (`'admin'`) im "Closure" und gibt den eigentlichen Dekorator zurück.
      * `decorator(func)`: Die mittlere Funktion. Dies ist der Standard-Dekorator, der die zu dekorierende Funktion (`func`) entgegennimmt und den `wrapper` zurückgibt.
      * `wrapper(*args, **kwargs)`: Die innerste Funktion. Sie enthält die eigentliche Logik (die Prüfung), die bei *jedem Aufruf* der dekorierten Funktion ausgeführt wird.
2.  **Logik im Wrapper**: Der `wrapper` extrahiert die `user_role` aus den `kwargs`. Dies ist eine gängige Methode, um kontextbezogene Informationen (wie den Benutzer) für Sicherheitsprüfungen bereitzustellen. Wenn die Prüfung fehlschlägt, wird die Originalfunktion `func` *nie* aufgerufen, und stattdessen wird eine Exception ausgelöst.

## Python-Code: Basis-Aufgabe

```python
import time
from functools import wraps

# --- Definition des Dekorators ---

def log_function_call(func):
    """
    Ein Dekorator, der den Aufruf einer Funktion protokolliert,
    inklusive Argument-Handling, Rückgabewerten und Metadaten.
    """
    
    @wraps(func) # 4. Metadaten erhalten (von func auf wrapper kopieren)
    def wrapper(*args, **kwargs):
        """Der Wrapper, der die eigentliche Logik ausführt."""
        
        # 3a. Logik VOR dem Aufruf
        print(f"LOG: Calling function '{func.__name__}'...")
        
        # 2. Aufruf der Originalfunktion mit allen Argumenten
        # 3b. Rückgabewert speichern
        result = func(*args, **kwargs)
        
        # 3c. Logik NACH dem Aufruf
        print(f"LOG: Function '{func.__name__}' finished.")
        
        # 3d. Rückgabewert zurückgeben
        return result

    # 5. Der Dekorator gibt den Wrapper zurück
    return wrapper

# === Kopiervorlage zum Testen ===

@log_function_call
def deposit(account_id: str, amount: float) -> str:
    """
    Simuliert eine Einzahlung auf ein Konto.
    Gibt einen Erfolgs-String zurück.
    """
    print(f"  -> Processing deposit: {amount} EUR for Account {account_id}")
    time.sleep(0.5) # Simuliert Arbeitsaufwand
    return f"Success: {amount} deposited."

@log_function_call
def get_balance(account_id: str) -> float:
    """
    Simuliert die Abfrage eines Kontostands.
    Gibt einen simulierten Kontostand zurück.
    """
    print(f"  -> Fetching balance for Account {account_id}")
    return 1000.00

# --- Aufrufe ---
print("--- Test 1: deposit ---")
result = deposit("AT12345", 500)
print(f"Return value: {result}")
print(f"Function name: {deposit.__name__}") # Korrekt: 'deposit'
print(f"Function docstring: {deposit.__doc__}") # Korrekt: Zeigt Docstring

print("\n--- Test 2: get_balance ---")
balance = get_balance("AT98765")
print(f"Return value: {balance}")
print(f"Function name: {get_balance.__name__}") # Korrekt: 'get_balance'
```

## Python-Code: Bonus-Herausforderung

```python
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

@require_role('admin') # Parameter 'admin' wird an require_role übergeben
def delete_account(account_id: str, user_role: str = 'guest'):
    """Löscht ein Konto (nur für Admins)."""
    print(f"SUCCESS: Account {account_id} wurde gelöscht.")
    return True

@require_role('user') # Parameter 'user'
def view_own_balance(account_id: str, user_role: str = 'guest'):
    """Zeigt Kontostand (für 'user' oder 'admin')."""
    print(f"SUCCESS: Zeige Kontostand für {account_id}.")
    return 123.45

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
```
