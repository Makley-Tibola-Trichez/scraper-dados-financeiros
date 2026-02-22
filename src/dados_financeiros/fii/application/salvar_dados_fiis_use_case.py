from logging import Logger

from dados_financeiros.fii.domain.interfaces import IFiiInvestidor10Gateway, IFiiRepository
from dados_financeiros.fii.domain.value_objects import Fii
from dados_financeiros.utils.datetime import DatetimeUtils


class SalvarFiiUseCase:
    def __init__(self, logger: Logger, gateway: IFiiInvestidor10Gateway, repository: IFiiRepository) -> None:
        self._logger = logger
        self._gateway = gateway
        self._repository = repository

    def executar(self, tickers: list[str]) -> list[Fii]:
        fiis: list[Fii] = []
        fiis_existentes = self._repository.obter_tickers_existentes(tickers, DatetimeUtils.hoje())

        for ticker, fii in fiis_existentes:
            if fii is not None:
                self._logger.info(f"{ticker} já existe")
                fiis.append(fii)
            else:
                try:
                    fii = self._gateway.obter_dados(ticker)

                    if fii is None:
                        self._logger.warning(f"FII {ticker} não encontrado")
                        continue

                    self._repository.inserir(fii)
                    fiis.append(fii)
                    self._logger.info(f"FII {ticker} inserido no banco de dados.")
                except Exception as e:
                    self._logger.error(f"Erro ao fazer scrape do FII {ticker}: {e}", exc_info=e)
                    exit()

        return fiis
