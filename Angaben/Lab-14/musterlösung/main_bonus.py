import logging
import logging.config
import sys
from account import BankAccount  # Import des Moduls

# Regel 4: Strukturiertes Logging mit dictConfig
LOGGING_CONFIG = {
  'version': 1,
  'disable_existing_loggers': False,  # Wichtig, um Logger aus Modulen zu erhalten
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
      'formatter': 'json_formatter',  # Den obigen Formatter verwenden
      'stream': 'ext://sys.stdout',  # Nach stdout loggen
    },
  },
  'loggers': {
    '': {  # Der Root-Logger (gilt für alle Logger)
      'level': 'DEBUG',
      'handlers': ['console_json'],  # Den JSON-Handler verwenden
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