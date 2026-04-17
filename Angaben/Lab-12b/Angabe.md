# Lab 12b: Automatisierung mit OpenAPI Clients

## Lernziele
In diesem Lab lernen Sie, wie Sie manuelle `requests`-Aufrufe durch einen automatisch generierten, typsicheren Client ersetzen.

* Generierung eines Python-Clients aus einer `openapi.json`.
* Verwendung von Pydantic-Modellen für die Datenvalidierung.
* Vergleich der Fehlerbehandlung zwischen manuellem Code und SDK.

## Vorbereitung
1. Stellen Sie sicher, dass das Banking-Backend (`backend.py`) läuft.
2. Generieren Sie den Client basierend auf der bereitgestellten `openapi.json`:
   `uvx openapi-python-client generate --path openapi.json --meta pdm`
3. Installieren Sie den generierten Client lokal (im neu entstandenen Ordner):
   `uv pip install ./banking-app-api-client`

### Angabe
Ersetzen Sie Ihre manuelle `get_account_details`-Logik durch den generierten Client.

1.  **Client-Initialisierung:** Importieren Sie den `Client` und erstellen Sie eine Instanz für `http://127.0.0.1:5000`.
2.  **Abruf:** Nutzen Sie die Funktion `get_account_details.sync(...)` des generierten Pakets.
3.  **Typsicherheit:** Geben Sie nicht mehr ein `dict` zurück, sondern das vom Client bereitgestellte Datenmodell (`Account`).

### Bonus-Herausforderung
Führen Sie eine Transaktion mit dem generierten SDK durch.

1.  Nutzen Sie das Modell `Transaction`, um den Payload zu erstellen. Beobachten Sie, wie Ihre IDE Sie bei den Parametern (`type`, `amount`) unterstützt.
2.  Führen Sie den Post-Request über `transact.sync_detailed(...)` aus.
3.  **Fehlerprüfung:** Prüfen Sie den `status_code` des Response-Objekts des Clients.

**Testen:**
Wiederholen Sie die Tests aus Lab 12 (DE456 Einzahlung/Abhebung) und vergleichen Sie, wie viel weniger Code Sie für die Validierung schreiben mussten.