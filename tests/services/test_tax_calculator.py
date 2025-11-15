import pytest
from decimal import Decimal

from src.services.tax_calculator import TaxCalculator
from src.models.tax import Tax
from tests.helpers import create_operation_data


@pytest.fixture
def calculator() -> TaxCalculator:
    return TaxCalculator()


def test_buy_operations_have_no_tax(calculator: TaxCalculator):
    operations = [
        create_operation_data("buy", 10.0, 100, 0.0, 10.0),
        create_operation_data("buy", 15.0, 200, 0.0, 12.5),
    ]
    result = calculator.compute(operations)
    
    assert all(tax == Tax(0.0) for tax in result)


def test_sell_below_exempt_limit_has_no_tax(calculator: TaxCalculator):
    operations = [create_operation_data("sell", 15.0, 1000, 5000.0, 10.0)]
    result = calculator.compute(operations)
    
    assert result[0] == Tax(0.0)


def test_sell_above_exempt_limit_with_profit_calculates_tax(calculator: TaxCalculator):
    operations = [create_operation_data("sell", 25.0, 1000, 5000.0, 20.0)]
    result = calculator.compute(operations)
    
    assert result[0] == Tax(1000.0)


def test_loss_is_accumulated(calculator: TaxCalculator):
    operations = [create_operation_data("sell", 5.0, 1000, -5000.0, 10.0)]
    calculator.compute(operations)
    
    assert calculator.accumulated_loss == Decimal("5000.0")


def test_accumulated_loss_offsets_future_profit(calculator: TaxCalculator):
    operations = [
        create_operation_data("sell", 5.0, 1000, -5000.0, 10.0),
        create_operation_data("sell", 25.0, 1000, 5000.0, 20.0)
    ]
    result = calculator.compute(operations)
    
    assert result[0] == Tax(0.0)
    assert result[1] == Tax(0.0)
    assert calculator.accumulated_loss == Decimal("0.0")


def test_partial_loss_offset(calculator: TaxCalculator):
    operations = [
        create_operation_data("sell", 5.0, 1000, -3000.0, 10.0),
        create_operation_data("sell", 25.0, 1000, 5000.0, 20.0)
    ]
    result = calculator.compute(operations)
    
    assert result[1] == Tax(400.0)


def test_mixed_operations(calculator: TaxCalculator):
    operations = [
        create_operation_data("buy", 10.0, 100, 0.0, 10.0),
        create_operation_data("sell", 25.0, 1000, 5000.0, 20.0),
        create_operation_data("buy", 15.0, 200, 0.0, 12.5)
    ]
    result = calculator.compute(operations)
    
    assert result[0] == Tax(0.0)
    assert result[1] == Tax(1000.0)
    assert result[2] == Tax(0.0)


def test_loss_carryover_across_multiple_profits(calculator: TaxCalculator):
    operations = [
        create_operation_data("sell", 5.0, 2000, -10000.0, 10.0),
        create_operation_data("sell", 25.0, 1000, 4000.0, 20.0),
        create_operation_data("sell", 30.0, 1000, 5000.0, 25.0)
    ]
    result = calculator.compute(operations)
    
    assert result[0] == Tax(0.0)
    assert result[1] == Tax(0.0)
    assert result[2] == Tax(0.0)
    assert calculator.accumulated_loss == Decimal("1000.0")
