import json
import subprocess
from pathlib import Path
import pytest

DATA_DIR = Path(__file__).parent.parent / "data"

def load_input_from_file(name: str) -> str:
    with open(DATA_DIR/"input"/name , "r") as f:
        data = json.load(f)
        return json.dumps(data, separators=(",", ": "))

def load_output_from_file(name: str) -> str:
    path = (DATA_DIR/"output"/ name)
    return read_text_file(path)

def read_text_file(filepath: Path) -> str:
    return filepath.read_text().strip()

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
    ("operation-1.json", 'tax-1.txt'),
    ("operation-2.json", 'tax-2.txt'),
    ("operation-3.json", 'tax-3.txt'),
    ("operation-4.json", 'tax-4.txt'),
    ("operation-5.json", 'tax-5.txt'),
    ("operation-6.json", 'tax-6.txt'),
    ("operation-7.json", 'tax-7.txt'),
    ("operation-8.json", 'tax-8.txt'),
    ("operation-9.json", 'tax-9.txt')
]

@pytest.mark.parametrize("input_file, output_file", TEST_CASES)
def test_cli_operations(input_file, output_file):
    input_data = load_input_from_file(input_file)
    cli_output = run_cli(input_data)
    expected_output = load_output_from_file(output_file)

    assert cli_output == expected_output

def test_cli_operations_multi_array():
    path = DATA_DIR/"input"/"multi-array.txt"
    input_data = read_text_file(path)
    expected_output = '[{"tax": 0.0}]\n[{"tax": 0.0}]'
    cli_output = run_cli(input_data)
    assert cli_output == expected_output
