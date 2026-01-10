from dataclasses import dataclass


@dataclass
class AcaoModel:
    id: int | None
    ticker: str
    cotacao: str
    pl: str
    pvp: str
    dividend_yield: str
    payout: str
    date: str
    setor: str
    segmento: str
    vpa: str
    lpa: str
    roe: str
