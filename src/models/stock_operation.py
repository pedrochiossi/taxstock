from decimal import Decimal
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Literal


@dataclass(frozen=True)
class StockOperation:
    type: Literal["buy", "sell"]
    unit_cost: Decimal
    quantity: int
    id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def total_value(self) -> Decimal:
        return self.unit_cost * self.quantity
