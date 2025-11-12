from dataclasses import dataclass
from typing import Optional

@dataclass
class AcaoModel: 
    id: Optional[int]
    ticker: str
    cotacao: str
    pl: str
    pvp: str
    dividend_yield: str
    payout: str
    date: str
    setor: str
    segmento: str
