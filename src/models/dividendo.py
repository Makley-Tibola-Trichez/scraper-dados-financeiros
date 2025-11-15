from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class DividendoAnualModel:
    id: Optional[int]
    ticker: str
    ano: str
    valor: float
    date: str
    
    
@dataclass
class DividendoHistoricoModel:
    ticker: str
    valor: float
    data_anuncio: datetime
    data_pagamento: Optional[datetime]
    tipo: str
    data: Optional[str]