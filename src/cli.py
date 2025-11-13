import sys
import json
from dataclasses import asdict
from src.models.portfolio import StockPortfolio
from src.services.tax_calculator import TaxCalculator
from src.utils.loader import load_operation_data


def read_input() -> str:
    """Reads operation data either interactively or from piped stdin."""
    if sys.stdin.isatty():
        # Interactive mode
        print(
            "Enter your stock operations as a JSON array, for example:\n"
            '[{"operation": "buy", "unit-cost": 10.00, "quantity": 10000}]\n'
        )
        return input("Operations: ").strip()
    else:
        # When data is piped or redirected
        return sys.stdin.read().strip()


def main() -> None:
    """Command-line interface for the tax calculator application.

    Reads JSON arrays of operations from stdin (one per line),
    computes applicable taxes, and prints the results as JSON arrays.
    """

    user_input = read_input()
    if not user_input:
        print("No input provided. Exiting.")
        return

    portfolio = StockPortfolio()
    tax_calculator = TaxCalculator()

    for line in user_input.splitlines():
        line = line.strip()
        if not line:
            continue

        operations_data_list = load_operation_data(portfolio, line)

        taxes = tax_calculator.compute(operations_data_list)

        output = [asdict(tax) for tax in taxes]

        print("Calculated Taxes: ",json.dumps(output))