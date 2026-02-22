from abc import ABC, abstractmethod
from datetime import datetime

from dados_financeiros.acao.domain.value_objects import Acao, Dividendo


class IAcaoInvestidor10Gateway(ABC):
    @abstractmethod
    def fechar(self) -> None:
        pass

    @abstractmethod
    def obter_dados(self, ticker: str) -> Acao:
        pass

    @abstractmethod
    def obter_dividendos(self, ticker: str) -> list[Dividendo]:
        pass


class IAcaoRepository(ABC):
    @abstractmethod
    def inserir(self, acao: Acao) -> Acao:
        pass

    @abstractmethod
    def obter_tickers_existentes(self, tickers: list[str], date: datetime) -> list[tuple[str, Acao | None]]:
        pass
