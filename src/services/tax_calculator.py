from decimal import Decimal, ROUND_HALF_UP
from typing import List

from src.dto.operation_data import OperationDataDTO
from src.models.tax import Tax

class TaxCalculator:
    """Calculates taxes on realized profits considering loss carryovers and exemptions."""

    TAX_RATE: Decimal = Decimal("0.20")
    EXEMPT_LIMIT: Decimal = Decimal("20000.00")
    ZERO: Decimal = Decimal("0.00")
    ZERO_TAX: Tax = Tax(0.0)
    ROUND_MODE = ROUND_HALF_UP

    def __init__(self) -> None:
        self.accumulated_loss: Decimal = self.ZERO

    def _is_taxable(self, data: OperationDataDTO):
        if data.operation.type != "sell":
            return False
        if data.operation.total_value <= self.EXEMPT_LIMIT:
            return False
        if data.operation.unit_cost <= data.avg_price:
            return False
        return True

    def compute(self, operations: List[OperationDataDTO]) -> List[Tax]:
        """Computes and returns a list of tax due for a given list of operations."""

        taxes: List[Tax] = []
        for data in operations:
            if self._is_taxable(data):
                taxable_profit = data.profit - self.accumulated_loss

                if taxable_profit <= 0:
                    self.accumulated_loss = abs(taxable_profit)
                    taxes.append(self.ZERO_TAX)
                    continue

                tax_value = (taxable_profit * self.TAX_RATE).quantize(
                    Decimal("0.0"), rounding=self.ROUND_MODE
                )
                self.accumulated_loss = self.ZERO
                taxes.append(Tax(float(tax_value)))
            else:
                if data.profit is not None and data.profit < 0:
                    self.accumulated_loss += abs(data.profit)
                taxes.append(self.ZERO_TAX)

        return taxes



