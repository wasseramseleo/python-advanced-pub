import logging
from account import BankAccount  # Import des Moduls

# Regel 1: Applikation konfiguriert das Logging EINMALIG
logging.basicConfig(
  level=logging.DEBUG,  # Zeigt DEBUG, INFO, WARNING, ERROR, CRITICAL
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

    log.error("--- KORREKT (log.exception(...)) ---")
    log.exception("Schwerwiegender Fehler bei der Risikoberechnung")
    log.error("--- (Dieser Log hat den Stack Trace) ---")

  log.info("Banking-App beendet.")


if __name__ == "__main__":
  main()