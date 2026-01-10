from dataclasses import dataclass
from datetime import datetime


@dataclass
class DividendoAnualModel:
    id: int | None
    ticker: str
    ano: str
    valor: float
    date: str


@dataclass
class DividendoHistoricoModel:
    ticker: str
    valor: float
    data_anuncio: datetime
    data_pagamento: datetime | None
    tipo: str
    data: str | None
