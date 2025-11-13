from decimal import Decimal
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Literal
from src.exceptions.invalid_operation import InvalidOperationTypeError


@dataclass(frozen=True)
class StockOperation:
    type: Literal["buy", "sell"]
    unit_cost: Decimal
    quantity: int
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if self.type not in ("buy", "sell"):
            raise InvalidOperationTypeError(self.type)

    @property
    def total_value(self) -> Decimal:
        return self.unit_cost * self.quantity
