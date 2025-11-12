from dataclasses import dataclass
from decimal import Decimal
from src.models.stock_operation import StockOperation


@dataclass(frozen=True)
class OperationDataDTO:
    operation: StockOperation
    profit: Decimal
    avg_price: Decimal
