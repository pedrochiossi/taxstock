from decimal import Decimal, ROUND_HALF_UP
from src.models.stock_operation import StockOperation
from uuid import uuid4


class StockPortfolio:
    """Tracks stock portfolio state, including stock quantity, average price, and cumulative profit/loss."""
    ROUND_MODE = ROUND_HALF_UP
    ZERO = Decimal("0.00")

    def __init__(self) -> None:
        self.id: str = str(uuid4())
        self.quantity: int = 0
        self.avg_price: Decimal = self.ZERO
        self.total_profit: Decimal = self.ZERO
        self.total_loss: Decimal = self.ZERO

    def register_operation(self, op: StockOperation) -> None | Decimal:
        if op.type == "buy":
            return self._register_buy(op)
        return self._register_sell(op)

    def _register_buy(self, op: StockOperation) -> None:
        total_cost = self.avg_price * self.quantity + op.unit_cost * op.quantity
        self.quantity += op.quantity
        if self.quantity > 0:
            self.avg_price = (total_cost / self.quantity).quantize(Decimal("0.01"), rounding=self.ROUND_MODE)

    def _register_sell(self, op: StockOperation) -> Decimal:
        profit = (op.unit_cost - self.avg_price) * op.quantity
        self.quantity -= op.quantity
        if profit >= 0:
            self.total_profit += profit
        else:
            self.total_loss += abs(profit)
        return profit
