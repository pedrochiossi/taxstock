from decimal import Decimal
from typing import Literal

from src.models.stock_operation import StockOperation
from src.dto.operation_data import OperationDataDTO


def create_stock_operation(
    operation_type: Literal["buy", "sell"],
    unit_cost: float,
    quantity: int
) -> StockOperation:
    return StockOperation(
        type=operation_type,
        unit_cost=Decimal(str(unit_cost)),
        quantity=quantity
    )


def create_operation_data(
    operation_type: Literal["buy", "sell"],
    unit_cost: float,
    quantity: int,
    profit: float,
    avg_price: float
) -> OperationDataDTO:
    operation = create_stock_operation(operation_type, unit_cost, quantity)
    return OperationDataDTO(
        operation=operation,
        profit=Decimal(str(profit)),
        avg_price=Decimal(str(avg_price))
    )
