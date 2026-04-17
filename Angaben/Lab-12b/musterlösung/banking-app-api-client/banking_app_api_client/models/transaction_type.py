from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

    def __str__(self) -> str:
        return str(self.value)
