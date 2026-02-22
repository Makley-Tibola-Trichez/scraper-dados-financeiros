from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from dados_financeiros.errors import ElementoNaoEncontradoError
from dados_financeiros.fii.domain.value_objects import Fii
from dados_financeiros.utils.webdriver import WebDriver

from ..domain.interfaces import IFiiInvestidor10Gateway


class FiiInvestidor10Gateway(IFiiInvestidor10Gateway):
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def acessar(self, ticker: str) -> None:
        self._driver.get(f"https://investidor10.com.br/fiis/{ticker}")

    def fechar(self) -> None:
        self._driver.close()

    def obter_dados(self, ticker: str) -> Fii:
        cotacao = self.obter_cotacao()
        pvp = self.obter_pvp()
        segmento = self.obter_segmento()
        tipo_de_fundo = self.obter_tipo_de_fundo()
        quantidade_cotas_emitidas = self.obter_quantidade_cotas_emitidas()
        valor_patrimonial_por_cota = self.obter_valor_patrimonial_por_cota()

        dy_1_mes, dividendo_1_mes = self.obter_dividend_yield_1_mes()
        dy_3_meses, dividendo_3_meses = self.obter_dividend_yield_3_meses()
        dy_6_meses, dividendo_6_meses = self.obter_dividend_yield_6_meses()
        dy_12_meses, dividendo_12_meses = self.obter_dividend_yield_12_meses()

        return Fii(
            cotacao=cotacao,
            ticker=ticker,
            pvp=pvp,
            segmento=segmento,
            tipo_de_fundo=tipo_de_fundo,
            quantidade_cotas_emitidas=quantidade_cotas_emitidas,
            valor_patrimonial_por_cota=valor_patrimonial_por_cota,
            div_1_mes=dy_1_mes,
            div_3_meses=dy_3_meses,
            div_6_meses=dy_6_meses,
            div_12_meses=dy_12_meses,
            dy_1_mes=dividendo_1_mes,
            dy_3_meses=dividendo_3_meses,
            dy_6_meses=dividendo_6_meses,
            dy_12_meses=dividendo_12_meses,
        )

    def obter_cotacao(self) -> str:
        return self._driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.cotacao > div._card-body > div > span"
        ).text.strip()

    def obter_dividend_yield_1_mes(self) -> tuple[str, str]:
        dividend_yield = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(1) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(1) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def obter_dividend_yield_3_meses(self) -> tuple[str, str]:
        dividend_yield = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(2) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(2) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def obter_dividend_yield_6_meses(self) -> tuple[str, str]:
        dividend_yield = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(3) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(3) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def obter_dividend_yield_12_meses(self) -> tuple[str, str]:
        dividend_yield = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(4) > span.content--info--item--value",
        ).text.strip()
        dividendo_pago = self._driver.find_element(
            By.CSS_SELECTOR,
            "#yield-distribuition > div > div.content--info > div:nth-child(4) > span.content--info--item--value.amount",
        ).text.strip()

        return (dividend_yield, dividendo_pago)

    def obter_segmento(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("segmento")

    def obter_tipo_de_fundo(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("TIPO DE FUNDO")

    def obter_pvp(self) -> str:
        return self._driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.vp > div._card-body > span"
        ).text.strip()

    def obter_quantidade_cotas_emitidas(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("COTAS EMITIDAS")

    def obter_valor_patrimonial_por_cota(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("VAL. PATRIMONIAL P/ COTA")

    def __scrape_informacoes_sobre_empresa(self) -> list[WebElement]:
        if not self.__informacoes_sobre_empresa:
            self.__informacoes_sobre_empresa = self._driver.find_elements(By.CSS_SELECTOR, "#table-indicators > div")

        return self.__informacoes_sobre_empresa

    def __obter_valor_de_informacoes_da_empresa(self, tipo_informacao: str) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()

        for elemento in informacoes_sobre_empresa:
            if (
                str(elemento.find_element(By.CSS_SELECTOR, "div.desc > span").text).strip().lower()
                == tipo_informacao.lower()
            ):
                return elemento.find_element(By.CSS_SELECTOR, "div.desc > div > span").text.strip()

        raise ElementoNaoEncontradoError(seletor=tipo_informacao.upper())
