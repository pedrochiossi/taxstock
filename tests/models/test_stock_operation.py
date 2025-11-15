from decimal import Decimal
from src.exceptions.invalid_operation import InvalidOperationTypeError

import pytest
from tests.helpers import create_stock_operation

def test_stock_operation_creation():
    operation = create_stock_operation("buy", 15.5, 200)
    assert operation.type == "buy"
    assert operation.unit_cost == Decimal("15.50")
    assert operation.quantity == 200

def test_stock_operation_has_unique_id():
    operation1 = create_stock_operation("buy", 10.0, 100)
    operation2 = create_stock_operation("sell", 20.0, 50)
    assert operation1.id != operation2.id

def test_stock_operation_throws_error_invalid_operation():
    error_message = "Invalid operation type: 'test-error'. Expected 'buy' or 'sell'."
    with pytest.raises(Exception) as error:
        create_stock_operation("test-error", 10.0, 100)
    assert str(error.value) == error_message
    assert error.type is InvalidOperationTypeError

def test_stock_operation_sets_total_value():
    operation = create_stock_operation("buy", 12.5, 40)
    assert operation.total_value == Decimal("500.00")