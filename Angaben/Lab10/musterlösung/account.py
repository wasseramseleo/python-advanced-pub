# Typaliase mit dem 'type'-Keyword (Python 3.12, PEP 695)
type Amount = float
type AccountId = str


class BankAccount:
    """Stellt ein Bankkonto dar."""

    # Klassenattribute annotiert
    owner: str
    account_number: AccountId
    _balance: Amount

    def __init__(
        self,
        owner: str,
        account_number: AccountId,
        initial_balance: Amount = 0.0,
    ) -> None:
        self.owner = owner
        self.account_number = account_number
        self._balance = initial_balance

    def deposit(self, amount: Amount) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount: Amount) -> bool:
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> Amount:
        return self._balance

    def get_owner_name(self) -> str:
        return self.owner


# Typalias für eine Liste von Konten
type AccountList = list[BankAccount]


def find_account(accounts: AccountList, number: AccountId) -> BankAccount | None:
    """Sucht ein Konto anhand der Kontonummer. Gibt None zurück, wenn nicht gefunden."""
    for acc in accounts:
        if acc.account_number == number:
            return acc
    return None
