# Lab 14: Logging - Lösung

## Erläuterung der Lösung

### Angabe

Die Lösung besteht aus zwei Dateien, die die "Best Practice" der Trennung von Logger-Konfiguration (in der App) und Logger-Nutzung (in der Bibliothek) demonstrieren.

**1. `account.py` (Die Bibliothek)**

  * **Regel 2 (`getLogger(__name__)`):** Diese Datei holt sich nur ihren *eigenen* Logger. `__name__` wird magisch zu `"account"`, sodass wir in den Logs sehen können, woher die Nachricht stammt.
  * **Kein `basicConfig`:** Dieses Modul *konfiguriert nichts*. Es verlässt sich darauf, dass die aufrufende App (`main.py`) das Logging einrichtet.
  * **Performance:** Wir verwenden `log.info("Konto %s ...", var1, var2)` statt f-Strings. Das Logging-Framework formatiert den String nur, wenn die Nachricht tatsächlich protokolliert wird (d.h. wenn das Level `INFO` oder niedriger ist). Bei f-Strings (`log.info(f"Konto {var1}...")`) wird der String *immer* zuerst erstellt, auch wenn er (z.B. bei Log-Level `WARNING`) sofort wieder verworfen wird.
  * `calculate_internal_risk_score` wurde absichtlich fehlerhaft implementiert, um einen `ZeroDivisionError` für Regel 3 zu provozieren.

**2. `main.py` (Die Anwendung)**

  * **Regel 1 (Konfiguration):** Diese Datei (und *nur* diese) konfiguriert das Logging beim Start über `logging.basicConfig`. Sie stellt das Format und das globale Level (hier `DEBUG`) ein.
  * **Logger-Namen:** Wenn das Skript ausgeführt wird, sehen wir Logs von `__main__` (dem Logger von `main.py`) und von `account` (dem Logger des importierten Moduls).
  * **Regel 3 (Exception Logging):**
      * `log.error(f"Ein Fehler ist aufgetreten: {e}")`: Dies ist **FALSCH**. Die Ausgabe zeigt nur die Fehlermeldung (z.B. "division by zero"), aber nicht *wo* (welche Datei, welche Zeile) der Fehler aufgetreten ist. Der **Stack Trace** fehlt.
      * `log.exception(...)`: Dies ist **KORREKT**. Es protokolliert die Nachricht auf `ERROR`-Level und fügt *automatisch* den vollständigen Stack Trace hinzu. Dies ist für das Debugging unerlässlich.

### Bonus-Herausforderung

  * **Regel 4 (Structured Logging):** `basicConfig` wird durch `logging.config.dictConfig` ersetzt. Dies ist der empfohlene Weg für komplexe Anwendungen.
  * **JSON Formatter:** Wir weisen das `dictConfig` an, den `python-json-logger` als Formatter zu verwenden.
  * **Ergebnis:** Jede Log-Zeile ist jetzt ein separates, maschinenlesbares JSON-Objekt.
  * **Stack Trace in JSON:** `log.exception` funktioniert weiterhin, aber der Stack Trace wird nun sauber als String *innerhalb* des JSON-Feldes `exc_info` platziert.
  * **`extra={...}`:** Die Verwendung von `extra` im Bonus-Test (`log.info("App gestartet", ...`) zeigt, wie dem JSON-Log strukturierte Kontextdaten (wie `user_id`) hinzugefügt werden, die in Tools wie Kibana oder Datadog durchsuchbar sind.

## Python-Code: Angabe

### `account.py` (Modul / Bibliothek)

```python
import logging

# Regel 2: Logger auf Modulebene holen.
# __name__ wird hier zu "account"
log = logging.getLogger(__name__)

class BankAccount:
    """
    Stellt ein Bankkonto dar.
    Verwendet 'logging' statt 'print'.
    """
    def __init__(self, owner: str, account_number: str, balance: float):
        self.owner = owner
        self.account_number = account_number
        self._balance = balance
        
        # Info-Log (verwendet %-Formatierung für Performance)
        log.info("Konto %s für %s erstellt.", self.account_number, self.owner)

    def withdraw(self, amount: float) -> bool:
        """Hebt Geld ab."""
        if amount > self._balance:
            # Ersetzt 'print' durch 'log.warning'
            log.warning(
                "Nicht genügend Deckung für Konto %s (Saldo: %f, Abhebung: %f)",
                self.account_number, self._balance, amount
            )
            return False
        
        self._balance -= amount
        # Debug-Logs sind detaillierter und oft standardmäßig ausgeblendet
        log.debug("Abhebung von %f EUR von %s erfolgreich.", amount, self.account_number)
        return True

    def calculate_internal_risk_score(self, divisor: int) -> float:
        """
        Eine fehleranfällige Funktion, um ZeroDivisionError zu provozieren.
        """
        log.debug("Berechne Risikoscore mit Divisor %d", divisor)
        return self._balance / divisor

```

