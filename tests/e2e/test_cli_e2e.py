import subprocess
import sys
from pathlib import Path
import pytest

DATA_DIR = Path(__file__).parent.parent / "data"

def load_input(name: str) -> str:
    return (DATA_DIR / name).read_text().strip()

def run_cli(input_text: str) -> str:
    """Runs the CLI subprocess and captures stdout."""
    result = subprocess.run(
        ["taxstock"],
        input=input_text.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.decode().strip()

TEST_CASES = [
    ("test-operation-1.json", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]'),
    ("test-operation-2.json", '[{"tax": 0.0},{"tax": 10000.0},{"tax": 0.0}]'),
    ("test-operation-3.json", '[{"tax": 0.0},{"tax": 0.0},{"tax": 1000.0}]'),
    ("test-operation-4.json", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]'),
    ("test-operation-5.json", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 10000.0}]'),
    ("test-operation-6.json", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 3000.0}]'),
]

@pytest.mark.parametrize("input_file,expected_output", TEST_CASES)
def test_cli_operations(input_file, expected_output):
    input_data = load_input(input_file)
    output = run_cli(input_data)

    assert output == expected_output

def test_cli_operations_multi_array():
    input_data = load_input("test-multi-array.txt")
    expected_output = '[{"tax": 0.0}]\n[{"tax": 0.0}]'
    output = run_cli(input_data)
    assert output == expected_output
