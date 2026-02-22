from logging import Logger

from dados_financeiros.acao.domain.interfaces import IAcaoInvestidor10Gateway, IAcaoRepository
from dados_financeiros.acao.domain.value_objects import Acao
from dados_financeiros.utils.datetime import DatetimeUtils


class SalvarAcaoUseCase:
    def __init__(self, logger: Logger, gateway: IAcaoInvestidor10Gateway, repository: IAcaoRepository) -> None:
        self._logger = logger
        self._gateway = gateway
        self._repository = repository

    def executar(self, tickers: list[str]) -> list[Acao]:
        acoes: list[Acao] = []
        acoes_existentes = self._repository.obter_tickers_existentes(tickers, DatetimeUtils.hoje_datetime())

        for ticker, acao in acoes_existentes:
            if acao is not None:
                self._logger.info(f"{ticker} já existe")

                acao.dividendos = self._gateway.obter_dados(ticker).dividendos
                acoes.append(acao)
            else:
                try:
                    acao = self._gateway.obter_dados(ticker)

                    if acao is None:
                        self._logger.warning(f"Ação {ticker} não encontrado")
                        continue

                    self._repository.inserir(acao)
                    acoes.append(acao)
                    self._logger.info(f"Ação {ticker} inserida no banco de dados.")

                except Exception as e:
                    self._logger.error(f"Erro ao fazer scrape da ação {ticker}: {e}", exc_info=e)
                    exit()

        return acoes
