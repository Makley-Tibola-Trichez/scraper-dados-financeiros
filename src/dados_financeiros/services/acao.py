from logging import Logger

from ..models.acao import AcaoModel
from ..utils.acessos import acessar_acao_investidor10
from ..utils.datetime import DatetimeUtils
from ..utils.investidor10_acao import Investidor10Acao
from ..utils.webdriver import WebDriver


class AcaoService:
    def __init__(self, driver: WebDriver, logger: Logger) -> None:
        self.__driver = driver
        self._logger = logger

    def scrape(self, ticker: str) -> AcaoModel:
        self._logger.info(f"Iniciando scrape da ação: {ticker}")
        acessar_acao_investidor10(self.__driver, ticker)
        scrap = Investidor10Acao(self.__driver, logger=self._logger)

        cotacao = scrap.get_cotacao()
        pl = scrap.get_pl()
        pvp = scrap.get_pvp()
        vpa = scrap.get_vpa()
        lpa = scrap.get_lpa()
        roe = scrap.get_roe()
        dividend_yield = scrap.get_dividend_yield()
        payout = scrap.get_payout()
        setor = scrap.get_setor()
        segmento = scrap.get_segmento_do_setor()

        return AcaoModel(
            id=None,
            ticker=ticker,
            cotacao=cotacao,
            pl=pl,
            pvp=pvp,
            dividend_yield=dividend_yield,
            payout=payout,
            date=DatetimeUtils.hoje(),
            setor=setor,
            segmento=segmento,
            vpa=vpa,
            lpa=lpa,
            roe=roe,
        )
