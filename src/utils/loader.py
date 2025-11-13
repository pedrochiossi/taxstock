import json
from decimal import Decimal
from typing import List
from src.models.stock_operation import StockOperation
from src.models.portfolio import StockPortfolio
from src.dto.operation_data import OperationDataDTO


def load_operation_data(portfolio: StockPortfolio, line: str) -> List[OperationDataDTO]:

    operations = json.loads(line)
    data_list: List[OperationDataDTO] = []

    for item in operations:
        operation = StockOperation(
            type=item["operation"],
            quantity=int(item["quantity"]),
            unit_cost=Decimal(str(item["unit-cost"]))
        )
        profit = portfolio.register_operation(operation)
        dto = OperationDataDTO(
            operation=operation,
            profit=portfolio.total_profit,
            avg_price=portfolio.avg_price
        )
        data_list.append(dto)
    return data_list