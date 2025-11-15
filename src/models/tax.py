from dataclasses import dataclass

@dataclass(frozen=True)
class Tax:
    tax: float