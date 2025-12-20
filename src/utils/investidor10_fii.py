from logging import Logger

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..errors import ElementoNaoEncontradoError
from .webdriver import WebDriver


class Investidor10Fii:
    def __init__(self, driver: WebDriver, logger: Logger) -> None:
        self.__informacoes_sobre_empresa: list[WebElement] | None = None
        self.__driver = driver
        self._logger = logger

    def get_cotacao(self) -> str:
        self._logger.info("Obtendo cotação do FII")
        return self.__driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.cotacao > div._card-body > div > span"
        ).text.strip()

    def get_dividend_yield_1_mes(self) -> tuple[str, str]:
        self._logger.info("Obtendo dividend yield 1 mês do FII")
        dividend_yield = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(1) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(1) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def get_dividend_yield_3_meses(self) -> tuple[str, str]:
        self._logger.info("Obtendo dividend yield 3 meses do FII")
        dividend_yield = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(2) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(2) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def get_dividend_yield_6_meses(self) -> tuple[str, str]:
        self._logger.info("Obtendo dividend yield 6 meses do FII")
        dividend_yield = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(3) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(3) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def get_dividend_yield_12_meses(self) -> tuple[str, str]:
        self._logger.info("Obtendo dividend yield 12 meses do FII")
        dividend_yield = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(4) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self.__driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(4) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def get_segmento(self) -> str:
        self._logger.info("Obtendo segmento do FII")
        return self.__get_valor_de_informacoes_da_empresa("segmento")

    def get_tipo_de_fundo(self) -> str:
        self._logger.info("Obtendo tipo de fundo do FII")
        return self.__get_valor_de_informacoes_da_empresa("TIPO DE FUNDO")

    def get_pvp(self) -> str:
        self._logger.info("Obtendo PVP do FII")
        return self.__driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.vp > div._card-body > span"
        ).text.strip()

    def get_quantidade_cotas_emitidas(self) -> str:
        self._logger.info("Obtendo quantidade de cotas emitidas do FII")
        return self.__get_valor_de_informacoes_da_empresa("COTAS EMITIDAS")

    def get_valor_patrimonial_por_cota(self) -> str:
        self._logger.info("Obtendo valor patrimonial por cota do FII")
        return self.__get_valor_de_informacoes_da_empresa("VAL. PATRIMONIAL P/ COTA")

    def __scrape_informacoes_sobre_empresa(self) -> list[WebElement]:
        if not self.__informacoes_sobre_empresa:
            self._logger.info("Buscando informações sobre a empresa do FII")
            self.__informacoes_sobre_empresa = self.__driver.find_elements(By.CSS_SELECTOR, "#table-indicators > div")

        return self.__informacoes_sobre_empresa

    def __get_valor_de_informacoes_da_empresa(self, tipo_informacao: str) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()

        for elemento in informacoes_sobre_empresa:
            if (
                str(elemento.find_element(By.CSS_SELECTOR, "div.desc > span").text).strip().lower()
                == tipo_informacao.lower()
            ):
                return elemento.find_element(By.CSS_SELECTOR, "div.desc > div > span").text.strip()

        raise ElementoNaoEncontradoError(seletor=tipo_informacao.upper())
