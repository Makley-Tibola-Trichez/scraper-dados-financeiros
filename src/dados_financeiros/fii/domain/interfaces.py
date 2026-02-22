from abc import ABC, abstractmethod

from dados_financeiros.fii.domain.value_objects import Fii


class IFiiInvestidor10Gateway(ABC):
    @abstractmethod
    def fechar(self) -> None:
        pass

    @abstractmethod
    def obter_dados(self, ticker: str) -> Fii:
        pass


class IFiiRepository(ABC):
    @abstractmethod
    def inserir(self, fii: Fii) -> Fii:
        pass

    @abstractmethod
    def obter_tickers_existentes(self, tickers: list[str], date: str) -> list[tuple[str, Fii | None]]:
        pass
