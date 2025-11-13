class InvalidOperationTypeError(Exception):
    """Raised when a stock operation type is not recognized as valid."""
    def __init__(self, operation_type: str) -> None:
        super().__init__(f"Invalid operation type: '{operation_type}'. Expected 'buy' or 'sell'.")
        self.operation_type = operation_type
