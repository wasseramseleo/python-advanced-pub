import time


class CodeTimer:
  """
  Ein Context Manager zum Messen der Ausführungszeit
  eines Code-Blocks.

  Verwendung:
  with CodeTimer(name="Mein Test"):
      # ... langsamer Code ...
  """

  def __init__(self, name: str = "Timer"):
    """
    Initialisiert den Timer.

    Args:
        name (str): Ein Name zur Identifizierung der Messung in der Ausgabe.
    """
    self.name = name
    self.start_time = 0.0

  def __enter__(self):
    """
    Startet den Timer, wenn der 'with'-Block betreten wird.
    """
    # time.perf_counter() ist ideal für Performance-Messungen
    self.start_time = time.perf_counter()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    """
    Stoppt den Timer und gibt die Dauer aus,
    wenn der 'with'-Block verlassen wird.

    Die exc_ (exception) Argumente sind für uns nicht relevant,
    aber erforderlich für die Signatur.
    """
    end_time = time.perf_counter()
    duration = end_time - self.start_time

    # Ausgabe der gemessenen Zeit
    print(f"\n--- [{self.name}] Code-Block beendet in {duration:.6f} Sekunden ---")
    # Wir geben nichts zurück (oder None),
    # was signalisiert, dass alle Exceptions normal weitergeleitet werden sollen.