### `main.py` (Anwendung)

```python
import logging
from account import BankAccount # Import des Moduls

# Regel 1: Applikation konfiguriert das Logging EINMALIG
logging.basicConfig(
    level=logging.DEBUG, # Zeigt DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Logger für DIESE Datei holen (__name__ wird zu "__main__")
log = logging.getLogger(__name__)

def main():
    log.info("Starte die Banking-App...")
    
    acc1 = BankAccount("Max Mustermann", "AT123", 500.0)
    
    # Dieser Aufruf erzeugt ein WARNING-Log aus dem 'account'-Modul
    log.info("Teste absichtlich fehlgeschlagene Abhebung:")
    acc1.withdraw(99999)

    log.info("Teste absichtlich fehlerhafte Berechnung:")
    try:
        # Dieser Aufruf provoziert einen ZeroDivisionError
        acc1.calculate_internal_risk_score(0)
    except ZeroDivisionError as e:
        # Regel 3: Falsches vs. Richtiges Exception Logging
        
        log.error("--- FALSCH (log.error(f'...{e}')) ---")
        log.error(f"Ein Fehler ist aufgetreten: {e}")
        log.error("--- (Dieser Log hat keinen Stack Trace) ---")
        
        print("-" * 20)
        
        log.error("--- KORREKT (log.exception(...)) ---")
        log.exception("Schwerwiegender Fehler bei der Risikoberechnung")
        log.error("--- (Dieser Log hat den Stack Trace) ---")

    log.info("Banking-App beendet.")

if __name__ == "__main__":
    main()
```

## Python-Code: Bonus-Herausforderung

### `main.py` (Anwendung - JSON-Version)

*(Die Datei `account.py` bleibt exakt dieselbe wie in der Angabe.)*

```python
import logging
import logging.config
import sys
from account import BankAccount # Import des Moduls

# Regel 4: Strukturiertes Logging mit dictConfig
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False, # Wichtig, um Logger aus Modulen zu erhalten
    'formatters': {
        'json_formatter': {
            # Verwendet die installierte Bibliothek
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            # Fügt Zeit, Name, Level, Nachricht und den Stack Trace hinzu
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(exc_info)s'
        },
    },
    'handlers': {
        'console_json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter', # Den obigen Formatter verwenden
            'stream': 'ext://sys.stdout', # Nach stdout loggen
        },
    },
    'loggers': {
        '': { # Der Root-Logger (gilt für alle Logger)
            'level': 'DEBUG',
            'handlers': ['console_json'], # Den JSON-Handler verwenden
        },
    }
}

# Regel 1 (Ersetzt): Konfiguriert das Logging mit dem Dictionary
logging.config.dictConfig(LOGGING_CONFIG)

# Logger für DIESE Datei holen (__name__ wird zu "__main__")
log = logging.getLogger(__name__)

def main():
    # Bonus: Loggen mit 'extra' für strukturierte Daten
    log.info(
        "Starte die Banking-App (JSON-Modus)",
        extra={'user_id': 'SYSTEM', 'app_version': '2.0.1'}
    )
    
    acc1 = BankAccount("Max Mustermann", "AT123", 500.0)
    
    # Dieser Aufruf erzeugt ein WARNING-Log (jetzt als JSON)
    log.info("Teste absichtlich fehlgeschlagene Abhebung:")
    acc1.withdraw(99999)

    log.info("Teste absichtlich fehlerhafte Berechnung:")
    try:
        # Dieser Aufruf provoziert einen ZeroDivisionError
        acc1.calculate_internal_risk_score(0)
    except ZeroDivisionError as e:
        # log.exception funktioniert perfekt mit dem JSON-Logger.
        # Der Stack Trace wird in das 'exc_info'-Feld geschrieben.
        log.exception(
            "Schwerwiegender Fehler bei der Risikoberechnung",
            extra={'account_id': acc1.account_number}
        )

    log.info("Banking-App beendet.")

if __name__ == "__main__":
    main()
```