## Lab 3: Datetime & With – Transaktions-Logging

In unseren bisherigen Labs (1 und 2) führen die `Account`-Objekte Aktionen aus, hinterlassen aber keine Spuren. Für eine echte Banken-App ist es unerlässlich, *wann* eine Transaktion stattgefunden hat (Timestamping) und diese Aktionen *dauerhaft* zu protokollieren (Logging).

In diesem Lab erweitern wir unsere `Account`-Klasse, um jede Ein- und Auszahlung mit einem genauen Zeitstempel in eine separate Log-Datei zu schreiben. Wir verwenden das `datetime`-Modul für die Zeitstempel und das `with`-Statement (Context Manager) für ein sicheres und sauberes Datei-Handling.

### Lernziele

  * Das `datetime`-Modul zur Abfrage der aktuellen Zeit und zur Formatierung von Zeitstempeln verwenden.
  * Verstehen, was ein Context Manager ist.
  * Das `with`-Statement verwenden, um Ressourcen (wie Dateien) sicher zu öffnen und zu schließen.
  * Die Vorteile von `with` gegenüber einem manuellen `try...finally`-Block erkennen.

### Szenario

Die Compliance-Abteilung verlangt, dass alle Kontobewegungen (Ein- und Auszahlungen) in einem "Transaction Log" gespeichert werden. Jedes Konto muss eine eigene Log-Datei erhalten. Jede Log-Zeile muss einen ISO-formatierten Zeitstempel und eine Beschreibung der Aktion enthalten.

Wir werden die `Account`-Klasse aus Lab 1 direkt modifizieren, um diese Logging-Funktion zu implementieren.

-----

### Basis Aufgabe

**Voraussetzung:** Sie benötigen Ihre `account.py` aus Lab 1.

#### Kernaufgabe: Logging für `Account` implementieren

Modifizieren Sie Ihre bestehende `Account`-Klasse in `account.py`.

1.  **Import:** Importieren Sie das `datetime`-Modul am Anfang Ihrer `account.py` Datei (`import datetime`).
2.  **`__init__` anpassen:**
      * Fügen Sie im Konstruktor (`__init__`) ein neues Attribut hinzu: `self.log_file_path = f"log_account_{self.account_number}.txt"`. Jedes Konto-Objekt weiß nun, wo seine Log-Datei liegt.
3.  **Neue Logging-Methode:**
      * Erstellen Sie eine neue "protected" Methode: `_log_transaction(self, message: str)`.
      * Diese Methode soll:
          * Einen Zeitstempel generieren: `timestamp = datetime.datetime.now().isoformat()`
          * Einen Log-Eintrag formatieren: `log_entry = f"[{timestamp}] {message}\n"`
          * **Wichtig:** Das `with`-Statement verwenden, um die Datei zu öffnen und den `log_entry` hinzuzufügen.
          * Verwenden Sie `with open(self.log_file_path, mode="a", encoding="utf-8") as f:`
          * Schreiben Sie den Eintrag mit `f.write(log_entry)`.
      * (Der Modus `"a"` steht für "append", d.h. Hinzufügen am Ende der Datei).
4.  **Logging integrieren:**
      * Rufen Sie Ihre neue `_log_transaction`-Methode innerhalb der `deposit`- und `withdraw`-Methoden auf.
      * **In `deposit()`:** Wenn die Einzahlung erfolgreich war, rufen Sie `self._log_transaction(f"Einzahlung: +{amount:.2f} EUR")` auf.
      * **In `withdraw()`:** Wenn die Abhebung erfolgreich war, rufen Sie `self._log_transaction(f"Abhebung: -{amount:.2f} EUR")` auf. Wenn sie fehlschlug (z.B. nicht Gedeckt), rufen Sie `self._log_transaction(f"Abhebung fehlgeschlagen (Betrag: {amount:.2f} EUR)")` auf.
5.  **Testen:**
      * Passen Sie Ihre `main.py` an. Erstellen Sie ein oder zwei `Account`-Objekte.
      * Führen Sie mehrere erfolgreiche und eine fehlgeschlagene Transaktion durch.
      * Führen Sie das Skript aus.
      * Überprüfen Sie Ihr Projektverzeichnis: Sie sollten neue Dateien sehen (z.B. `log_account_AT001.txt`). Öffnen Sie diese und prüfen Sie, ob alle Transaktionen mit Zeitstempel protokolliert wurden.

#### Bonus-Herausforderung: Ein eigener Context Manager (`CodeTimer`)

Das `with`-Statement ist nicht nur für Dateien nützlich. Man kann *eigene* Context Manager schreiben. Wir erstellen einen `CodeTimer`, um zu messen, wie lange ein Code-Block für die Ausführung benötigt.

1.  **Neue Datei `utils.py`:** Erstellen Sie eine neue Datei `utils.py`.
2.  **Import:** Importieren Sie `time` (oder `datetime`). Wir verwenden `time.perf_counter()` für eine präzise Messung (`import time`).
3.  **`CodeTimer` Klasse definieren:**
      * Definieren Sie `class CodeTimer:`.
      * Implementieren Sie `__init__(self, name: str = "Timer")`. Speichern Sie `name`.
      * Implementieren Sie `__enter__(self)`. Diese Methode soll:
          * Die Startzeit speichern: `self.start_time = time.perf_counter()`.
          * Sich selbst zurückgeben: `return self`.
      * Implementieren Sie `__exit__(self, exc_type, exc_value, traceback)`. (Die `exc`-Parameter brauchen wir nicht, aber sie müssen da sein). Diese Methode soll:
          * Die Endzeit berechnen: `end_time = time.perf_counter()`.
          * Die Dauer berechnen: `duration = end_time - self.start_time`.
          * Eine formatierte Nachricht ausgeben: `print(f"[{self.name}] Code-Block beendet in {duration:.6f} Sekunden")`.
4.  **In `main.py` anwenden:**
      * Importieren Sie den Timer: `from utils import CodeTimer`.
      * Umschließen Sie in Ihrer `main.py` einen Block von Transaktionen (z.B. 10 Einzahlungen in einer `for`-Schleife) mit Ihrem neuen Timer:
    <!-- end list -->
    ```python
    with CodeTimer(name="Batch-Einzahlung"):
        for _ in range(10):
            acc1.deposit(5.0)
    ```
      * Führen Sie `main.py` aus und beobachten Sie die Ausgabe des Timers in der Konsole.
