from dataclasses import dataclass
from typing import Optional

@dataclass
class DividendoModel:
    id: Optional[int]
    ticker: str
    ano: str
    valor: float
    date: str
    