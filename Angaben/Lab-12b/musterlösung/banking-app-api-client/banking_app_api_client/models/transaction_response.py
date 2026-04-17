from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransactionResponse")


@_attrs_define
class TransactionResponse:
    """
    Attributes:
        message (str | Unset):
        account_id (str | Unset):
        new_balance (float | Unset):
    """

    message: str | Unset = UNSET
    account_id: str | Unset = UNSET
    new_balance: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        account_id = self.account_id

        new_balance = self.new_balance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if new_balance is not UNSET:
            field_dict["new_balance"] = new_balance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message", UNSET)

        account_id = d.pop("account_id", UNSET)

        new_balance = d.pop("new_balance", UNSET)

        transaction_response = cls(
            message=message,
            account_id=account_id,
            new_balance=new_balance,
        )

        transaction_response.additional_properties = d
        return transaction_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
