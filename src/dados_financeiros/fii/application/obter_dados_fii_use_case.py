from logging import Logger

from dados_financeiros.fii.domain.interfaces import IFiiInvestidor10Gateway
from dados_financeiros.fii.domain.value_objects import Fii


class ObterDadosFiiUseCase:
    def __init__(self, logger: Logger, gateway: IFiiInvestidor10Gateway) -> None:
        self._logger = logger
        self._gateway = gateway

    def executar(self, ticker: str) -> Fii:
        url = self._gateway.acessar(ticker)

        self._logger.info(f"Acessa {url}")

        return self._gateway.obter_dados(ticker)
