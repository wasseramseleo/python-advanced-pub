# Lab 0: Überprüfung der IDE & Python-Umgebung

## Ziel

Dieses Lab stellt sicher, dass Ihre lokale Entwicklungsumgebung (Windows) korrekt für den Kurs konfiguriert ist. Wir prüfen die Python-Version, `pip` und das `uv`-Tool.

**Bitte führen Sie alle Schritte sorgfältig aus und bitten Sie den Trainer um Hilfe, falls ein Befehl fehlschlägt.**

-----

## 1\. Konsole öffnen

Öffnen Sie eine neue Konsole. Sie können entweder die **Eingabeaufforderung** (`cmd.exe`) oder **PowerShell** verwenden. Alle folgenden Befehle werden dort ausgeführt.

-----

## 2\. Python-Version prüfen

1.  Geben Sie den folgenden Befehl ein, um Ihre Standard-Python-Version zu prüfen:

    ```bash
    python --version
    ```

2.  Falls dies fehlschlägt oder eine Version unter 3.11 anzeigt, versuchen Sie den Python-Launcher für Windows:

    ```bash
    py --version
    ```

**Erwartetes Ergebnis:** Sie sollten eine Version sehen, die `Python 3.11` oder höher ist (z.B. `Python 3.11.5` oder `Python 3.12.1`).

-----

## 3\. `pip` (Global) prüfen

Als nächstes prüfen wir, ob der Python-Paketmanager `pip` global verfügbar ist.

1.  Führen Sie aus:

    ```bash
    pip --version
    ```

**Erwartetes Ergebnis:** Sie sollten einen Pfad und die Version von `pip` sehen (z.B. `pip 24.0 from ...`).

-----

## 4\. `uv` (Global) prüfen

`uv` ist ein extrem schneller, moderner Python-Paketmanager, den wir in diesem Kurs verwenden werden.

1.  Führen Sie aus:

    ```bash
    uv --version
    ```

**Erwartetes Ergebnis:** Sie sollten eine Versionsnummer sehen (z.B. `uv 0.1.30`).

  * **Falls `uv` nicht gefunden wird:**
    Installieren Sie es bitte global über `pip`:
    ```bash
    pip install uv
    ```
    Oder über PowerShell (empfohlen vom `uv`-Team):
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    Schließen Sie nach der Installation Ihre Konsole und öffnen Sie eine neue, bevor Sie `uv --version` erneut versuchen.

-----

## 5\. Test: `uv` Projekt-Setup

Wir simulieren nun das Erstellen eines Projekt-Environments mit `uv`.

1.  Erstellen Sie einen neuen Ordner und wechseln Sie hinein:

    ```bash
    mkdir lab0_uv_test
    cd lab0_uv_test
    ```

2.  Erstellen Sie ein virtuelles Environment mit `uv` und zielen Sie auf Python 3.11:

    ```bash
    uv venv --python 3.11
    ```

    *(Falls dies fehlschlägt, weil Python 3.11 nicht im Pfad ist, fragt `uv` Sie möglicherweise nach dem exakten Pfad zur `python.exe`.)*

3.  Aktivieren Sie das Environment. Ein `.venv`-Ordner sollte erstellt worden sein:

    ```bash
    .venv\Scripts\activate
    ```

    Ihr Konsolen-Prompt sollte sich nun ändern und `(.venv)` anzeigen.

4.  Installieren Sie ein Paket mit `uv pip`:

    ```bash
    uv pip install requests
    ```

5.  Deaktivieren Sie das Environment wieder:

    ```bash
    deactivate
    ```

-----

## 6\. Test: Standard `venv` und `pip`

Zuletzt testen wir den klassischen Weg mit `venv` und `pip`, um sicherzustellen, dass auch dieser funktioniert.

1.  Wechseln Sie aus dem `lab0_uv_test`-Ordner zurück (oder öffnen Sie eine neue Konsole):

    ```bash
    cd ..
    ```

2.  Erstellen Sie einen zweiten Test-Ordner:

    ```bash
    mkdir lab0_pip_test
    cd lab0_pip_test
    ```

3.  Erstellen Sie ein virtuelles Environment mit dem `venv`-Modul:

    ```bash
    py -m venv venv
    ```

    *(Oder `python -m venv venv`)*

4.  Aktivieren Sie das Environment:

    ```bash
    venv\Scripts\activate
    ```

    Ihr Prompt sollte sich (erneut) ändern und `(venv)` anzeigen.

5.  Installieren Sie ein Paket mit dem Standard-`pip` (das jetzt das `pip` aus dem `venv` ist):

    ```bash
    pip install numpy
    ```

6.  Erstellen Sie eine Test-Datei.

      * Öffnen Sie einen einfachen Texteditor (wie Notepad) oder Ihre IDE (VS Code).
      * Erstellen Sie eine Datei namens `main.py` in Ihrem `lab0_pip_test`-Ordner.
      * Fügen Sie folgenden Inhalt ein und speichern Sie die Datei:

    <!-- end list -->

    ```python
    # main.py
    import numpy as np
    import sys

    def run_check():
        print("--- Python Check ---")
        print(f"Python Version: {sys.version.split()[0]}")
        
        try:
            arr = np.array([1, 2, 3])
            print(f"Numpy Version:  {np.__version__}")
            print(f"Numpy Test OK:  {arr.sum() == 6}")
        except ImportError:
            print("Numpy Import FEHLGESCHLAGEN")

    if __name__ == "__main__":
        run_check()
    ```

7.  Führen Sie das Skript in Ihrer (noch aktiven) Konsole aus:

    ```bash
    python main.py
    ```

**Erwartetes Ergebnis:**

```
--- Python Check ---
Python Version: 3.11.x (oder ähnlich)
Numpy Version:  1.26.x (oder ähnlich)
Numpy Test OK:  True
```

8.  Deaktivieren Sie das Environment:

    ```bash
    deactivate
    ```

-----

## Abschluss

Wenn alle Befehle erfolgreich ausgeführt wurden, ist Ihre Umgebung für den Kurs bereit. Wenn Sie bei einem Schritt auf Probleme gestoßen sind, melden Sie sich bitte jetzt beim Trainer.