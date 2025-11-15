## 💰 taxstock 🏛️

A simple CLI application to calculate tax from capital gains of stock market operations.

Developed in Python, following the tax calculation rules of the technical challenge proposed by Nubank.

### Features

- Small, dependency-light implementation
- Read lines of JSON arrays representing stock operations from stdin (one JSON array per line).
- For each array of operations, calculates applicable taxes following predefined taxation rules
- Prints a JSON array with all tax results.


### Requirements

- Python 3.10 or newer

The project uses a simple setuptools entry point (see [pyproject.toml](pyproject.toml)) that installs a `taxstock` console script.

### Install

Option 1 — editable install (recommended for development):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Option 2 — install from local source:

```bash
python -m pip install .
```

After installation you should have a `taxstock` command available in your PATH while the virtualenv is active.

### Running the CLI

The CLI reads JSON arrays from stdin (one array per line) and prints a JSON array of tax results for each input line.

Examples:

1. input with pipe operation:

```bash
echo '[{"operation":"buy","unit-cost":10.0,"quantity":100},{"operation":"sell","unit-cost":15.0,"quantity":50}]' | taxstock
```

2. interactive input:
   Run the command: `taxstock`

```txt
Enter your stock operations as a JSON array, for example:
[{"operation": "buy", "unit-cost": 10.00, "quantity": 10000}]

Operations: <type or paste your JSON array here>
````

The result is an output of one or more JSON arrays with calculated tax results (one object per operation):

```bash
[{"tax": 0.0},{"tax": 0.0},{"tax": 1000.0}]
```

## Testing

This project includes an end-to-end test that runs the CLI with [subprocess](https://docs.python.org/3.13/library/subprocess.html). \
All tests scenarios were derived from each case of the technical challenge documentation.

Tests were created with [pytest](https://docs.pytest.org/en/stable/).

To run tests locally:

```bash
# from project root after activating your virtualenv
pip install -r requirements.txt
pytest
```

### Development notes

- Entry point: `src.cli:main` (configured in `pyproject.toml`).
- The CLI expects valid JSON arrays of operations. Each operation should include at least the fields: `operation` ("buy"
  or "sell"), `unit-cost` (number) and `quantity` (integer).
- Multiple arrays can be passed by separating them into separate lines on stdin.
