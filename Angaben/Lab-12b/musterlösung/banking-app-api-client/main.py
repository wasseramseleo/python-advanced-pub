from banking_app_api_client import Client
from banking_app_api_client.api.default import get_api_account_account_id, post_api_account_account_id_transact
from banking_app_api_client.models import Transaction, Account, TransactionResponse
from banking_app_api_client.types import Response

# 1. Client Setup
client = Client(base_url="http://127.0.0.1:5000")


def get_account_safe(account_id: str):
  print(f"SDK ANFRAGE: Details für {account_id}")
  # Der Client übernimmt URL-Bau und JSON-Parsing
  account: Account = get_api_account_account_id.sync(client=client, account_id=account_id)

  if account:
    print(f"  ERFOLG: Besitzer ist {account.owner}, Saldo: {account.balance}")
    return account
  else:
    print(f"  FEHLER: Konto {account_id} nicht gefunden.")
    return None


def perform_transaction_safe(account_id: str, tx_type: str, amount: float):
  # Erstellung des validierten Payloads
  # IDE-Support: Transaction(type=..., amount=...)
  payload = Transaction(type_=tx_type, amount=amount)

  print(f"SDK ANFRAGE: {tx_type} von {amount} auf {account_id}")

  # sync_detailed gibt uns Zugriff auf Status Codes und Rohdaten
  response: Response[TransactionResponse] = post_api_account_account_id_transact.sync_detailed(
    client=client,
    account_id=account_id,
    body=payload
  )

  if response.status_code == 200:
    print(f"  ERFOLG: Neuer Saldo ist {response.parsed.new_balance}")
    return response.parsed
  else:
    print(f"  FEHLER: Status {response.status_code} - Transaktion abgelehnt.")
    return None


# --- Test ---
print("--- OpenAPI Client Test ---")
acc = get_account_safe("AT123")

print("\n--- Bonus Test ---")
perform_transaction_safe("DE456", "DEPOSIT", 100.0)
# Testet die SDK-Validierung (Ungültiger Typ würde hier bereits scheitern)
perform_transaction_safe("DE456", "WITHDRAW", 50.0)