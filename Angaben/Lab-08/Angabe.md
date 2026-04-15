# Lab 8: Dekoratoren

## Lernziele

In diesem Lab lagern Sie wiederkehrende Logik (wie Logging und Sicherheitsprüfungen) mithilfe von Dekoratoren aus Ihren Kernfunktionen aus.

  * Das DRY-Prinzip (Don't Repeat Yourself) durch Dekoratoren anwenden.
  * Eine Dekorator-Funktion erstellen, die eine `wrapper`-Funktion zurückgibt.
  * `*args` und `**kwargs` verwenden, um Argumente flexibel an die dekorierte Funktion durchzureichen.
  * Rückgabewerte korrekt verarbeiten.
  * `functools.wraps` verwenden, um die Metadaten (z.B. `__name__`, `__doc__`) der Originalfunktion zu erhalten.

## Szenario

Unsere Banking-App wächst. Wir stellen fest, dass wir an vielen Stellen (z.B. `deposit`, `withdraw`, `transfer`) identischen Code für Logging und Sicherheitsprüfungen hinzufügen. Das verstößt gegen das DRY-Prinzip.

Ihre Aufgabe ist es, einen universellen Logging-Dekorator zu erstellen, der diese Logik kapselt und einfach per `@`-Syntax zu jeder Funktion hinzugefügt werden kann.

### Angabe

**Ziel:** Erstellen Sie einen Dekorator `log_function_call`, der den Aufruf einer Funktion protokolliert.

1.  **Import:** Importieren Sie `wraps` aus dem `functools`-Modul.
2.  **Dekorator-Funktion:**
      * Definieren Sie eine Funktion `log_function_call(func)`.
      * Innerhalb von `log_function_call`, definieren Sie eine `wrapper`-Funktion.
      * **WICHTIG:** Der `wrapper` muss flexibel sein und alle möglichen Argumente akzeptieren. Verwenden Sie `*args` und `**kwargs`.
3.  **Wrapper-Logik:** Der `wrapper` soll:
      * Vor dem Aufruf: Eine Log-Nachricht ausgeben, z.B.: `LOG: Calling function '{func.__name__}'...`
      * Die Originalfunktion `func(*args, **kwargs)` aufrufen und deren Rückgabewert speichern (z.B. `result = ...`).
      * Nach dem Aufruf: Eine Log-Nachricht ausgeben, z.B.: `LOG: Function '{func.__name__}' finished.`
      * Den Rückgabewert der Originalfunktion (`result`) zurückgeben.
4.  **Metadaten erhalten:**
      * Dekorieren Sie Ihre *innere* `wrapper`-Funktion mit `@wraps(func)`, um sicherzustellen, dass `__name__` und `__doc__` der dekorierten Funktion erhalten bleiben.
5.  **Rückgabewert:** Der Dekorator `log_function_call` muss die `wrapper`-Funktion zurückgeben (`return wrapper`).

**Testen (Kopiervorlage):**

Verwenden Sie die folgenden Beispielfunktionen, um Ihren Dekorator zu testen.

```python
# === Kopiervorlage zum Testen ===
import time

# HIER IHREN DEKORATOR DEFINIEREN
# def log_function_call(func):
#    ...


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
print(f"Function name: {deposit.__name__}") # Sollte 'deposit' sein
print(f"Function docstring: {deposit.__doc__}") # Sollte den Docstring zeigen

print("\n--- Test 2: get_balance ---")
balance = get_balance("AT98765")
print(f"Return value: {balance}")
print(f"Function name: {get_balance.__name__}") # Sollte 'get_balance' sein
```

-----

### Bonus-Herausforderung

**Ziel:** Erstellen Sie einen *parametrisierten* Dekorator für die Zugriffskontrolle.

Manchmal muss ein Dekorator Argumente entgegennehmen (z.B. `@require_role('admin')`). Dies erfordert eine zusätzliche "Ebene" (eine Dekorator-Fabrik).

1.  **Szenario:** Wir benötigen einen Dekorator `require_role`, der prüft, ob der aufrufende Benutzer die erforderliche Rolle hat.
2.  **Implementierung:**
      * Erstellen Sie eine Funktion `require_role(required_role: str)`. Dies ist die "Fabrik", die das Argument (`'admin'`) entgegennimmt.
      * *Innerhalb* dieser Funktion, definieren Sie den eigentlichen Dekorator (`def decorator(func):`).
      * *Innerhalb* des Dekorators, definieren Sie den `wrapper(*args, **kwargs)`. (Insgesamt 3 Ebenen).
      * Verwenden Sie `@wraps(func)` auf dem `wrapper`.
3.  **Wrapper-Logik (Simulation):**
      * Wir simulieren den "angemeldeten Benutzer", indem wir annehmen, dass die dekorierte Funktion immer ein Keyword-Argument `user_role` erhält.
      * Der `wrapper` muss das `user_role` Keyword-Argument aus `kwargs` extrahieren (z.B. `kwargs.get('user_role', 'guest')`).
      * **Prüfung:** Wenn `user_role == required_role`, rufen Sie die Originalfunktion `func(*args, **kwargs)` auf und geben Sie das Ergebnis zurück.
      * **Fehlerfall:** Wenn die Rollen nicht übereinstimmen, lösen Sie einen `PermissionError` aus (z.B. `raise PermissionError(f"Access denied. Requires role: {required_role}")`).
4.  **Test:** Dekorieren Sie eine Funktion `delete_account` mit `@require_role('admin')` und testen Sie den Aufruf mit `user_role='admin'` (sollte klappen) und `user_role='user'` (sollte einen `PermissionError` auslösen).
