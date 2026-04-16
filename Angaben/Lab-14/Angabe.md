# Lab 14: Logging

## Lernziele

In diesem Lab ersetzen Sie unzureichende `print()`-Anweisungen durch professionelles Logging.

  * Die `logging.config`-Methoden (z.B. `basicConfig`) zur *Konfiguration* in einer Hauptanwendung verwenden.
  * `logging.getLogger(__name__)` in *Modulen* (Bibliotheken) verwenden, anstatt Logging zu konfigurieren.
  * Den Unterschied zwischen `log.error(f"{e}")` (schlecht) und `log.exception(...)` (gut) verstehen und anwenden.
  * (Bonus) Strukturiertes Logging (JSON) für maschinelle Auswertbarkeit einrichten.

## Szenario

Die `BankAccount`-Klasse ist jetzt ein eigenständiges Modul (`account.py`). Unsere Hauptanwendung (`main.py`) importiert und verwendet es.

Aktuell verwendet die `BankAccount`-Klasse `print()`-Anweisungen, um über Fehler (z.B. "Nicht genügend Deckung") zu informieren. Dies ist in einer Produktionsumgebung inakzeptabel. Gleichzeitig fängt `main.py` Exceptions ab, protokolliert sie aber falsch, wodurch wertvolle Stack-Trace-Informationen verloren gehen.

Ihre Aufgabe ist es, ein robustes Logging-System nach "Best Practices" zu implementieren.


Dieses Lab erfordert zwei Dateien: `account.py` (die "Bibliothek") und `main.py` (die "Anwendung").

### Angabe

**Ziel:** Implementieren Sie `getLogger(__name__)` im Modul und `basicConfig` in der App. Demonstrieren Sie das korrekte Loggen von Exceptions.

**1. Datei: `account.py` (Das Modul)**

1.  Importieren Sie `logging`.
2.  Holen Sie sich den Modul-Logger: `log = logging.getLogger(__name__)` (ganz oben auf Modulebene).
3.  Erstellen Sie die `BankAccount`-Klasse (siehe Kopiervorlage).
4.  **Refactoring:** Ersetzen Sie die `print()`-Anweisung in der `withdraw`-Methode durch ein `log.warning(...)`. Verwenden Sie String-Formatierungs-Platzhalter (z.B. `log.warning("Nachricht für %s", self.account_number)`), nicht f-Strings, um die Log-Formatierung zu optimieren.
5.  **Fehler simulieren:** Fügen Sie eine "fehlerhafte" Methode `calculate_internal_risk_score(self, divisor)` hinzu, die einfach `self._balance / divisor` zurückgibt. (Wir werden `0` übergeben, um einen `ZeroDivisionError` zu provozieren).

<!-- end list -->

```python
# === Kopiervorlage für account.py ===
# 1. Import logging
# 2. Logger holen (log = ...)

class BankAccount:
    def __init__(self, owner: str, account_number: str, balance: float):
        self.owner = owner
        self.account_number = account_number
        self._balance = balance
        # 3. Info-Log hinzufügen
        log.info("Konto %s für %s erstellt.", self.account_number, self.owner)

    def withdraw(self, amount: float) -> bool:
        if amount > self._balance:
            # 4. TODO: 'print' durch 'log.warning' ersetzen
            print(f"Nicht genügend Deckung für {self.account_number}")
            return False
        
        self._balance -= amount
        log.debug("Abhebung von %f EUR von %s erfolgreich.", amount, self.account_number)
        return True

    # 5. TODO: Fehlerhafte Methode hinzufügen
    # def calculate_internal_risk_score(self, divisor):
    #    ...
```

**2. Datei: `main.py` (Die Anwendung)**

1.  Importieren Sie `logging` und die `BankAccount`-Klasse aus `account.py`.
2.  **Konfiguration (Regel 1):** Konfigurieren Sie das Logging *nur hier*. Verwenden Sie `logging.basicConfig(...)`.
      * Setzen Sie `level=logging.DEBUG`.
      * Setzen Sie ein `format` (z.B. `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`).
3.  Holen Sie sich den *Applikations*-Logger: `log = logging.getLogger(__name__)`.
4.  Erstellen Sie eine `BankAccount`-Instanz.
5.  Rufen Sie `acc.withdraw(99999)` auf (um die `log.warning`-Meldung aus dem Modul zu sehen).
6.  **Fehler abfangen (Regel 3):**
      * Erstellen Sie einen `try...except ZeroDivisionError as e:` Block.
      * Rufen Sie im `try`-Block `acc.calculate_internal_risk_score(0)` auf.
      * Im `except`-Block:
          * Loggen Sie den Fehler *zuerst FALSCH*: `log.error(f"Ein Fehler ist aufgetreten: {e}")`
          * Loggen Sie den Fehler *danach KORREKT*: `log.exception("Schwerwiegender Fehler bei der Risikoberechnung")`
7.  **Analyse:** Führen Sie `main.py` aus und vergleichen Sie die beiden Log-Ausgaben im `except`-Block. Was fehlt bei der ersten?

-----

### Bonus-Herausforderung

**Ziel:** Ersetzen Sie `basicConfig` durch `dictConfig` und implementieren Sie strukturiertes JSON-Logging (Regel 4).

1.  **Installation:** Sie benötigen einen JSON-Logger.
    `pip install python-json-logger`
2.  **Refactoring `main.py`:**
      * Importieren Sie `logging.config`.
      * Entfernen Sie `logging.basicConfig(...)`.
      * Definieren Sie eine `LOGGING_CONFIG`-Dictionary (siehe Kopiervorlage unten).
      * Konfigurieren Sie den Logger *einmalig* mit `logging.config.dictConfig(LOGGING_CONFIG)`.
      * Fügen Sie im `main` einen Log-Aufruf mit Zusatzinformationen hinzu:
        `log.info("App gestartet", extra={'user_id': 123, 'app_version': '2.0.1'})`
3.  **Analyse:** Führen Sie `main.py` erneut aus. Die gesamte Ausgabe (auch die Fehler und Stack Traces) sollte nun im JSON-Format vorliegen, bereit für ein Tool wie Datadog oder ELK.

**Kopiervorlage für `LOGGING_CONFIG` (in `main.py` einzufügen):**

```python
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formatter': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(exc_info)s'
        },
    },
    'handlers': {
        'console_json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter', # Den obigen Formatter verwenden
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': { # Der Root-Logger
            'level': 'DEBUG',
            'handlers': ['console_json'], # Den JSON-Handler verwenden
        },
    }
}
```
