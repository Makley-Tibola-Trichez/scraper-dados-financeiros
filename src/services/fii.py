from logging import Logger

from ..models.fii import FiiModel
from ..utils.acessos import acessar_fii_investidor10
from ..utils.datetime import DatetimeUtils
from ..utils.investidor10_fii import Investidor10Fii
from ..utils.webdriver import WebDriver


class FiiService:
    def __init__(self, driver: WebDriver, logger: Logger) -> None:
        self.__driver = driver
        self._logger = logger

    def scrape(self, ticker: str) -> FiiModel:
        self._logger.info(f"Iniciando scrape do FII {ticker} no Investidor10")
        acessar_fii_investidor10(self.__driver, ticker)

        scrap = Investidor10Fii(self.__driver, logger=self._logger)

        cotacao = scrap.get_cotacao()
        pvp = scrap.get_pvp()
        segmento = scrap.get_segmento()
        tipo_de_fundo = scrap.get_tipo_de_fundo()
        quantidade_cotas_emitidas = scrap.get_quantidade_cotas_emitidas()
        valor_patrimonial_por_cota = scrap.get_valor_patrimonial_por_cota()

        dy_1_mes, dividendo_1_mes = scrap.get_dividend_yield_1_mes()
        dy_3_meses, dividendo_3_meses = scrap.get_dividend_yield_3_meses()
        dy_6_meses, dividendo_6_meses = scrap.get_dividend_yield_6_meses()
        dy_12_meses, dividendo_12_meses = scrap.get_dividend_yield_12_meses()

        self._logger.debug("Gerando modelo de FII com os dados obtidos")
        self._logger.info(f"Scrape do FII {ticker} concluído com sucesso")
        return FiiModel(
            id=None,
            cotacao=cotacao,
            ticker=ticker,
            pvp=pvp,
            segmento=segmento,
            tipo_de_fundo=tipo_de_fundo,
            quantidade_cotas_emitidas=quantidade_cotas_emitidas,
            valor_patrimonial_por_cota=valor_patrimonial_por_cota,
            dividendo_1_mes=dy_1_mes,
            dividendo_3_meses=dy_3_meses,
            dividendo_6_meses=dy_6_meses,
            dividendo_12_meses=dy_12_meses,
            dividend_yield_1_mes=dividendo_1_mes,
            dividend_yield_3_meses=dividendo_3_meses,
            dividend_yield_6_meses=dividendo_6_meses,
            dividend_yield_12_meses=dividendo_12_meses,
            date=DatetimeUtils.hoje(),
        )
