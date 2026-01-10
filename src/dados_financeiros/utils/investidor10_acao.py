from logging import Logger

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..errors import ElementoNaoEncontradoError
from .webdriver import WebDriver


class Investidor10Acao:
    def __init__(self, driver: WebDriver, logger: Logger) -> None:
        self.__informacoes_sobre_empresa: list[WebElement] | None = None
        self.__indicadores: list[WebElement] | None = None
        self.__driver = driver
        self._logger = logger

    def get_cotacao(self) -> str:
        self._logger.info("Obtendo cotação da ação")
        return self.__driver.find_element(
            By.CSS_SELECTOR,
            "#cards-ticker > div._card.cotacao > div._card-body > div > span",
        ).text.strip()

    def get_pl(self) -> str:
        self._logger.info("Obtendo P/L da ação")
        return self.__driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.val > div._card-body > span"
        ).text.strip()

    def get_pvp(self) -> str:
        self._logger.info("Obtendo P/VP da ação")
        return self.__driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.vp > div._card-body > span"
        ).text.strip()

    def get_vpa(self) -> str:
        self._logger.info("Obtendo VPA da ação")
        indicatores = self.__scrape_indicadores()
        for indicador in indicatores:
            if str(indicador.find_element(By.CSS_SELECTOR, "& > span").text).strip().lower() == "vpa":
                return indicador.find_element(By.CSS_SELECTOR, "div.value > span").text.strip()

        raise ElementoNaoEncontradoError(seletor="VPA")

    def get_lpa(self) -> str:
        self._logger.info("Obtendo LPA da ação")
        indicatores = self.__scrape_indicadores()
        for indicador in indicatores:
            if str(indicador.find_element(By.CSS_SELECTOR, "& > span").text).strip().lower() == "lpa":
                return indicador.find_element(By.CSS_SELECTOR, "div.value > span").text.strip()

        raise ElementoNaoEncontradoError(seletor="LPA")

    def get_roe(self) -> str:
        self._logger.info("Obtendo ROE da ação")
        indicatores = self.__scrape_indicadores()
        for indicador in indicatores:
            if str(indicador.find_element(By.CSS_SELECTOR, "& > span").text).strip().lower() == "roe":
                return indicador.find_element(By.CSS_SELECTOR, "div.value > span").text.strip()

        raise ElementoNaoEncontradoError(seletor="ROE")

    def get_dividend_yield(self) -> str:
        self._logger.info("Obtendo Dividend Yield da ação")
        return self.__driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.dy > div._card-body > span"
        ).text.strip()

    def get_payout(self) -> str:
        self._logger.info("Obtendo Payout da ação")
        indicatores = self.__scrape_indicadores()
        for indicador in indicatores:
            if str(indicador.find_element(By.CSS_SELECTOR, "& > span").text).strip().lower() == "payout":
                return indicador.find_element(By.CSS_SELECTOR, "div.value > span").text.strip()

        raise ElementoNaoEncontradoError(seletor="PAYOUT")

    def __scrape_indicadores(self) -> list[WebElement]:
        if not self.__indicadores:
            self._logger.info("Raspando indicadores financeiros da ação")
            self.__indicadores = self.__driver.find_elements(By.CSS_SELECTOR, "#table-indicators > div")
        return self.__indicadores

    def __scrape_informacoes_sobre_empresa(self) -> list[WebElement]:
        if not self.__informacoes_sobre_empresa:
            self._logger.info("Buscando informações sobre a empresa da ação")
            self.__informacoes_sobre_empresa = self.__driver.find_elements(
                By.CSS_SELECTOR, "#table-indicators-company > div"
            )
        return self.__informacoes_sobre_empresa

    def get_setor(self) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()
        informacoes_sobre_empresa.reverse()

        self._logger.info("Obtendo setor da ação")
        for elemento in informacoes_sobre_empresa:
            if str(elemento.find_element(By.CSS_SELECTOR, "span.title").text).strip().lower() == "setor":
                return elemento.find_element(By.CSS_SELECTOR, "span.value").text.strip()

        raise ElementoNaoEncontradoError(seletor="SETOR")

    def get_segmento_do_setor(self) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()
        informacoes_sobre_empresa.reverse()

        self._logger.info("Obtendo segmento do setor da ação")
        for elemento in informacoes_sobre_empresa:
            if str(elemento.find_element(By.CSS_SELECTOR, "span.title").text).strip().lower() == "segmento":
                return elemento.find_element(By.CSS_SELECTOR, "span.value").text.strip()

        raise ElementoNaoEncontradoError(seletor="SEGMENTO DO SETOR")
