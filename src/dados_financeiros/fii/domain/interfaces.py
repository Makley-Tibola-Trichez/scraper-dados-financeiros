from abc import ABC, abstractmethod

from dados_financeiros.fii.domain.value_objects import Fii


class IFiiInvestidor10Gateway(ABC):
    @abstractmethod
    def acessar(self, ticker: str) -> None:
        pass

    @abstractmethod
    def fechar(self) -> None:
        pass

    @abstractmethod
    def obter_dados(self, ticker: str) -> Fii:
        pass
