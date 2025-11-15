import pytest
from decimal import Decimal

from src.models.portfolio import StockPortfolio
from tests.helpers import create_stock_operation


@pytest.fixture
def portfolio() -> StockPortfolio:
    return StockPortfolio()


def test_portfolio_initializes_with_zero_values(portfolio: StockPortfolio):
    assert portfolio.quantity == 0
    assert portfolio.avg_price == Decimal("0.00")
    assert portfolio.total_profit == Decimal("0.00")
    assert portfolio.total_loss == Decimal("0.00")


def test_buy_operation_updates_quantity(portfolio: StockPortfolio):
    operation = create_stock_operation("buy", 10.0, 100)
    portfolio.register_operation(operation)
    
    assert portfolio.quantity == 100


def test_buy_operation_sets_average_price(portfolio: StockPortfolio):
    operation = create_stock_operation("buy", 10.0, 100)
    portfolio.register_operation(operation)
    
    assert portfolio.avg_price == Decimal("10.00")


def test_multiple_buys_calculate_weighted_average(portfolio: StockPortfolio):
    operation1 = create_stock_operation("buy", 10.0, 100)
    operation2 = create_stock_operation("buy", 20.0, 100)
    
    portfolio.register_operation(operation1)
    portfolio.register_operation(operation2)
    
    assert portfolio.quantity == 200
    assert portfolio.avg_price == Decimal("15.00")


def test_sell_operation_decreases_quantity(portfolio: StockPortfolio):
    buy = create_stock_operation("buy", 10.0, 100)
    sell = create_stock_operation("sell", 15.0, 50)
    
    portfolio.register_operation(buy)
    portfolio.register_operation(sell)
    
    assert portfolio.quantity == 50


def test_sell_with_profit_updates_total_profit(portfolio: StockPortfolio):
    buy = create_stock_operation("buy", 10.0, 100)
    sell = create_stock_operation("sell", 15.0, 50)
    
    portfolio.register_operation(buy)
    profit = portfolio.register_operation(sell)
    
    assert profit == Decimal("250.0")
    assert portfolio.total_profit == Decimal("250.0")
    assert portfolio.total_loss == Decimal("0.00")


def test_sell_with_loss_updates_total_loss(portfolio: StockPortfolio):
    buy = create_stock_operation("buy", 20.0, 100)
    sell = create_stock_operation("sell", 15.0, 50)
    
    portfolio.register_operation(buy)
    profit = portfolio.register_operation(sell)
    
    assert profit == Decimal("-250.0")
    assert portfolio.total_loss == Decimal("250.0")
    assert portfolio.total_profit == Decimal("0.00")


def test_sequential_operations(portfolio: StockPortfolio):
    buy1 = create_stock_operation("buy", 10.0, 100)
    sell1 = create_stock_operation("sell", 15.0, 50)
    buy2 = create_stock_operation("buy", 20.0, 50)
    
    portfolio.register_operation(buy1)
    portfolio.register_operation(sell1)
    portfolio.register_operation(buy2)
    
    assert portfolio.quantity == 100
    assert portfolio.avg_price == Decimal("15.00")
